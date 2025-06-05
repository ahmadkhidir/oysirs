from celery import shared_task
from django.utils import timezone


@shared_task(name="upload_records_task")
def upload_records_task(mapping: dict):
    """
    This function is a Celery task that uploads records to the database.
    It processes a file, extracts data, and creates records in the database.
    """
    from .helper import upload_records

    # Call the upload_records function with the provided mapping
    total_records = upload_records(mapping)
    return f"Uploaded {total_records} records successfully."