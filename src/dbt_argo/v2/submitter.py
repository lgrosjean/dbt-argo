# Source: https://github.com/couler-proj/couler/blob/master/couler/argo_submitter.py
import logging
import re

import pyaml
import yaml
from kubernetes import client as k8s_client
from kubernetes import config


class WorkflowCRD(object):
    PLURAL = "workflows"
    KIND = "Workflow"
    GROUP = "argoproj.io"
    VERSION = "v1alpha1"
    NAME_MAX_LENGTH = 45
    NAME_PATTERN = r"[a-z]([-a-z0-9]*[a-z0-9])?"


class CronWorkflowCRD(WorkflowCRD):
    PLURAL = "cronworkflows"
    KIND = "CronWorkflow"


class _SubmitterImplTypes:
    PYTHON = "Python"
    GO = "Go"


# TODO: some k8s common parts can move to another file later.
class ArgoSubmitter:
    """A submitter which submits a workflow to Argo"""

    _default_submitter = None

    def __init__(
        self,
        namespace="default",
        config_file=None,
        context=None,
        client_configuration=None,
        persist_config=True,
    ):
        logging.basicConfig(level=logging.INFO)
        self.namespace = namespace
        logging.info("Argo submitter namespace: %s" % self.namespace)

        try:
            config.load_kube_config(
                config_file, context, client_configuration, persist_config
            )
            logging.info(
                "Found local kubernetes config. " "Initialized with kube_config."
            )
            if client_configuration is not None:
                logging.info("Setting default k8s client config as provided")
                k8s_client.Configuration.set_default(client_configuration)
        except Exception:
            logging.info("Cannot find local k8s config. " "Trying in-cluster config.")
            config.load_incluster_config()
            logging.info("Initialized with in-cluster config.")

        self._custom_object_api_client = k8s_client.CustomObjectsApi()
        self._core_api_client = k8s_client.CoreV1Api()

    @staticmethod
    def check_name(name):
        """Check the name is valid or not"""
        if len(name) > WorkflowCRD.NAME_MAX_LENGTH:
            raise ValueError(
                "Name is too long. Max length: {}, now: {}"
                "".format(WorkflowCRD.NAME_MAX_LENGTH, len(name))
            )
        if "." in name:
            raise ValueError("Name cannot include dot.")
        if "_" in name:
            raise ValueError("Name cannot include underscore.")

        match_obj = re.match(WorkflowCRD.NAME_PATTERN, name)
        if not match_obj:
            raise ValueError(
                "Name is invalid. Regex used for validation is %s"
                % WorkflowCRD.NAME_PATTERN
            )

    def get_custom_object_api_client(self):
        return self._custom_object_api_client

    def get_core_api_client(self):
        return self._core_api_client

    def submit(self, workflow_yaml, secrets=None):
        wf_name = (
            workflow_yaml["metadata"]["name"]
            if "name" in workflow_yaml["metadata"]
            else workflow_yaml["metadata"]["generateName"]
        )
        if secrets:
            for secret in secrets:
                if secret.use_existing is False:
                    if secret.artifact_secret is True:
                        # For artifact secrets, check if the secret already exists
                        if secret.name in [
                            x.metadata.name
                            for x in self.get_core_api_client()
                            .list_namespaced_secret(namespace=self.namespace)
                            .items
                        ]:
                            logging.info(
                                "Secret {} already exists in the {} namespace. Skipping creation.".format(
                                    secret.name, self.namespace
                                )
                            )
                        else:
                            # Otherwise create the secret
                            self._create_secret(secret.to_yaml())
                    else:
                        # For all other secrets
                        self._create_secret(secret.to_yaml())

        logging.info("Checking workflow name/generatedName %s" % wf_name)
        self.check_name(wf_name)
        return self._create_workflow(workflow_yaml)

    def _create_workflow(self, workflow_yaml):
        yaml_str = pyaml.dump(workflow_yaml)
        workflow_yaml = yaml.safe_load(yaml_str)
        logging.info("Submitting workflow to Argo")
        try:
            response = self._custom_object_api_client.create_namespaced_custom_object(  # noqa: E501
                WorkflowCRD.GROUP,
                WorkflowCRD.VERSION,
                self.namespace,
                WorkflowCRD.PLURAL
                if workflow_yaml["kind"] == WorkflowCRD.KIND
                else CronWorkflowCRD.PLURAL,
                workflow_yaml,
            )
            logging.info(
                'Workflow %s has been submitted in "%s" namespace!'
                % (response.get("metadata", {}).get("name"), self.namespace)
            )
            return response
        except Exception as e:
            logging.error("Failed to submit workflow")
            raise e

    def _create_secret(self, secret_yaml):
        yaml_str = pyaml.dump(secret_yaml)
        secret_yaml = yaml.safe_load(yaml_str)
        return self._core_api_client.create_namespaced_secret(  # noqa: E501
            self.namespace, secret_yaml
        )
