"""
Dump video URLs from a list of videos.
"""

import sys

from pornhub_scraper import page_iterator

def dump_list(first_page):
    """
    Print out the video URLs from the given page.
    """
    for url in page_iterator(first_page):
        print(url)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python dump_list.py <first page>\n')
        sys.exit(0)
    dump_list(sys.argv[1])
