"""
Dump video URLs from all the categories.
"""

from pornhub_scraper import joint_page_iterator

def dump_categories():
    """
    Print out the video URLs from the given page.
    """
    for url in joint_page_iterator(category_urls()):
        print(url)

def category_urls():
    """
    Get all the category URLs.
    """
    return ['https://www.pornhub.com/video?c='+str(i) for i in range(1, 106)]

if __name__ == '__main__':
    dump_categories()
