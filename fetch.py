#!/usr/bin/env python

import time
import pandas as pd

from pathlib import Path

from mediawikiapi import MediaWikiAPI
from mediawikiapi.exceptions import PageError


input_folder = Path("./input_sources")
input_files = ('astronomy.txt', 'biology.txt', 'oceanography.txt', 'plantlife.txt', 'political-science.txt', 'sports.txt', 'state_and_war.txt')

api_endpoint = MediaWikiAPI()

df = pd.DataFrame(columns=["topic", "uri", "categories", "summary", "content"])

for page_file in input_files:
    with open(input_folder/page_file, 'r') as f:
        page_names = f.read().splitlines()
        print(f"Processing {page_file}")
        for page_name in page_names:
            print(f"-Downloading page {page_name}")
            try:
                page_obj = api_endpoint.page(page_name)
                # Process current page
                source = page_obj.url
                summary = page_obj.summary
                text = page_obj.content
                categories = page_obj.categories
                df.loc[len(df.index)] = [page_file, source, categories, summary, text]
            except Exception:
                print("Unknown exception")
                continue

            # Process degree 1
            print("Downloading nested page -", end=" ")
            for nested_link in page_obj.links:
                print(f"{nested_link}", end=", ")
                try:
                    nestedpage_obj = api_endpoint.page(nested_link)
                    source = nestedpage_obj.url
                    summary = nestedpage_obj.summary
                    text = nestedpage_obj.content
                    categories = nestedpage_obj.categories
                    df.loc[len(df.index)] = [page_file, source, categories, summary, text]
                    #time.sleep(2)
                except PageError:
                    continue
                except Exception:
                    print("Unknown exception, passing")
                    continue
            print("")
        df.to_feather(f"text_db.{page_file}.feather")
        df.to_csv(f"text_db.{page_file}.csv")
        df.drop(df.index,inplace=True) 
