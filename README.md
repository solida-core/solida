# Solida
NGS pipeline bootstrapper

## Usage

To list all the pipelines enabled, digit
```bash
solida list
solida list --full
```

To check if both pipeline and profile are available, digit:
```bash
solida pipeline -l pipeline_label -p profile_label
```

Before to deploy a pipeline, you need to be create a project profile:
```bash
solida pipeline --create-profile -l pipeline_label -p profile_label 
```
Solida will create a yaml file named _profile_label.yaml_ into _~/solida_profiles_  
Edit the _profile_label.yaml_ to match your environment settings.

After that, deploy the pipeline with:
```bash
solida pipeline --deploy -l pipeline_label -p profile_label
```

## Requirements

To run Solida, you need Conda.  
To install it, see [https://conda.io/miniconda.html](https://conda.io/miniconda.html) 
