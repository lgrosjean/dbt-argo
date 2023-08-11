from os.path import join

import click

from dbt_argo.main import main


@click.command(name="dbt-argo", context_settings={"show_default": True})
@click.argument("path", default=".")
@click.option(
    "--target-path",
    default="./target",
    help="""
    Define the dbt target directory location, containing manifest.json.
""",
)
@click.option(
    "--output-file",
    default="dbt-workflow.yaml",
    help="File path to insert output into.",
)
def cli(
    path: str,
    target_path: str,
    output_file: str,
):
    """CLI program to run the dbt-argo converter

    PATH: base project path containing the `.dbt-argo.yml` conf file (default=".")
    """
    config_path = join(path, ".dbt-argo.yml")
    manifest_path = join(path, target_path, "manifest.json")
    main(
        config_path=config_path,
        manifest_path=manifest_path,
        output_path=output_file,
    )


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
