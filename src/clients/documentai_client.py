"""
Wrapper around GCP Document AI, handles ADC or service-account JSON, with access validation.
"""
import os
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
        # Use Application Default Credentials or service account file
        if GOOGLE_APPLICATION_CREDENTIALS and os.path.exists(GOOGLE_APPLICATION_CREDENTIALS):
            creds = service_account.Credentials.from_service_account_file(
                GOOGLE_APPLICATION_CREDENTIALS
            )
        else:
            creds, proj = google.auth.default()
        # Initialize the Document AI client with credentials
        self.client = documentai.DocumentProcessorServiceClient(credentials=creds)
        project = GCP_PROJECT_ID or proj
        self.name = (
            f"projects/{project}/locations/{GCP_LOCATION}" \
            f"/processors/{GCP_PROCESSOR_ID}"
        )
        # Validate access by retrieving the processor metadata
        try:
            _ = self.client.get_processor(request={"name": self.name})
        except Exception as e:
            raise RuntimeError(f"Failed to validate Document AI processor access: {e}")

    def process(self, content: bytes, mime_type: str):
        """Sends content to Document AI and returns the resulting document object."""
        request = documentai.types.ProcessRequest(
            name=self.name,
            raw_document=documentai.types.RawDocument(
                content=content,
                mime_type=mime_type,
            ),
        )
        result = self.client.process_document(request=request)
        return result.document