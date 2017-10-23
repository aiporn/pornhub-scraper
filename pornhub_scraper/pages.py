"""
APIs for going through pages of videos.
"""

from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

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
    for title in soup.find_all('span', {'class': 'title'}):
        link = title.find('a')
        if link is not None:
            urls.append(urljoin(page_url, link['href']))
    return urls, _find_next_url(page_url, soup)

def _find_next_url(base_url, soup):
    """
    Find the URL for the "next" button on a list page.

    Returns:
      The next URL, or None if no next button was found.
    """
    next_button = soup.find('li', {'class': 'page_next'})
    if next_button is None:
        print('no next button')
        return None
    next_link = next_button.find('a')
    if next_link is not None:
        return urljoin(base_url, next_link['href'])
    return None
