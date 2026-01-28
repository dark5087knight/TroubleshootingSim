#!/usr/bin/env python3
import requests
import json
import sys
import subprocess
from pathlib import Path
import tempfile
import shutil
import os

# --- GitHub repo ---
REPO_URL = "https://github.com/dark5087knight/TroubleshootingSim.git"
REPO_METADATA_URL = "https://raw.githubusercontent.com/dark5087knight/TroubleshootingSim/main/metadata.json"

# --- Local paths ---
MAIN_PATH = Path(sys.argv[0]).resolve()       # main.py path
LOCAL_DIR = MAIN_PATH.parent                  # directory where main.py actually lives
LOCAL_METADATA = LOCAL_DIR / "metadata.json"  # local metadata file

def handle_update(args):
    """
    Check if a newer version exists in GitHub and optionally update by
    cloning the repo and running install
    """
    # --- Load local metadata ---
    if not LOCAL_METADATA.exists():
        print(" Local metadata.json not found. Cannot determine current version.")
        sys.exit(1)

    with open(LOCAL_METADATA, "r") as f:
        local_meta = json.load(f)

    local_version = local_meta.get("version", "0.0.0")
    print(f" Current installed version: {local_version}")

    # --- Fetch remote metadata ---
    try:
        resp = requests.get(REPO_METADATA_URL)
        resp.raise_for_status()
        remote_meta = resp.json()
    except requests.RequestException as e:
        print(f" Failed to fetch remote metadata: {e}")
        sys.exit(1)

    remote_version = remote_meta.get("version", "0.0.0")
    print(f" Latest version on GitHub: {remote_version}")

    # --- Compare versions ---
    if local_version == remote_version:
        print(" Your LabCTL is up-to-date!")
        return

    print(f" A newer version is available: {remote_version}")
    choice = input("Do you want to update now? [y/N]: ").strip().lower()
    if choice != "y":
        print("Update cancelled.")
        return

    # --- Clone repo and run install.sh ---
    try:
        tmp_dir = tempfile.mkdtemp()
        print(f"🔄 Cloning repo into temporary folder: {tmp_dir}")
        subprocess.run(["git", "clone", "--depth", "1", REPO_URL, tmp_dir], check=True)

        install_script = Path(tmp_dir) / "install"
        if not install_script.exists():
            print(" install.sh not found in repo!")
            sys.exit(1)

        # Make executable
        os.chmod(install_script, 0o755)

        print(" Running installer...")
        subprocess.run([str(install_script)], check=True)

        print(" LabCTL has been updated successfully!")

    except subprocess.CalledProcessError as e:
        print(f" Update failed: {e}")
        sys.exit(1)

    finally:
        # Clean up temporary clone folder
        shutil.rmtree(tmp_dir, ignore_errors=True)
