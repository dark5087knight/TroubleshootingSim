# engine/run.py
import requests
import subprocess
import tempfile
import os
import sys

REPO_OWNER = "dark5087knight"
REPO_NAME = "TroubleshootingSim"
BRANCH = "main"


def handle_run(args):
    level = args.level
    section = args.section
    scenario = args.scenario
    dry_run = args.dry_run

    relative_path = f"scenarios/{level}/{section}/{scenario}/run.sh"
    raw_url = (
        f"https://raw.githubusercontent.com/"
        f"{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{relative_path}"
    )

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("▶ Running Scenario (Shell)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Level    : {level}")
    print(f"Section  : {section}")
    print(f"Scenario : {scenario}")
    print(f"Mode     : {'DRY RUN' if dry_run else 'EXECUTE'}\n")

    try:
        r = requests.get(raw_url, timeout=10)

        if r.status_code == 404:
            print("❌ Error: run.sh not found.")
            print(f"Expected path: {relative_path}")
            sys.exit(1)

        r.raise_for_status()

    except requests.exceptions.RequestException as e:
        print("❌ Failed to fetch scenario script.")
        print(e)
        sys.exit(1)

    if dry_run:
        print("────────────── DRY RUN ──────────────")
        print("Script URL:")
        print(raw_url)
        print("\nScript Content:\n")
        print(r.text.rstrip())
        print("\n(No execution performed)")
        print("────────────────────────────────────")
        return

    # Write and execute shell script
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, "run.sh")

        with open(script_path, "w") as f:
            f.write(r.text)

        os.chmod(script_path, 0o755)

        print("────────────── EXECUTING ──────────────\n")

        try:
            subprocess.run(
                ["bash", script_path],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print("\n❌ Scenario execution failed.")
            print(f"Exit code: {e.returncode}")
            sys.exit(e.returncode)

    print("\n✔ Scenario executed successfully.")
