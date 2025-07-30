import logging
import uuid
import os


logger = logging.getLogger('prod')


def post_thumbnail_upload_to(instance, filename):
    extension = os.path.splitext(filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{extension}"
    return os.path.join('post_thumbnails/', unique_filename)
