"""
Wrapper around GCP Document AI, handles ADC or service-account JSON, with access validation.
"""
import os
import click
import google.auth
from google.oauth2 import service_account
from google.cloud import documentai_v1 as documentai
from utils.config import (
    GOOGLE_APPLICATION_CREDENTIALS,
    GCP_PROJECT_ID,
    GCP_LOCATION,
    GCP_PROCESSOR_ID,
)

class DocumentAIClient:
    def __init__(self):
        # 1) Try service-account JSON if provided and exists
        sa_path = GOOGLE_APPLICATION_CREDENTIALS
        if sa_path and os.path.exists(sa_path):
            creds = service_account.Credentials.from_service_account_file(sa_path)
            # Use explicit project ID if set
            proj = GCP_PROJECT_ID
        else:
            # Clear invalid env var so google.auth.default() won't pick it up
            os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
            # 2) Fallback to application-default credentials
            creds, proj = google.auth.default()

        # Initialize the Document AI client
        self.client = documentai.DocumentProcessorServiceClient(credentials=creds)

        # Determine which project to use
        project = GCP_PROJECT_ID or proj
        self.name = (
            f"projects/{project}/locations/{GCP_LOCATION}"
            f"/processors/{GCP_PROCESSOR_ID}"
        )

        # Validate access by retrieving the processor metadata
        from google.api_core.exceptions import PermissionDenied, InvalidArgument
        try:
            _ = self.client.get_processor(request={"name": self.name})
        except PermissionDenied:
            click.echo(
                f"Warning: permission denied for processor {self.name}, skipping validation."
            )
        except InvalidArgument:
            click.echo(
                f"Warning: invalid processor resource '{self.name}', skipping validation."
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to validate Document AI processor access: {e}"
            )
