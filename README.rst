Solida
======
SOLIDA is command-line solution that facilitate the reproducibility and portability of NGS pipelines. It can easily organize the deployment, the data management and the execution of a Snakemake based workflow.

|build|

Installation
------------

You can install the latest stable version from PyPI

.. code:: console

    $ pip install solida


Prerequisites
-------------

To run Solida, you need Conda.
To install it, see `conda.io`_


Usage
-----

To check version:

.. code-block:: console

    $ solida -v

To list all the pipelines enabled, digit

.. code-block:: console

    $ solida info

To check if both pipeline and profile are available, digit:

.. code-block:: console

    $ solida setup -l pipeline_label -p profile_label

Before to deploy a pipeline, you have to create a project profile:

.. code-block:: console

    $ solida setup -l pipeline_label -p profile_label --create-profile

| Solida will create a yaml file named *profile_label.yaml* into *~/solida_profiles*.
| Edit the *profile_label.yaml* to match your environment settings.


After that, deploy the pipeline into localhost with:

.. code-block:: console

    $ solida setup -l pipeline_label -p profile_label --deploy

If you want to deploy the pipeline into a remote host, add these
arguments:

.. code-block:: console

    $ solida setup -l pipeline_label -p profile_label --deploy --host remote_host --remote-user username --connection ssh

where:

*--host* is the hostname of the remote host

*--remote-user* is a username available in the remote host

*--connection* is the type of connection to use


Pay attention, *remote_user* have to be able to do ssh login into *remote_host*
without password (SSH Key-Based Authentication)

.. _conda.io: https://conda.io/miniconda.html

.. |build| image:: https://travis-ci.org/gmauro/solida.svg?branch=master
   :target: https://travis-ci.org/gmauro/solida
   :alt: Continuous Integration

.. |license| image:: http://img.shields.io/badge/license-GPLv3-blue.svg
   :target: https://github.com/gmauro/solida/blob/master/LICENSE
