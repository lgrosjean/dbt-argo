from typing import List

from .argo.arguments import Arguments
from .argo.container import Container
from .argo.dag_task import DAGTask
from .argo.dag_template import DAGTemplate
from .argo.inputs import Inputs
from .argo.parameter import Parameter
from .argo.template import Template
from .argo.workflow_spec import WorkflowSpec
from .argo.workflow_step import WorkflowStep
from .dbt import DbtManifest, DbtNode

DBT_IMAGE = "ghcr.io/dbt-labs/dbt-bigquery"


class DbtContainer(Container):
    """A single dbt application container to run within a pod."""

    def __init__(self, version: str = "latest"):
        super().__init__(
            image=f"{DBT_IMAGE}:{version}",
            command=["/bin/sh"],
            args=[
                "-c",
                "dbt {{ inputs.parameters.command }} {{ inputs.parameters.args }}",
            ],
        )


class DbtBaseTemplate(Template):
    """dbt Template unit of execution in a workflow"""

    def __init__(self, name="dbt-base", version="latest"):
        super().__init__(
            name=name,
            container=DbtContainer(version=version),
            inputs=Inputs(
                parameters=[Parameter(name="command"), Parameter(name="args", value="")]
            ),
        )


class DbtDAGTask(DAGTask):
    """A single dbt node execution"""

    def __init__(self, node: DbtNode, dependencies: List[str], base_name="dbt-base"):
        super().__init__(
            name=node.name,
            template=base_name,
            arguments=Arguments(
                parameters=[
                    Parameter(name="command", value="run"),
                    Parameter(name="args", value=f"-s {node.node_name}"),
                ]
            ),
            dependencies=dependencies,
        )


class DbtRunTemplate(Template):
    """An Argo template defining the DAG of tasks and dependencies based on
    the dbt manifest given in args"""

    def __init__(self, manifest: DbtManifest, name="run", base_name="dbt-base"):
        tasks = []
        for node in manifest.nodes.values():
            dependencies = manifest.get_dependencies(node)
            dbt_task = DbtDAGTask(node, dependencies, base_name=base_name)
            tasks.append(dbt_task)

        dag_template = DAGTemplate(tasks=tasks)
        super().__init__(name=name, dag=dag_template)


class DbtRunStep(WorkflowStep):
    def __init__(self, name="run"):
        super().__init__(name=name, template=name)


class DbtSeedStep(WorkflowStep):
    def __init__(self, name="seed", base_name="dbt-base"):
        super().__init__(
            name=name,
            template=base_name,
            arguments=Arguments(
                parameters=[
                    Parameter(name="command", value="seed"),
                    # Parameter(name="args", value=""),
                ]
            ),
        )


class DbtPipelineTemplate(Template):
    def __init__(
        self, name="pipeline", base_name="dbt-base", seed_name="seed", run_name="run"
    ):
        dbt_seed_step = DbtSeedStep(name=seed_name, base_name=base_name)
        dbt_run_step = DbtRunStep(name=run_name)

        steps = [
            [dbt_seed_step],
            [dbt_run_step],
        ]

        super().__init__(name=name, steps=steps)


class DbtWorkflowSpec(WorkflowSpec):
    def __init__(
        self,
        manifest: DbtManifest,
        base_name="dbt-base",
        seed_name="seed",
        run_name="run",
        pipeline_name="pipeline",
    ):
        dbt_base_template = DbtBaseTemplate(name=base_name)
        dbt_run_template = DbtRunTemplate(
            manifest, name=run_name, base_name=dbt_base_template.name
        )
        dbt_pipeline_template = DbtPipelineTemplate(
            name=pipeline_name,
            base_name=dbt_base_template.name,
            seed_name=seed_name,
            run_name=run_name,
        )

        templates = [
            dbt_base_template,
            dbt_run_template,
            dbt_pipeline_template,
        ]

        super().__init__(entrypoint=pipeline_name, templates=templates)
