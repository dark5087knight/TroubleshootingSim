#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import json

TREE_FILE = Path(__file__).parent / "tree.json"

def main():
    parser = argparse.ArgumentParser(
        prog="labctl",
        description="Linux Troubleshooting Simulator",
        add_help=True
    )

    # --- First argument MUST be the command ---
    parser.add_argument(
        "command",
        nargs="?",
        choices=["list", "show", "run", "sync"],  # added sync
        help="Command to execute: list, show, run, sync"
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


if __name__ == "__main__":
    main()
