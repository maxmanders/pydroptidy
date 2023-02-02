import logging
import os
import sys

import dropbox

from pydroptidy import settings
from pydroptidy import tidy

LOG = logging.getLogger(__name__)


def lambda_handler(event, context):
    APP_KEY = os.getenv("DROPBOX_APP_KEY", None)
    APP_SECRET = os.getenv("DROPBOX_APP_SECRET", None)
    REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN", None)
    if APP_KEY is None or APP_SECRET is None or REFRESH_TOKEN is None:
        sys.exit("Set the Dropbox APP_KEY, APP_SECRET, REFRESH_TOKEN in the environment with DROPBOX_<VAR>")

    DRY_RUN = os.getenv("DRY_RUN", 'False').lower() in ('true', '1', 't')
    dropbox_client = dropbox.Dropbox(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        oauth2_refresh_token=REFRESH_TOKEN,
    )
    uploads = dropbox_client.files_list_folder(path=settings.UPLOADS_FOLDER)

    tidy.tidy(dropbox_client, uploads, DRY_RUN)
