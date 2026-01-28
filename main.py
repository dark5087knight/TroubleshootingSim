#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import json

# --- Determine paths ---
main_path = Path(sys.argv[0]).resolve()  # resolves symlink
local_dir = main_path.parent              # directory where main.py actually lives
TREE_FILE = local_dir / "tree.json"
META_FILE = local_dir / "metadata.json"  # metadata file beside tree.json

def print_version():
    """Read metadata.json and print version info"""
    if not META_FILE.exists():
        print("Metadata file not found!")
        return
    try:
        meta = json.loads(META_FILE.read_text())
        print(f"{meta.get('name', 'LabCTL')} v{meta.get('version', 'unknown')}")
    except Exception as e:
        print(f"Error reading metadata: {e}")

def main():
    parser = argparse.ArgumentParser(
        prog="labctl",
        description="Linux Troubleshooting Simulator",
        add_help=True
    )

    # --- Add --version argument ---
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show LabCTL version and metadata"
    )

    # --- First argument MUST be the command ---
    parser.add_argument(
        "command",
        nargs="?",
        choices=["list", "show", "run", "sync", "update"],  # added update
        help="Command to execute: list, show, run, sync, update"
    )

    # --- Context arguments ---
    parser.add_argument(
        "-l", "--level",
        nargs="?", const=True,
        help="Level name (beginner, intermediate, advanced) or just --level to list levels"
    )
    parser.add_argument(
        "-s", "--section",
        nargs="?", const=True,
        help="Section name (network, storage, services) or just --section to list sections"
    )
    parser.add_argument(
        "--scenario",
        nargs="?",       # optional value
        const=True,      # if no value is given → True (for list depth)
        help="For list: include scenarios; for show/run: scenario name"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview commands without executing"
    )

    args = parser.parse_args()

    # --- Handle version ---
    if args.version:
        print_version()
        sys.exit(0)

    # --- No command provided → launch interactive mode ---
    if not args.command:
        from engine.interactive import run_interactive
        run_interactive()
        sys.exit(0)

    # --- Dispatch based on command ---
    if args.command == "list":
        from engine.list import handle_list
        handle_list(args)

    elif args.command in ["show", "run"]:
        # For show/run, if --scenario provided but level or section missing, auto-detect from tree.json
        if args.scenario and args.scenario is not True:
            # Load tree.json
            with open(TREE_FILE, "r") as f:
                tree = json.load(f)

            level = args.level
            section = args.section
            scenario = args.scenario

            # Lookup scenario in tree if level/section missing
            if not level or not section:
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
                    print(f"❌ Scenario '{scenario}' not found in tree.json")
                    sys.exit(1)
                args.level = level
                args.section = section

        if args.command == "show":
            from engine.show import handle_show
            handle_show(args)
        elif args.command == "run":
            from engine.run import handle_run
            handle_run(args)

    elif args.command == "sync":
        # --- Sync command ---
        from engine.sync import handle_sync
        handle_sync(args)

    elif args.command == "update":
        # --- Update command ---
        from engine.update import handle_update
        handle_update(args)


if __name__ == "__main__":
    main()
