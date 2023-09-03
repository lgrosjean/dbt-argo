DBT_IMAGE = "ghcr.io/dbt-labs/dbt-bigquery"


def clean_name(name: str):
    """
    _int_webinar__webinar_ru > int-webinar--webinar-ru
    """
    return name.replace("_", "-").strip("-")
