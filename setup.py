import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'APPNAME')) as f:
    __appname__ = f.read().strip()

with open(os.path.join(here, 'VERSION')) as f:
    __version__ = f.read().strip()


with open(os.path.join(here, 'requirements.txt')) as f:
    required = f.read().splitlines()

with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

extra_files = [os.path.join(here, 'VERSION'),
               os.path.join(here, 'APPNAME'),
               os.path.join(here, 'solida', 'config', 'config.yaml'),
               os.path.join(here, 'solida', 'playbooks',
                            'common.yaml'),
               os.path.join(here, 'solida', 'playbooks',
                            'install_pipeline.yaml'),
               os.path.join(here, 'solida', 'playbooks',
                            'install_diva.yaml'),
               os.path.join(here, 'solida', 'playbooks',
                            'install_ride.yaml'),
               os.path.join(here, 'solida', 'playbooks',
                            'templates', 'run.project.j2'),
               os.path.join(here, 'solida', 'playbooks',
                            'vars', 'main.yaml'),
               os.path.join(here, 'solida', 'playbooks',
                            'vars', 'diva.yaml'),
               ]

setup(
    name=__appname__,
    version=__version__,
    description='NGS pipelines bootstrapper',
    long_description=long_description,

    # The project's main homepage.
    url='https://bitbucket.org/biopipelines/solida',

    # Author details
    author='Gianmauro Cuccuru',
    author_email='gmauro@crs4.it',
    # Choose your license
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],

    # What does your project relate to?
    keywords='NGS, pipeline deployment, bioinformatics',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),
    package_data={'': extra_files},

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=required,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'solida=solida.__main__:main',
        ],
    },
)
