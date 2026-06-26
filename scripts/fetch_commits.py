import argparse
import subprocess
import json
import os
import sys

def run_git_log(workspace, author, since, until):
    """Run git log in the specified workspace and return a list of commit messages."""
    if not os.path.isdir(workspace):
        return []
    
    # Check if it's a git repo
    git_dir = os.path.join(workspace, '.git')
    if not os.path.exists(git_dir):
        return []

    cmd = ['git', 'log', '--no-merges', '--pretty=format:%s']
    
    if author:
        cmd.extend(['--author', author])
    if since:
        cmd.extend(['--since', since])
    if until:
        cmd.extend(['--until', until])

    try:
        result = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if not output:
            return []
        
        # Split by newline and filter empty lines
        commits = [line.strip() for line in output.split('\n') if line.strip()]
        return commits
    except subprocess.CalledProcessError as e:
        # Silently catch git command failures (e.g. not a git repo, no commits)
        return []

def main():
    parser = argparse.ArgumentParser(description="Fetch git commits across multiple workspaces.")
    parser.add_argument('--author', type=str, help="Filter by author name or email (e.g., 'John Doe' or 'john@example.com')")
    parser.add_argument('--since', type=str, help="Start date/time (e.g., 'midnight', '2023-10-01')")
    parser.add_argument('--until', type=str, help="End date/time (e.g., 'now', '2023-10-31')")
    parser.add_argument('--workspaces', nargs='+', required=True, help="List of absolute paths to workspace directories")
    parser.add_argument('--output', type=str, required=True, help="Output JSON file path")
    
    args = parser.parse_args()
    
    report = {}
    
    for workspace in args.workspaces:
        # Use the folder name as the project identifier
        project_name = os.path.basename(os.path.normpath(workspace))
        commits = run_git_log(workspace, args.author, args.since, args.until)
        if commits:
            report[project_name] = commits
    
    # Write to output file
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Success! Data written to: {args.output}")
    except Exception as e:
        print(f"Error writing to output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
