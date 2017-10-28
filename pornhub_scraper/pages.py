"""
APIs for going through pages of videos.
"""

from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

from .metadata import ScrapeError

def page_listing(page_url):
    """
    Get a list of video URLs from a page full of videos.

    Args:
      page_url: the URL of the page of videos.
        For example: https://www.pornhub.com/video

    Returns:
      A pair containing:
        urls: a list of video urls
        next_url: a URL to the next page, or None.

    Raises:
      ScrapeError: if the page is not structured as expected.
      request.exceptions.RequestException: if the request fails.
    """
    html = requests.get(page_url).text
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    container = soup.find('div', {'class': 'nf-videos'})
    if container is None:
        raise ScrapeError('could not find videos on page')
    for link in container.find_all('a'):
        if link.get('href') and 'view_video' in link.get('href'):
            urls.append(urljoin(page_url, link.get('href')))
    return urls, _find_next_url(page_url, soup)

def page_iterator(page_url):
    """
    List all videos starting at the given page.

    Args:
      page_url: the page URL to start at.
        For example: https://www.pornhub.com/video

    Returns:
      An iterator of video URLs.

    Raises:
      ScrapeError: if the page is not structured as expected.
      request.exceptions.RequestException: if a request fails.
    """
    while page_url is not None:
        urls, page_url = page_listing(page_url)
        for url in urls:
            yield url

def joint_page_iterator(page_urls, ignore_errors=False):
    """
    Iterate over listings from multiple starting pages.

    Produces URLs in a round-robin fashion, with a URL from the first page,
    then one from the second, etc. Goes through as many pages as possible for
    each URL.

    Returns:
      An iterator of video URLs.

    Raises:
      ScrapeError: if a page is not structured as expected.
      request.exceptions.RequestException: if a request fails.
    """
    listings = [([], u) for u in page_urls]
    while [l for l in listings if l[0] is not None]:
        for i, listing in enumerate(listings):
            if listing[1] is None:
                continue
            elif not listing[0]:
                if ignore_errors:
                    try:
                        listing = page_listing(listing[1])
                    except Exception: # pylint: disable=W0703
                        listing = ([], None)
                        continue
                listings[i] = listing
            yield listing[0][0]
            del listing[0][0]

def _find_next_url(base_url, soup):
    """
    Find the URL for the "next" button on a list page.

    Returns:
      The next URL, or None if no next button was found.
    """
    next_button = soup.find('li', {'class': 'page_next'})
    if next_button is None:
        return None
    next_link = next_button.find('a')
    if next_link is not None:
        return urljoin(base_url, next_link['href'])
    return None
