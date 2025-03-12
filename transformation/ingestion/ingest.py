"""
Author : Arjun P
Modified on : 11/02
"""
import kaggle
from typing import List
from kaggle.api.kaggle_api_extended import KaggleApi

def download_data_source(kaggle_paths: List[str]) -> None:
    api = KaggleApi()
    api.authenticate()
    for kaggle_path in kaggle_paths: 
        try:
            api.dataset_download_files(kaggle_path,path='datasets',unzip=True)
            print(f"Downloaded and unzipped dataset: {kaggle_path}")
        except Exception as e:
            print(f"Failed to download {kaggle_path}: {e}")

