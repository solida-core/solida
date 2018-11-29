import curses
import os

from comoda import a_logger, ensure_dir, path_is_empty, path_exists
from comoda.yaml import dump
from git import Repo

from solida import cache_dir
from .config_manager import ConfigurationManager
from .pipelines_manager import Pipeline


class CacheManager:
    def __init__(self, args=None):
        self.loglevel = args.loglevel
        self.logfile = args.logfile
        self.logger = a_logger(self.__class__.__name__, level=self.loglevel,
                               filename=self.logfile)
        path_from_cli = args.config_file if 'config_file' in vars(args) else None
        cm = ConfigurationManager(args=args,
                                  path_from_cli=path_from_cli)
        self.conf = cm.get_pipelines_config
        self.core_environment_file = cm.get_default_config[
            'core_environment_file']
        self.environment_file = cm.get_default_config[
            'project_environment_file']
        self.cache_dir = cache_dir
        ensure_dir(self.cache_dir)

        self.ask_before_to_refresh = args.ask if 'ask' in vars(args) else False

    def clone(self, label):
        pipeline = Pipeline(self.conf[label], loglevel=self.loglevel,
                            logfile=self.logfile)
        repo_dir = os.path.join(self.cache_dir, label)
        ensure_dir(repo_dir)
        if path_is_empty(repo_dir):
            print("Cloning {}".format(pipeline.url))
            Repo.clone_from(pipeline.url, repo_dir)
            repo = Repo(repo_dir)
            heads = repo.heads
            master = heads.master
            with open(os.path.join(repo_dir, ".git_repo_last_commit"), 'w') as filename:
                filename.write(pipeline.url)
                filename.write("\ncommit id: {}".format(master.commit))

            requirements_path = os.path.join(repo_dir, self.core_environment_file)
            if not path_exists(requirements_path):
                data = {'channels': ['bioconda', 'conda-forge', 'defaults'],
                        'dependencies': ['python==3.6.1', 'pip']}
                dump(data, requirements_path)

            requirements_path = os.path.join(repo_dir, self.environment_file)
            if not path_exists(requirements_path):
                data = {'channels': ['bioconda', 'conda-forge', 'defaults'],
                        'dependencies': ['snakemake', 'drmaa==0.7.8']}
                dump(data, requirements_path)

            print("commit id: {}".format(master.commit))
            print("Done.\n")
            self.logger.info('Cloned git repo at {} into {} '
                             'directory'.format(pipeline.url, repo_dir))
        else:
            self.logger.warning("Can't clone git repo {} "
                                "into {}".format(pipeline.url,
                                                 repo_dir))

    def clones(self):
        for p in self.conf.keys():
            self.clone(p)

    def update(self, label):
        pipeline = Pipeline(self.conf[label], loglevel=self.loglevel,
                            logfile=self.logfile)
        skip = ''
        if self.ask_before_to_refresh:
            msg = ("Updating {} - {}".format(pipeline.label.capitalize(),
                                             pipeline.description))
            skip = self.user_input(msg)
        if skip != ord('s'):
            repo_dir = os.path.join(self.cache_dir, label)
            ensure_dir(repo_dir, force=True)
            self.clone(label)

    def updates(self):
        for p in self.conf.keys():
            self.update(p)

    @staticmethod
    def user_input(msg):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.addstr(0, 0, msg)
        stdscr.addstr(1, 0, 'Enter s to skip or any other else to continue')
        c = stdscr.getch()
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        return c
