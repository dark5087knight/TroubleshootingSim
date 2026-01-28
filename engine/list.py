# list.py
import json
from pathlib import Path

main_path = Path(sys.argv[0]).resolve()  # resolves symlink
local_dir = main_path.parent              # directory where main.py actually lives
TREE_FILE = local_dir / "tree.json"

def handle_list(args):
    """
    Pretty list of levels, sections, and scenarios with depth control.
    """

    # Load the JSON tree
    with open(TREE_FILE, "r") as f:
        tree = json.load(f)

    # --- Helper to print scenarios ---
    def print_scenarios(scen_list, indent="        "):
        for i, scen in enumerate(scen_list, 1):
            print(f"{indent}└─ [{i}] {scen}")

    # --- Helper to print sections ---
    def print_sections(sections, show_scenarios=False):
        for i, (section_name, scenarios) in enumerate(sections.items(), 1):
            print(f"    ├─ [{i}] {section_name}")
            if show_scenarios:
                print_scenarios(scenarios, indent="        ")

    # --- Determine if we should show scenarios ---
    show_scenarios = args.scenario is True

    # --- No args → list everything ---
    if not args.level and not args.section and not show_scenarios:
        print("\n▶ All Levels, Sections, and Scenarios:\n")
        for i, (level_name, sections) in enumerate(tree.items(), 1):
            print(f"{i}. ▶ Level: {level_name}")
            print_sections(sections, show_scenarios=True)
        return

    # --- Only --level without value → list levels ---
    if args.level is True:
        print("\n▶ Levels:\n")
        for i, level_name in enumerate(tree.keys(), 1):
            print(f"  {i}. {level_name}")
        return

    # --- Only --section without value → list all sections grouped by level ---
    if args.section is True and not args.level:
        print("\n▶ Sections by Level:\n")
        for i, (level_name, sections) in enumerate(tree.items(), 1):
            print(f"{i}. ▶ Level: {level_name}")
            for j, section_name in enumerate(sections.keys(), 1):
                print(f"    {j}. {section_name}")
        return

    # --- Specific level ---
    if isinstance(args.level, str):
        if args.level not in tree:
            print(f"Error: Level '{args.level}' not found.")
            return
        level_data = tree[args.level]
        print(f"\n▶ Level: {args.level}")

        # --section without value → list sections of this level
        if args.section is True or (args.section is None and not show_scenarios):
            print("  Sections:")
            for i, section_name in enumerate(level_data.keys(), 1):
                print(f"    {i}. {section_name}")
            return

        # --specific section
        if isinstance(args.section, str):
            if args.section not in level_data:
                print(f"Error: Section '{args.section}' not found in level '{args.level}'.")
                return
            section_scenarios = level_data[args.section]
            print(f"  Section: {args.section}")
            if show_scenarios:
                print_scenarios(section_scenarios)
            else:
                print("    (Scenarios hidden. Use --scenario to list)")
            return

        # --scenario without specifying section → list all sections + scenarios in level
        if show_scenarios:
            print_sections(level_data, show_scenarios=True)
            return

    # --- Only --scenario without specifying level → list all scenarios under all sections/levels
    if show_scenarios and not args.level and not args.section:
        print("\n▶ All Levels with Scenarios:\n")
        for i, (level_name, sections) in enumerate(tree.items(), 1):
            print(f"{i}. ▶ Level: {level_name}")
            print_sections(sections, show_scenarios=True)
        return
