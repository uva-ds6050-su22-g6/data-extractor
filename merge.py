#!/usr/bin/env python

import glob
import pandas as pd


df_merged = pd.DataFrame()

def read_cleanup_feather(filename):
    df = pd.read_feather(filename)
    df.drop_duplicates(subset=['uri'], inplace=True)
    return df

dfs = list(map(read_cleanup_feather, glob.glob("*.feather")))
df_merged = pd.concat(dfs, axis=0).reset_index()

df_merged.to_feather("dataset.feather")
df_merged.to_csv("dataset.csv")
