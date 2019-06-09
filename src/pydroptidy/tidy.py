import logging
import re

import dropbox

from pydroptidy import settings

LOG = logging.getLogger(__name__)


def tidy(dropbox_client, list_folder_result, dry_run):

    while True:
        process(dropbox_client, list_folder_result, dry_run)
        if list_folder_result.has_more:
            list_folder_result = dropbox_client.files_list_folder_continue(list_folder_result.cursor)
        else:
            break


def process(dropbox_client, list_folder_result, dry_run):
    for entry in list_folder_result.entries:

        LOG.info("Considering '{}'".format(entry.path_display))

        if isinstance(entry, dropbox.files.FolderMetadata):
            LOG.info("Skipping folder '{}'".format(entry.path_display))
            continue

        folder_matches = re.search(r"([0-9]{4}\-[0-9]{2})", entry.path_display)

        if folder_matches is None:
            LOG.info("Cannot extract traget folder name from '{}'".format(entry.path_display))
            continue

        folder = folder_matches[0]
        new_folder = "{}/{}".format(settings.UPLOADS_FOLDER, folder)
        new_path = "{}/{}".format(new_folder, entry.path_display.split("/")[-1:][0])

        LOG.info("Moving '{}' to '{}'".format(entry.path_display, new_path))

        if not dry_run:
            dropbox_client.files_move_v2(entry.path_display, new_path)
