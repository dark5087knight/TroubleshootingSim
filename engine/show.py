# engine/show.py
import requests
import sys

REPO_OWNER = "dark5087knight"
REPO_NAME = "TroubleshootingSim"
BRANCH = "main"


def handle_show(args):
    level = args.level
    section = args.section
    scenario = args.scenario

    # Build relative path
    relative_path = f"scenarios/{level}/{section}/{scenario}/problem.md"

    # Build raw GitHub URL
    raw_url = (
        f"https://raw.githubusercontent.com/"
        f"{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{relative_path}"
    )

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("▶ Scenario Problem Description")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    print(f"Level    : {level}")
    print(f"Section  : {section}")
    print(f"Scenario : {scenario}\n")

    try:
        response = requests.get(raw_url, timeout=10)

        if response.status_code == 404:
            print("❌ Error: problem.md not found.")
            print(f"   Expected path: {relative_path}")
            sys.exit(1)

        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print("❌ Network error while fetching scenario.")
        print(f"   Details: {e}")
        sys.exit(1)

    # Print the markdown content as-is
    print(f"────────────── {scenario} ──────────────\n")
    print(response.text.rstrip())
    print("\n────────────────────────────────────────\n")
