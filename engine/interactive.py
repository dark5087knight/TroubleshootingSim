# engine/interactive.py
import shlex
import sys
import argparse

from engine.list import handle_list
from engine.show import handle_show
from engine.run import handle_run


def print_help():
    print("""
Available commands:

  list [options]
    --level [LEVEL]        List levels or sections
    --section [SECTION]   List sections or scenarios
    --senarios            Include scenarios in listing

  show --level L --section S --scenario X
    Show the problem description (problem.md)

  run --level L --section S --scenario X [--dry-run]
    Execute the scenario shell script

Other commands:
  help, h       Show this help
  exit, quit    Exit interactive mode
""")


def build_parser():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("command", choices=["list", "show", "run"])
    parser.add_argument("-l", "--level", nargs="?", const=True)
    parser.add_argument("-s", "--section", nargs="?", const=True)
    parser.add_argument("--senarios", action="store_true")
    parser.add_argument("--scenario")
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
                print("Bye 👋")
                return

            if raw in ("help", "h"):
                print_help()
                continue

            tokens = shlex.split(raw)

            try:
                args = parser.parse_args(tokens)
            except SystemExit:
                print("❌ Invalid command or arguments. Type 'help'.")
                continue

            # Dispatch
            if args.command == "list":
                handle_list(args)

            elif args.command == "show":
                if not args.level or not args.section or not args.scenario:
                    print("❌ show requires --level, --section, and --scenario")
                    continue
                handle_show(args)

            elif args.command == "run":
                if not args.level or not args.section or not args.scenario:
                    print("❌ run requires --level, --section, and --scenario")
                    continue
                handle_run(args)

        except KeyboardInterrupt:
            print("\nBye 👋")
            return
