#!/usr/bin/env python3
import sys
import os
import urllib.request
import gzip
import shutil

if len(sys.argv) < 5:
    print("Usage: download_tpch_to_repo.py <local_repo_dir> <ext_version> <platform> <duckdb_version_number>")
    sys.exit(1)

local_repo_dir = sys.argv[1]
ext_version = sys.argv[2]
platform = sys.argv[3]
duckdb_version = sys.argv[4]

dest_dir = os.path.join(local_repo_dir, ext_version, platform)
os.makedirs(dest_dir, exist_ok=True)
dest_gz = os.path.join(dest_dir, 'tpch.duckdb_extension.gz')
dest = os.path.join(dest_dir, 'tpch.duckdb_extension')

urls = [
    f"https://extensions.duckdb.org/{ext_version}/{platform}/tpch.duckdb_extension.gz",
    f"https://extensions.duckdb.org/{duckdb_version}/{platform}/tpch.duckdb_extension.gz",
]

for url in urls:
    try:
        print(f"Trying download: {url}")
        urllib.request.urlretrieve(url, dest_gz)
        # decompress
        with gzip.open(dest_gz, 'rb') as f_in:
            with open(dest, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(dest_gz)
        print(f"Downloaded and installed tpch to {dest}")
        sys.exit(0)
    except Exception as e:
        print(f"Download failed for {url}: {e}")

print("tpch not available for the configured versions")
sys.exit(0)
