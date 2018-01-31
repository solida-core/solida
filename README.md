# Solida [![Build Status](https://travis-ci.org/gmauro/solida.svg?branch=master)](https://travis-ci.org/gmauro/solida)
NGS pipelines bootstrapper


## Installation

You can install the latest stable version from PyPI
```bash
pip install solida
```

## Requirements

To run Solida, Conda must be present in your computer.    
To install it, see [https://conda.io/miniconda.html](https://conda.io/miniconda.html) 

## Usage

To check version:
```bash
solida -v
```

To list all the pipelines enabled, digit
```bash
solida list
solida list --full
```

To check if both pipeline and profile are available, digit:
```bash
solida pipeline -l pipeline_label -p profile_label
```

Before to deploy a pipeline, you have to create a project profile:
```bash
solida pipeline -l pipeline_label -p profile_label --create-profile 
```
Solida will create a yaml file named _profile_label.yaml_ into _~/solida_profiles_  
Edit the _profile_label.yaml_ to match your environment settings.

After that, deploy the pipeline with:
```bash
solida pipeline -l pipeline_label -p profile_label --deploy 
```
### Script to execute the workflow
Solida provides a bash script, _**run.project.sh**_, to facilitate the 
workflow execution.  

```
run.project.sh [-h] [-s Snakefile] -c FILENAME [-w DIR] [-p "parameters"] --script to execute a snakemake workflow

where:
    -h  show this help text
    -s  path to a Snakefile different from the default one (Snakefile).
    -c  path to the snakemake's configuration file.
    -w  is the project's workdir label. Default is current timestamp.
    -p  snakemake parameters as "--rerun-incomplete --dryrun --keep-going --restart-time"
```
Use _-s_ to specify a different Snakefile.  

If you don't give the script a workdir label (_-w_), a directory with the current 
timestamp as label will be created and used to collect results into.

Option _-c_ is mandatory and have to be the path to the snakemake's configuration file.
 
Option _-p_ permit to provide the script all the snakemake parameters (don't 
forget to encapsulate them with """).
