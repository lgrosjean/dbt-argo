"""
Source: https://argoproj.github.io/argo-workflows/fields/#artifact
"""
from pydantic import BaseModel, Field


class GCSArtifact(BaseModel):
    """GCSArtifact is the location of a GCS artifact"""

    bucket: str = Field(description="Bucket is the name of the bucket")
    key: str = Field(
        description="Key is the path in the bucket where the artifact resides"
    )


class Artifact(BaseModel):
    """Artifact indicates an artifact to place at a specified path"""

    name: str
    path: str = "/app"
    gcs: GCSArtifact
