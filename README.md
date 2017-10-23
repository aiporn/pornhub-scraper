# pornhub-scraper

This is a tool for scraping thumbnails, "hotspots", and other meta-data from Pornhub videos.

# Usage

This requires Python 3.

Here's an example of how you might fetch all the thumbnails for a video:

```python
from pornhub_scraper import video_metadata, video_thumbnails

metadata = video_metadata('https://www.pornhub.com/view_video.php?viewkey=1604625352')
for timestamp, thumbnail in video_thumbnails(metadata):
    thumbnail.save(str(timestamp)+'.jpg')
```
