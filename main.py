#!/usr/bin/env python3

import argparse
import sys

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
        choices=["list", "show", "run"],
        help="Command to execute: list, show, or run"
    )

    # --- Context arguments (optional depending on command) ---
    parser.add_argument("-l", "--level", help="Level name (beginner, intermediate, advanced)")
    parser.add_argument("-s", "--section", help="Section name (network, storage, services)")
    parser.add_argument("--scenario", help="Scenario name")
    parser.add_argument("--dry-run", action="store_true", help="Preview commands without executing")

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

    elif args.command == "show":
        from app.show import handle_show
        # scenario required for show
        if not args.level or not args.section or not args.scenario:
            print("Error: --level, --section, and --scenario are required for show")
            sys.exit(1)
        handle_show(args)

    elif args.command == "run":
        from app.run import handle_run
        # scenario required for run
        if not args.level or not args.section or not args.scenario:
            print("Error: --level, --section, and --scenario are required for run")
            sys.exit(1)
        handle_run(args)

if __name__ == "__main__":
    main()
