import os
import re
from icrawler.builtin import BingImageCrawler
from icrawler import ImageDownloader
from glob import glob

# Custom downloader with 3s timeout and 1 retry to avoid slow sites
class CustomImageDownloader(ImageDownloader):
    def download(self, task, default_ext, timeout=3, max_retry=1,
                 overwrite=False, **kwargs):
        return super().download(
            task, default_ext, timeout=timeout,
            max_retry=max_retry, overwrite=overwrite, **kwargs
        )

class MyBingCrawler(BingImageCrawler):
    def __init__(self, *args, **kwargs):
        super().__init__(downloader_cls=CustomImageDownloader, *args, **kwargs)

# Configuration
images_per_class = 1000  # max 1000 images per query (bing images is 1000 max)
root_dir = 'images'
input_txt_path = 'recycle_queries.txt' # query .txt file
query_suffix = " white background -clipart -illustration -drawing -cartoon -vector -icon -emoji" # extra keywords/filters for search engine

# Ensure root dir exists
os.makedirs(root_dir, exist_ok=True)

# Parse the input file
with open(input_txt_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

parent = None
sub = None
queries = []

for line in lines:
    line = line.strip()
    if not line or line.startswith('//'):  # skip empty or comment lines
        continue

    if line.startswith("##"): # main category
        parent = line[2:].strip()
    elif line.startswith("#"): # subcategory
        sub = line[1:].strip()
    else:
        queries.append((parent, sub, line))

# Download images per query
for parent, sub, query in queries:
    print(f"Scraping: {query}")
    class_name = query.replace(" ", "_")
    class_dir = os.path.join(root_dir,
                             parent.replace(" ", "_"),
                             sub.replace(" ", "_"),
                             query.replace(" ", "_"))

    os.makedirs(class_dir, exist_ok=True)

    crawler = MyBingCrawler(
        downloader_threads=4,
        storage={'backend': 'FileSystem', 'root_dir': class_dir}
    )

    full_query = query + query_suffix
    crawler.crawl(keyword=full_query, max_num=images_per_class)

    for idx, filepath in enumerate(sorted(glob(os.path.join(class_dir, "*")))):
        ext = os.path.splitext(filepath)[-1]
        new_name = f"{class_name}_{idx+1:06d}{ext}"
        os.rename(filepath, os.path.join(class_dir, new_name))
