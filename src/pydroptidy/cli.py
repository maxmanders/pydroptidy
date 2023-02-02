import logging
import os
import re
import sys

import click
import dropbox

from pydroptidy import settings
from pydroptidy import tidy

LOG = logging.getLogger(__name__)


@click.command()
@click.option(
    "--dry-run/--no-dry-run",
    default=False,
    help="whether or not to perform API actions",
)
def run(dry_run):
    """
    Run via shell command line
    """

    APP_KEY = os.getenv("DROPBOX_APP_KEY", None)
    APP_SECRET = os.getenv("DROPBOX_APP_SECRET", None)
    REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN", None)
    if APP_KEY is None or APP_SECRET is None or REFRESH_TOKEN is None:
        sys.exit("Set the Dropbox APP_KEY, APP_SECRET, REFRESH_TOKEN in the environment with DROPBOX_<VAR>")

    DRY_RUN = os.getenv("DRY_RUN", dry_run)

    dropbox_client = dropbox.Dropbox(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        oauth2_refresh_token=REFRESH_TOKEN,
    )
    dropbox_client.users_get_current_account()
    list_folder_result = dropbox_client.files_list_folder(path=settings.UPLOADS_FOLDER)
    tidy.tidy(dropbox_client, list_folder_result, DRY_RUN)
