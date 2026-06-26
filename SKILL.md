---
name: daily-report-generator
description: >-
  Extracts git commit history across all active workspaces for a specific author and time range, summarizing the work into a concise daily report.
---

# Daily Report Generator

## Overview
This skill automatically fetches the git commit history across all active workspaces for a specified time range, filtering by the user's name or email. It filters out merge commits, explicitly ignores any repositories with no commits, and uses an AI agent to structure the results into a concise daily report that can be directly used for daily standups or reporting.

## Dependencies
None.

## Quick Start
"帮我写一份今天（或者特定时间段）的日报"

## Utility Scripts

### `fetch_commits.js`
A Node.js helper script that iterates over multiple git repositories to fetch commit logs.

**Usage:**
```bash
node scripts/fetch_commits.js --author "hezhengxing" --since "midnight" --workspaces "C:\path\to\repo1" "C:\path\to\repo2" --output "results.json"
```

**Arguments:**
- `--author`: Filter by author name or email.
- `--since`: Start date/time (e.g., "midnight", "1.week.ago").
- `--until`: End date/time (optional).
- `--workspaces`: Space-separated list of absolute paths to workspace directories.
- `--output`: Output JSON file path.

## Workflow

1. **Identify User & Workspaces:** Determine the user's git author name/email (e.g., using `git config user.name`). Determine all active workspaces from your context.
2. **Execute Helper Script:** Run the `fetch_commits.js` script specifying the time range, author, workspaces, and a temporary output JSON path.
3. **Parse Output:** Read the JSON output. Any workspace missing from the output means there were no commits, so silently skip it.
4. **Generate Report:** Use the extracted commits to synthesize a professional, concise daily report (one point, one short sentence), categorized by project, and output it directly to the user in the chat window. **CRITICAL:** When stating the reporter/author name in the report, use the exact `git config user.name` value (e.g., `hezhengxing`), do NOT translate or infer a real name.

## Rate Limiting
N/A. This skill operates entirely on local git repositories.

## Common Mistakes
- **Forgetting to specify `--output`**: The script requires an output file and does not print JSON to stdout.
- **Merge Commits**: Make sure you rely on the script's default behavior, which automatically uses `--no-merges` to keep the report clean.
