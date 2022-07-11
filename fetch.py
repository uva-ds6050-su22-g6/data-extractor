#!/usr/bin/env python

import time
import pandas as pd
from mediawikiapi import MediaWikiAPI
from mediawikiapi.exceptions import PageError


input_files = ('astronomy.txt', 'biology.txt', 'political-science.txt')

api_endpoint = MediaWikiAPI()

df = pd.DataFrame(columns=["topic", "uri", "categories", "summary", "content"])

for page_file in input_files:
    with open(page_file, 'r') as f:
        page_names = f.read().splitlines()
        print(f"Processing {page_file}")
        for page_name in page_names:
            print(f"-Downloading page {page_name}")
            page_obj = api_endpoint.page(page_name)
            # Process current page
            source = page_obj.url
            summary = page_obj.summary
            text = page_obj.content
            categories = page_obj.categories
            df.loc[len(df.index)] = [page_file, source, categories, summary, text]
            # Process degree 1
            for nested_link in page_obj.links:
                print(f"--Downloading page {nested_link}")
                try:
                    nestedpage_obj = api_endpoint.page(nested_link)
                    source = nestedpage_obj.url
                    summary = nestedpage_obj.summary
                    text = nestedpage_obj.content
                    categories = nestedpage_obj.categories
                    df.loc[len(df.index)] = [page_file, source, categories, summary, text]
                    time.sleep(2)
                except PageError:
                    print("---Page does not exist")
                    continue

df.to_feather("text_db.feather")
df.to_csv("text_db.csv")
