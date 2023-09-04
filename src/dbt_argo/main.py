import yaml
from couler.argo_submitter import ArgoSubmitter

from dbt_argo.argo.base import WorkflowFactory
from dbt_argo.dbt import DbtManifest
from dbt_argo.dbt_workflow import DbtWorkflowSpec

from .utils import load_yaml


# T-12 use a "project_dir" folder instead
def main(config_path: str, manifest_path: str, output_path: str):
    """Main function to run to parsing and bumping"""

    config = load_yaml(config_path)
    manifest = DbtManifest.load(manifest_path)

    base_workflow = WorkflowFactory(config)

    dbt_workflow_spec = DbtWorkflowSpec(manifest=manifest)

    dbt_workflow = base_workflow.set_workflow_spec(dbt_workflow_spec)

    with open(output_path, "w", encoding="utf8") as f:
        workflow_yaml = dbt_workflow.model_dump(exclude_none=True)
        yaml.dump(workflow_yaml, f)

    submitter = ArgoSubmitter(namespace="omni-leogrosjean")

    submitter.submit(workflow_yaml)
