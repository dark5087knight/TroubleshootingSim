# engine/interactive.py
import shlex
import sys
import argparse
import json
from pathlib import Path

from engine.list import handle_list
from engine.show import handle_show
from engine.run import handle_run
from engine.sync import handle_sync  # optional if you want sync in interactive

# Path to tree.json (beside main.py, not inside engine/)
TREE_FILE = Path(sys.argv[0]).resolve().parent / "tree.json"

def print_help():
    print("""
Available commands:

  list [options]
    -l, --level [LEVEL]       List levels or sections
    -s, --section [SECTION]   List sections or scenarios
    --scenario                Include scenarios in listing (depth control)

  show --level L --section S --scenario X
    Show the problem description (problem.md)

  run --level L --section S --scenario X [--dry-run]
    Execute the scenario shell script

  sync
    Update the local tree.json from GitHub

Other commands:
  help, h       Show this help
  exit, quit    Exit interactive mode
""")

def build_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("command", choices=["list", "show", "run", "sync"])
    parser.add_argument("-l", "--level", nargs="?", const=True)
    parser.add_argument("-s", "--section", nargs="?", const=True)
    parser.add_argument("--scenario", nargs="?", const=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser

def run_interactive():
    print("\nlabctl interactive mode")
    print("Type 'help' or 'h' for help")
    print("Type 'exit' or Ctrl+C to quit\n")

    parser = build_parser()

    while True:
        try:
            raw = input("labctl> ").strip()

            if not raw:
                continue

            if raw in ("exit", "quit"):
                return

            if raw in ("help", "h"):
                print_help()
                continue

            tokens = shlex.split(raw)

            try:
                args = parser.parse_args(tokens)
            except SystemExit:
                print(" Invalid command or arguments. Type 'help'.")
                continue

            # --- Handle sync ---
            if args.command == "sync":
                handle_sync(args)
                continue

            # --- Handle list ---
            if args.command == "list":
                handle_list(args)
                continue

            # --- Handle show/run ---
            if args.command in ["show", "run"]:
                scenario_name = args.scenario

                if scenario_name is True or scenario_name is None:
                    print(" Error: --scenario (name) is required for show/run")
                    continue

                # Auto-detect level/section if missing
                if not args.level or not args.section:
                    try:
                        with open(TREE_FILE, "r") as f:
                            tree = json.load(f)
                    except FileNotFoundError:
                        print(f" tree.json not found at {TREE_FILE}. Please run 'sync' first.")
                        continue

                    found = False
                    for lvl_name, sections in tree.items():
                        for sec_name, scenarios in sections.items():
                            if scenario_name in scenarios:
                                if not args.level:
                                    args.level = lvl_name
                                if not args.section:
                                    args.section = sec_name
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        print(f" Scenario '{scenario_name}' not found in tree.json")
                        continue

                # Dispatch
                if args.command == "show":
                    handle_show(args)
                elif args.command == "run":
                    handle_run(args)

        except KeyboardInterrupt:
            print("\nExiting interactive mode.")
            return
