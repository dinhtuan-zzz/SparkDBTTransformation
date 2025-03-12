"""
Author : Arjun P
Modified on : 11/02
"""

from .ingest import download_data_source
from .utils import traverse_folder, ingest_spark

if __name__ == '__main__':
    download_data_source(
        kaggle_paths = ['hellbuoy/car-price-prediction']
    )
    files = traverse_folder(
        dir = 'datasets'
    )

    ingest_spark(
        files=files
    )

    
