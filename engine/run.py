# engine/run.py
import requests
import subprocess
import tempfile
import os
import sys
import json
from pathlib import Path

REPO_OWNER = "dark5087knight"
REPO_NAME = "TroubleshootingScenarios"
BRANCH = "main"

main_path = Path(sys.argv[0]).resolve()  # resolves symlink
local_dir = main_path.parent              # directory where main.py actually lives
TREE_FILE = local_dir / "tree.json"

def handle_run(args):
    # Load the tree
    with open(TREE_FILE, "r") as f:
        tree = json.load(f)

    level = args.level
    section = args.section
    scenario = args.scenario
    dry_run = args.dry_run

    # --- Case 1: Full path provided ---
    if level and section and scenario:
        pass  # use as is

    # --- Case 2: Only scenario name provided ---
    elif scenario and (not level or not section):
        found = False
        for lvl_name, sections in tree.items():
            for sec_name, scenarios in sections.items():
                if scenario in scenarios:
                    if not level:
                        level = lvl_name
                    if not section:
                        section = sec_name
                    found = True
                    break
            if found:
                break
        if not found:
            print(f" Scenario '{scenario}' not found in tree.json")
            sys.exit(1)

    else:
        print(" Error: --scenario is required (and optionally --level/--section)")
        sys.exit(1)

    # Build relative path to shell script
    relative_path = f"scenarios/{level}/{section}/{scenario}/run.sh"
    raw_url = (
        f"https://raw.githubusercontent.com/"
        f"{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{relative_path}"
    )

    # Print header
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("▶ Running Scenario (Shell)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Level    : {level}")
    print(f"Section  : {section}")
    print(f"Scenario : {scenario}")
    print(f"Mode     : {'DRY RUN' if dry_run else 'EXECUTE'}\n")

    # Fetch script
    try:
        r = requests.get(raw_url, timeout=10)
        if r.status_code == 404:
            print(" Error: run.sh not found.")
            print(f"Expected path: {relative_path}")
            sys.exit(1)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(" Failed to fetch scenario script.")
        print(e)
        sys.exit(1)

    # Dry-run mode → just display script
    if dry_run:
        print("────────────── DRY RUN ──────────────")
        print("Script URL:")
        print(raw_url)
        print("\nScript Content:\n")
        print(r.text.rstrip())
        print("\n(No execution performed)")
        print("────────────────────────────────────")
        return

    # Execute shell script
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, "run.sh")
        with open(script_path, "w") as f:
            f.write(r.text)
        os.chmod(script_path, 0o755)

        print("────────────── EXECUTING ──────────────\n")
        try:
            subprocess.run(["bash", script_path], check=True)
        except subprocess.CalledProcessError as e:
            print("\n Scenario execution failed.")
            print(f"Exit code: {e.returncode}")
            sys.exit(e.returncode)

    print("\n✔ Scenario executed successfully.")
