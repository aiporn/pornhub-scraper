"""
APIs for processing thumbnails.
"""

import re

from PIL import Image
import requests

from .metadata import ScrapeError

def main_thumbnail(metadata):
    """
    Fetch the main thumbnail for the video.

    Returns:
      A PIL image for the thumbnail.

    Raises:
      ScrapeError: if thumbnail meta-data is missing or invalid.
      request.exceptions.RequestException: if a request fails.
    """
    return _fetch_image(metadata['thumbnail'])

def video_thumbnails(metadata):
    """
    Fetch the thumbnails for the video.

    Args:
      metadata: an object returned by video_metadata().

    Returns:
      A chronologically-sorted iterable of pairs containing:
        timestamp: the offset of this thumbnail (in seconds).
        image: a PIL image for the thumbnail.

    Raises:
      ScrapeError: if thumbnail meta-data is missing or invalid.
      request.exceptions.RequestException: if a request fails.
    """
    thumbnail_data = metadata['thumbnails']
    try:
        frequency = int(thumbnail_data['samplingFrequency'])
        url_pattern = str(thumbnail_data['urlPattern'])
    except (KeyError, ValueError) as exc:
        raise ScrapeError('invalid thumbnail meta-data') from exc
    num_thumbs = metadata['duration'] // frequency
    thumb_idx = 0
    for grid in _fetch_thumbnail_grids(url_pattern):
        for thumbnail in _split_thumbnail_grid(grid):
            if thumb_idx >= num_thumbs:
                break
            thumb_idx += 1
            yield (thumb_idx*frequency, thumbnail)

def _fetch_thumbnail_grids(url_pattern):
    """
    Get an iterator over all the thumbnail grids.
    """
    idx_field = re.search('\\{([0-9]*)\\}', url_pattern)
    if idx_field is None:
        raise ScrapeError('invalid URL pattern')
    max_idx = int(idx_field.group(1))
    for idx in range(0, max_idx+1):
        url = url_pattern.replace(idx_field.group(0), str(idx))
        yield _fetch_image(url)

def _split_thumbnail_grid(image):
    """
    Get an iterator over all the sub-images in the image.
    """
    cols = 5
    rows = 5
    width = image.width // cols
    height = image.height // rows
    for row in range(rows):
        for col in range(cols):
            off_x, off_y = width*col, height*row
            yield image.crop((off_x, off_y, off_x+width, off_y+height))

def _fetch_image(url):
    """
    Fetch a PIL image.
    """
    req = requests.get(url, stream=True)
    img = Image.open(req.raw)
    img.load()
    return img
