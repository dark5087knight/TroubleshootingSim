import requests

def print_tree(owner, repo, path="", max_depth=None, current_depth=0, indent=""):
    """
    Print GitHub repo folder tree up to max_depth levels.
    
    Args:
        owner (str): GitHub username or org
        repo (str): Repository name
        path (str): Path inside repo
        max_depth (int | None): Maximum depth to traverse (None = unlimited)
        current_depth (int): Internal recursion depth
        indent (str): String prefix for formatting
    """
    # Stop if max_depth reached
    if max_depth is not None and current_depth > max_depth:
        return
    
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url)
    resp.raise_for_status()
    items = resp.json()

    for item in items:
        print(f"{indent}{item['name']}")
        if item["type"] == "dir":
            # Recursively traverse subfolder
            print_tree(owner, repo, item["path"], max_depth, current_depth + 1, indent + "  ")

# Example usage
owner = "dark5087knight"
repo = "TroubleshootingSim"
start_path = "scenarios"
max_depth = 2  # Change this to 2, 3, None, etc.

print_tree(owner, repo, start_path, max_depth)
