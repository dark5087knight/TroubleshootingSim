# sync.py
import requests
import os
import sys
from pathlib import Path

# URL of the tree.json in the repo
TREE_JSON_URL = "https://raw.githubusercontent.com/dark5087knight/TroubleshootingScenarios/main/tree.json"
TREE_FILE = Path(__file__).parent.parent / "tree.json"
def handle_sync(args):
    """
    Sync the local tree.json with the latest version from GitHub,
    placing it in the same directory as main.py (not in engine/).
    """


    print("Syncing....")

    try:
        resp = requests.get(TREE_JSON_URL)
        resp.raise_for_status()
        tree_data = resp.text

        # Write to local tree.json
        with open(TREE_FILE, "w") as f:
            f.write(tree_data)

        print(f"updated successfully at: {TREE_FILE}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download tree.json: {e}")
        sys.exit(1)
