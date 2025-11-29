#!/usr/bin/env python3
import os
import shutil
import sys

if len(sys.argv) < 5:
    print("Usage: copy_built_extensions_to_repo.py <build_dir> <local_repo_dir> <ext_version> <platform>")
    sys.exit(1)

build_dir = sys.argv[1]
local_repo_dir = sys.argv[2]
ext_version = sys.argv[3]
platform = sys.argv[4]

dest_dir = os.path.join(local_repo_dir, ext_version, platform)
os.makedirs(dest_dir, exist_ok=True)

# Known outputs for tpch extension when built in-tree
candidates = [
    os.path.join(build_dir, 'extension', 'tpch', 'tpch.duckdb_extension'),
    os.path.join(build_dir, 'extension', 'tpch', 'libtpch_extension.a'),
    os.path.join(build_dir, 'extension', 'tpch', 'tpch.duckdb_extension.gz'),
]

copied = False
for src in candidates:
    if os.path.exists(src):
        # Preserve filename when copying into repo
        dest = os.path.join(dest_dir, os.path.basename(src))
        try:
            shutil.copy2(src, dest)
            print(f"Copied {src} -> {dest}")
            copied = True
        except Exception as e:
            print(f"Failed to copy {src} -> {dest}: {e}")

if not copied:
    print("No built tpch artifacts found in build directory")

sys.exit(0)
