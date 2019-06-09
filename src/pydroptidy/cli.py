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
@click.option("--api-key", help="Dropbox API Key")
def run(dry_run, api_key):
    """
    Run via shell command line
    """

    API_KEY = os.getenv("DROPBOX_API_KEY", api_key)
    if API_KEY is None:
        sys.exit("Set the Dropbox API Key in the environment with DROPBOX_API_KEY, or use --api-key")

    DRY_RUN = os.getenv("DRY_RUN", dry_run)

    dropbox_client = dropbox.Dropbox(API_KEY)
    list_folder_result = dropbox_client.files_list_folder(path=settings.UPLOADS_FOLDER)
    tidy.tidy(dropbox_client, list_folder_result, DRY_RUN)
