# Solida [![Build Status](https://travis-ci.org/gmauro/solida.svg?branch=master)](https://travis-ci.org/gmauro/solida)
NGS pipelines bootstrapper

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

## Requirements

To run Solida, Conda must be present in your computer.    
To install it, see [https://conda.io/miniconda.html](https://conda.io/miniconda.html) 
