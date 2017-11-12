Solida
======
.. image:: https://travis-ci.org/gmauro/solida.svg?branch=master
    :target: https://travis-ci.org/gmauro/solida

NGS pipelines bootstrapper


Usage
-----

To check version:

.. code-block:: console

    $ solida -v

To list all the pipelines enabled, digit

.. code-block:: console

    $ solida list
    $ solida list --full

To check if both pipeline and profile are available, digit:

.. code-block:: console

    $ solida pipeline -l pipeline_label -p profile_label

Before to deploy a pipeline, you need to be create a project profile:

.. code-block:: console

    $ solida pipeline -l pipeline_label -p profile_label --create-profile

| Solida will create a yaml file named *profile_label.yaml* into *~/solida_profiles*.
| Edit the *profile_label.yaml* to match your environment settings.

After that, deploy the pipeline with:

.. code-block:: console

    $ solida pipeline -l pipeline_label -p profile_label --deploy


Requirements
------------

To run Solida, you need Conda.  
To install it, see `conda.io`_

.. _conda.io: https://conda.io/miniconda.html
