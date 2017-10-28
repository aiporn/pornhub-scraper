"""
Dump meta-data and thumbnails for a batch of videos.

Feed video URLs into this command as standard input.
"""

from hashlib import md5
import json
import os
import sys

from pornhub_scraper import main_thumbnail, video_metadata, video_thumbnails

def dump_data(output_dir):
    """
    Print out the video URLs from the given page.
    """
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    print('Reading URLs from stdin...')
    for url in sys.stdin:
        url = url.strip()
        if not url:
            continue
        out_path = os.path.join(output_dir, _hash_url(url))
        if os.path.exists(out_path):
            print('Skipping ' + url)
            continue
        print('Fetching ' + url)
        try:
            metadata = video_metadata(url)
            metadata['url'] = url
            os.mkdir(out_path)
            with open(os.path.join(out_path, 'metadata.json'), 'w') as mdfile:
                json.dump(metadata, mdfile)
            main_thumbnail(metadata).save(os.path.join(out_path, 'thumbnail.jpg'))
            for timestamp, thumbnail in video_thumbnails(metadata):
                thumb_name = 'thumbnail_' + str(timestamp) + '.jpg'
                thumbnail.save(os.path.join(out_path, thumb_name))
        except Exception as exc: # pylint: disable=W0703
            print('Error fetching %s: %s' % (url, str(exc)))

def _hash_url(url):
    """
    Generate a unique ID for the URL.
    """
    hasher = md5()
    hasher.update(bytes(url, 'utf-8'))
    return hasher.hexdigest()[:12]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python dump_data.py <output_dir>\n')
        sys.exit(0)
    dump_data(sys.argv[1])
