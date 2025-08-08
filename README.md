# RecycleImageDatasetWebScraper
Scrapes thousands of images of recyclable objects from web efficiently and quickly

**Note**
This tool is part of a larger project for creating a web-scraped image dataset for training YOLO models. The full project is available [on HuggingFace](https://huggingface.co/datasets/lreal/BingRecycle40k).

# How to use
You can either pip install icrawler or install the requirements.txt. As of now this repo uses Python 3.13.5, the latest Python version should work just fine though. It is reccomended you use a venv or conda.

```
pip install icrawler
```
or
```
pip install -r requirements.txt
```

# Query .txt file
The recycle_queries.txt file aims to create the most diverse recycle dataset possible, consisting of the main categories:
```
- plastic
- paper
- glass
- metal
```
There are over 200 total queries as well.

The file structure is as follows:
```
## Main category
# Subcategory
query1
query2
query3
...
```

# Scraper script
I did not add args to this script, so you will have to change the paths for the queries .txt file and the output directory in the script if desired. These can all be found in the configuration section of the script. The script also contains a query suffix to further filter and refine results for all searches.
```
python scraper.py
```

Configuration section:
```
# Configuration
images_per_class = 1000  # max 1000 images per query (bing images is 1000 max)
root_dir = 'images'
input_txt_path = 'recycle_queries.txt' # query .txt file
query_suffix = " white background -clipart -illustration -drawing -cartoon -vector -icon -emoji" # extra keywords/filters for search engine
```

# Post processing
Run this remove_duplicates.py script at the end which compares MD5 image hashes to find exact matches and keep only 1, takes param for the dataset directory
```
python remove_duplicates.py --dataset_dir images/
```
