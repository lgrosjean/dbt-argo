# pylint: disable=line-too-long,too-many-arguments,too-many-locals
"""CLI methods to run dbt-argo app"""

import sys

import click
import yaml
from couler.argo_submitter import ArgoSubmitter  # pylint: disable=import-error
from dbt.cli.main import dbtRunner, dbtRunnerResult
from dbt.contracts.graph.manifest import Manifest

from .workflows import create_dbt_workflow


@click.group(invoke_without_command=True)
def cli():
    """Test"""
    ctx = click.get_current_context()
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(name="create")
# Some for cron
@click.option("--name", default="analytics-adhoc", show_default=True)
@click.option("--gcs-bucket", envvar="GCS_BUCKET", required=True, show_default=True)
@click.option("--namespace", envvar="K8S_NAMESPACE", show_default=True)
@click.option("--service-account-name", envvar="K8S_SA", show_default=True)
@click.option("--env", envvar="ENV", show_default=True)
@click.option("--gcp_project_id", envvar="GCP_PROJECT_ID", show_default=True)
@click.option("--submit", is_flag=True)
@click.option("--echo", is_flag=True)
@click.argument("command", type=click.Choice(["build", "run"]))
def create_workflow(
    name,
    gcs_bucket,
    namespace,
    service_account_name,
    env,
    gcp_project_id,
    submit,
    echo,
    command,
):
    """Create a dbt Argo Workflow"""

    # https://docs.getdbt.com/reference/programmatic-invocations#reusing-objects
    res: dbtRunnerResult = dbtRunner().invoke(["parse"])
    if isinstance(res.result, Manifest):
        manifest = res.result

        workflow = create_dbt_workflow(
            manifest,
            name=name,
            command=command,
            service_account_name=service_account_name,
            namespace=namespace,
            gcs_bucket=gcs_bucket,
            env=env,
            gcp_project_id=gcp_project_id,
        )

        filepath = workflow.to_file(name=name)

        if echo:
            click.echo()
            click.echo(workflow.to_yaml())

        if submit:
            submit_workflow(filepath, dry_run=False)


@cli.group(invoke_without_command=True)
def cron():
    """Manage cron workflow"""
    ctx = click.get_current_context()
    click.echo(ctx.get_help())


@cron.command(name="create")
@click.option("--schedule", default="1 * * * *", show_default=True)
@click.option("--timezone", default="Europe/Paris", show_default=True)
@click.option("--suspend", default=False, show_default=True)
@click.argument("command", type=click.Choice(["build", "run"]))
def create_cron(schedule, timezone, suspend, command):
    """Create a dbt Argo CronWorkflow"""
    click.echo("Building cronworkflow")
    click.echo(f"Command: {command}")


@cli.command(name="submit")
@click.option("-f", "--filename")
@click.option("--dry-run", is_flag=True)
def submit_workflow(filename, dry_run):
    """dbt-argo deploy {FILE}"""
    click.echo(f" Deploying {filename}!")

    submitter = ArgoSubmitter(namespace="omni-leogrosjean")
    with open(filename, encoding="utf8") as file:
        workflow_yaml = yaml.safe_load(file)
    if dry_run:
        sys.exit("Dry run mode...")
    # submitter.submit(workflow_yaml)
    print("hello")
