# dbt-argo

![PyPI - Version](https://img.shields.io/pypi/v/dbt-argo?logo=pypi&color=blue&link=https%3A%2F%2Fpypi.org%2Fproject%2Fdbt-argo%2F)


A simple Python package to parse dbt dependencies to create an Argo Workflow job. It can also submit Argo files directly to the server.

## Motivations

Simplify CI steps to create Argo workflow for dbt projects.

## Limitations

- This version only support Google Cloud Storage as backend to store **dbt artifacts** to be used by Argo as artifacts.
- This version only support `CronWorkflow` and `Workflow` generation

## Usage

By default, it assumes the `dbt_project.yml` file is located at the root folder, if not the `DBT_PROJECT_DIR` can be defined to locate the project path.

```sh
Usage: dbt-argo [OPTIONS] COMMAND [ARGS]...

  Test

Options:
  --help  Show this message and exit.

Commands:
  cp      copy local folder to GCS Bucket
  create  Create a dbt Argo Workflow
  cron    Manage cron workflow
  submit  dbt-argo deploy {FILE
```

## Inspirations

- [Hera](https://github.com/argoproj-labs/hera) for pydantic + argo
- [couler](https://github.com/couler-proj/couler) for cluster submission
- [dbt > 1.5](https://docs.getdbt.com/reference/programmatic-invocations) for easy manifest parsing directly in python scripts
- [Argo CLI](https://argoproj.github.io/argo-workflows/walk-through/argo-cli/) for cli options
- [kubectl](https://argoproj.github.io/argo-workflows/kubectl/) for create functiin definition
