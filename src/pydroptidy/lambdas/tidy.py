import logging
import os
import sys

import dropbox

from pydroptidy import settings
from pydroptidy import tidy

LOG = logging.getLogger(__name__)


def lambda_handler(event, context):
    API_KEY = os.getenv("DROPBOX_API_KEY", None)
    if API_KEY is None:
        sys.exit("Set the Dropbox API Key in the environment with DROPBOX_API_KEY, or use --api-key")

    DRY_RUN = os.getenv("DRY_RUN", False)

    dropbox_client = dropbox.Dropbox(API_KEY)
    uploads = dropbox_client.files_list_folder(path=settings.UPLOADS_FOLDER)

    tidy.tidy(dropbox_client, uploads, DRY_RUN)
