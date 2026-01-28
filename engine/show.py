# engine/show.py
import requests
import sys
import json
from pathlib import Path

REPO_OWNER = "dark5087knight"
REPO_NAME = "TroubleshootingScenarios"
BRANCH = "main"

main_path = Path(sys.argv[0]).resolve()  # resolves symlink
local_dir = main_path.parent              # directory where main.py actually lives
TREE_FILE = local_dir / "tree.json"


def handle_show(args):
    # Load tree.json
    with open(TREE_FILE, "r") as f:
        tree = json.load(f)

    level = args.level
    section = args.section
    scenario = args.scenario

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

    # Build relative path to problem.md
    relative_path = f"scenarios/{level}/{section}/{scenario}/problem.md"
    raw_url = (
        f"https://raw.githubusercontent.com/"
        f"{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{relative_path}"
    )

    # Print header
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("▶ Scenario Problem Description")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    print(f"Level    : {level}")
    print(f"Section  : {section}")
    print(f"Scenario : {scenario}\n")

    # Fetch and print markdown
    try:
        response = requests.get(raw_url, timeout=10)
        if response.status_code == 404:
            print(" Error: problem.md not found.")
            print(f"   Expected path: {relative_path}")
            sys.exit(1)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(" Network error while fetching scenario.")
        print(f"   Details: {e}")
        sys.exit(1)

    # Print content
    print(f"────────────── {scenario} ──────────────\n")
    print(response.text.rstrip())
    print("\n────────────────────────────────────────\n")
