"""
APIs for video meta-data.
"""

import json
import re

from bs4 import BeautifulSoup
import requests

class ScrapeError(Exception):
    """
    An exception thrown when scraping fails.
    """

def video_metadata(view_url):
    """
    Fetch meta-data about a particular video.

    Args:
      view_url: the URL to view the video.
        For example: https://www.pornhub.com/view_video.php?viewkey=abcdef.

    Returns:
      metadata: a dict containing the following keys:
        'id': unique identifier.
        'title': full video title.
        'duration': duration in seconds.
        'categories': list of category names.
        'views': number of views.
        'votes_up': number of upvotes.
        'votes_down': number of downvotes.
        'hotspots': a list of view counts at different parts of the video.
          May be None if the video does not count hotspots.
        'thumbnails': an object specifying how thumbnails are stored.

    Raises:
      ScrapeError: if the page is not structured as expected.
      request.exceptions.RequestException: if the request fails.
    """
    html = requests.get(view_url).text
    soup = BeautifulSoup(html, 'html.parser')
    flashvars, video_id = _find_flash_vars(soup)
    try:
        metadata = {
            'id': video_id,
            'title': flashvars['video_title'],
            'duration': int(flashvars['video_duration']),
            'thumbnails': flashvars['thumbs']
        }
        if 'hotspots' in flashvars:
            metadata['hotspots'] = flashvars['hotspots']
    except (KeyError, ValueError) as exc:
        raise ScrapeError('could not unpack flashvars') from exc
    metadata['categories'] = _find_categories(soup)
    metadata['views'] = _find_views(soup)
    metadata['votes_up'], metadata['votes_down'] = _find_votes(soup)
    return metadata

def _find_flash_vars(soup):
    """
    Decode the "flashvars" object from a parsed HTML page.

    Returns:
      A pair containing:
        flashvars: the decoded JSON object.
        video_id: the unique ID of the video.
    """
    expr = re.compile('var flashvars_([0-9]*) = (.*);\\s*\n')
    for script in soup.find_all('script'):
        contents = script.text
        match = expr.search(contents)
        if match is not None:
            return json.loads(match.group(2)), match.group(1)
    raise ScrapeError('could not find flashvars object')

def _find_categories(soup):
    """
    Find the video categories from a parsed HTML page.
    """
    element = soup.find('div', {'class': 'categoriesWrapper'})
    if element is None:
        raise ScrapeError('could not find categories')
    categories = []
    for link in element.find_all('a'):
        category = link.text.strip()
        if category != '+ Suggest':
            categories.append(category)
    return categories

def _find_views(soup):
    """
    Find the video view count from a parsed HTML page.
    """
    return _parse_counter(soup, 'count')

def _find_votes(soup):
    """
    Find the vote counts from a parsed HTML page.

    Returns:
      A pair containing:
        upvotes: number of upvotes
        downvotes: number of downvotes
    """
    return tuple(_parse_counter(soup, x) for x in ['votesUp', 'votesDown'])

def _parse_counter(soup, counter_class):
    """
    Parse the contents of a numerical field.
    """
    element = soup.find('span', {'class': counter_class})
    if element is None:
        raise ScrapeError('could not find count')
    try:
        return int(element.text.strip().replace(',', ''))
    except ValueError as exc:
        raise ScrapeError('could not parse count') from exc
