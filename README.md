# dbt-argo

A simple Python package to parse dbt dependencies to create an Argo Workflow job

## Limitations

- This version only support Google Cloud Storage as backend to store `manifest.json` and `dbt models` files to be executed.
- This version only support `CronWorkflow` and `Workflow` generation

## Usage

```sh
dbt-argo [PATH] \
    --target-path [TARGET_PATH] \
    --output_file [OUTPUT_FILE]
```
## `.dbt-argo.yml` configuration file

This file is a simplify Argo Workflow spec file. It only contains root configuration options and any reference to templates, steps or containers.

## TODO

- Créer un CLI qui permet de générer sans fichier de config (dbt-argo cronworkflow . --schedule ... --name ...--service_account ...)