import typing as t
from pathlib import Path

from cloudpathlib import GSPath
from google.cloud import storage

DBT_IMAGE = "ghcr.io/dbt-labs/dbt-bigquery"


def clean_name(name: str):
    """
    _int_webinar__webinar_ru > int-webinar--webinar-ru
    """
    return name.replace("_", "-").strip("-")


# Source: https://stackoverflow.com/a/52193880
def copy_dir_to_gcs(
    local_path: t.Union[str, Path],
    gcs_path: str,
    gcp_project_id: t.Optional[str] = None,
):
    """Recursively copy a directory of files to GCS."""

    dir_path = Path(local_path)

    if not dir_path.exists():
        raise NotADirectoryError()

    gcs_pathlib = GSPath(gcs_path)

    bucket_name = gcs_pathlib.bucket

    client = storage.Client(project=gcp_project_id)
    bucket = client.get_bucket(bucket_name)

    for file_path in dir_path.rglob("*"):
        if not file_path.is_file():
            continue

        print(f"Local file: {file_path}")
        relative_file_path = file_path.relative_to(dir_path)
        print(f"Relative file: {relative_file_path}")

        remote_path = gcs_pathlib / relative_file_path.as_posix()

        print(remote_path.blob)
        blob = bucket.blob(remote_path.blob)
        blob.upload_from_filename(file_path)
