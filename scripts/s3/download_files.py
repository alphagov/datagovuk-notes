import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from os.path import isfile as exists

import boto3


_download_client = None


def _initialize_download_worker():
    global _download_client
    _download_client = boto3.client('s3')


def _download_file(bucket, key, file_path):
    if _download_client is None:
        raise RuntimeError("Download worker was not initialized")
    _download_client.download_file(Bucket=bucket, Key=key, Filename=file_path)


def download_s3_files_with_prefix(prefix, path="./downloads"):
    _bucket = 'govuk-production-aws-logging'
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(
        Bucket=_bucket,
        Prefix=f"s3/datagovuk-production-ckan-organogram/{prefix}",
    )
    workers = os.cpu_count() or 1
    with ProcessPoolExecutor(
        max_workers=workers,
        initializer=_initialize_download_worker,
    ) as executor:
        for page_counter, page in enumerate(pages, start=1):
            print(f"\nProcessing page {page_counter} for {prefix}")
            files = []
            scheduled_paths = set()
            for obj in page.get('Contents', []):
                name_file = obj.get("Key")
                file_path = path + "/" + name_file.split('/')[-1]
                if not exists(file_path) and file_path not in scheduled_paths:
                    files.append((_bucket, name_file, file_path))
                    scheduled_paths.add(file_path)

            futures = [executor.submit(_download_file, *file) for file in files]
            for counter, future in enumerate(as_completed(futures), start=1):
                future.result()
                print(f"\rProcessing objects {counter} / {len(files)}", end='', flush=True)
            if files:
                print()


def main():
    download_s3_files_with_prefix("2026-11-09")
    download_s3_files_with_prefix("2026-11-10")
    download_s3_files_with_prefix("2026-11-11")
    download_s3_files_with_prefix("2026-11-12")


if __name__ == "__main__":
    sys.exit(main())
