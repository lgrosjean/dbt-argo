# pylint: disable=line-too-long,too-many-arguments,too-many-locals
import typing as t

from croniter import CroniterBadCronError, croniter
from dbt.contracts.graph.manifest import Manifest
from hera.workflows import (
    DAG,
    Container,
    CronWorkflow,
    Env,
    GCSArtifact,
    Parameter,
    Resources,
    Steps,
    Task,
    Workflow,
)

from .utils import DBT_IMAGE, clean_name


# TODO: creer une fonction "base" qui permet de générer le dbt_base, dag et pipeline
# pour le réutiliser dans dans create_dbt_workflow and create_dbt_cronworkflow
def _base_workflow():
    raise NotImplementedError


def create_dbt_workflow(
    manifest: Manifest,
    gcs_bucket: str,
    env: str,  # Used by dbt to be executed
    gcp_project_id: str,  # Used by dbt to be executed
    command: str = "run",
    name: str = "dbt-workflow",
    service_account_name: t.Optional[str] = None,
    namespace: t.Optional[str] = None,
):
    """
    Create an hera workflow object which runs a dbt pipeline workflow, based on
    dbt Manifest object
    """

    entrypoint = "pipeline"

    with Workflow(
        generate_name=f"{name}-",
        namespace=namespace,
        entrypoint=entrypoint,
        service_account_name=service_account_name,
    ) as workflow:
        # create a func dbt_base which returns dbt_base_op
        dbt_base = Container(
            image=DBT_IMAGE,
            working_dir="/app",
            inputs=[
                Parameter(name="command"),  # type: ignore
                Parameter(name="args", default=""),  # type: ignore
                GCSArtifact(name="models", path="/app", bucket=gcs_bucket, key=name),  # type: ignore
            ],
            name="dbt-base",
            command=["/bin/sh"],
            args=["-c", "dbt {{inputs.parameters.command}} {{inputs.parameters.args}}"],
            resources=Resources(
                cpu_limit="0.15",
                cpu_request="0.1",
                memory_limit="300Mi",
                memory_request="200Mi",
            ),
            env=[
                Env(name="ENV", value=env),
                Env(name="GCP_PROJECT_APP", value=gcp_project_id),
                Env(name="DBT_PROFILES_DIR", value="./"),
            ],
        )

        with DAG(name=f"dbt-{command}") as dag:
            tasks = {}

            # #1. create tasks
            for node_name, node in manifest.nodes.items():
                if node.resource_type == "model" and node.config.materialized in (
                    "table",
                    "view",
                    "ephemeral",
                ):
                    # print(node.name)
                    tasks[node_name] = dbt_base(
                        name=clean_name(node.name),
                        arguments={"command": command, "args": f"-s {node_name}"},
                    )

            # 2. Create dependencies
            for node_name, node in manifest.nodes.items():
                if node.resource_type == "model":
                    task = tasks[node_name]
                    for node_parent_name in node.depends_on.nodes:  # type: ignore
                        node_parent = manifest.nodes[node_parent_name]
                        if node_parent.config.materialized in (
                            "table",
                            "view",
                            "ephemeral",
                        ):
                            task_parent: Task = tasks[node_parent_name]
                            task_parent.next(task)

        with Steps(name=entrypoint):
            dbt_base(name="dbt-seed-step", arguments={"command": "seed"})
            dag(name=f"dbt-{command}-step")

        return workflow


def create_dbt_cronworkflow(
    manifest: Manifest,
    schedule: str,
    gcs_bucket: str,
    env: str,  # Used by dbt to be executed
    gcp_project_id: str,  # Used by dbt to be executed
    command: str = "run",
    name: str = "dbt-workflow",
    service_account_name: t.Optional[str] = None,
    namespace: t.Optional[str] = None,
    timezone: t.Optional[str] = None,
    suspend: t.Optional[bool] = None,
):
    """
    Create an hera workflow object which runs a dbt pipeline workflow, based on
    dbt Manifest object
    """

    if not croniter.is_valid(schedule):
        raise CroniterBadCronError(f"Not valid cron : {schedule}")

    entrypoint = "pipeline"

    with CronWorkflow(
        generate_name=f"{name}-",
        schedule=schedule,
        namespace=namespace,
        entrypoint=entrypoint,
        service_account_name=service_account_name,
        timezone=timezone,
        suspend=suspend,
    ) as workflow:
        # create a func dbt_base which returns dbt_base_op
        dbt_base = Container(
            image=DBT_IMAGE,
            working_dir="/app",
            inputs=[
                Parameter(name="command"),  # type: ignore
                Parameter(name="args", default=""),  # type: ignore
                GCSArtifact(name="models", path="/app", bucket=gcs_bucket, key=name),  # type: ignore
            ],
            name="dbt-base",
            command=["/bin/sh"],
            args=["-c", "dbt {{inputs.parameters.command}} {{inputs.parameters.args}}"],
            resources=Resources(
                cpu_limit="0.15",
                cpu_request="0.1",
                memory_limit="300Mi",
                memory_request="200Mi",
            ),
            env=[
                Env(name="ENV", value=env),
                Env(name="GCP_PROJECT_APP", value=gcp_project_id),
                Env(name="DBT_PROFILES_DIR", value="./"),
            ],
        )

        with DAG(name=f"dbt-{command}") as dag:
            tasks = {}

            # #1. create tasks
            for node_name, node in manifest.nodes.items():
                if node.resource_type == "model" and node.config.materialized in (
                    "table",
                    "view",
                    "ephemeral",
                ):
                    # print(node.name)
                    tasks[node_name] = dbt_base(
                        name=clean_name(node.name),
                        arguments={"command": command, "args": f"-s {node_name}"},
                    )

            # 2. Create dependencies
            for node_name, node in manifest.nodes.items():
                if node.resource_type == "model":
                    task = tasks[node_name]
                    for node_parent_name in node.depends_on.nodes:  # type: ignore
                        node_parent = manifest.nodes[node_parent_name]
                        if node_parent.config.materialized in (
                            "table",
                            "view",
                            "ephemeral",
                        ):
                            task_parent: Task = tasks[node_parent_name]
                            task_parent.next(task)

        with Steps(name=entrypoint):
            dbt_base(name="dbt-seed-step", arguments={"command": "seed"})
            dag(name=f"dbt-{command}-step")

        return workflow
