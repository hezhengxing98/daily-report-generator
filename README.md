# Daily Report Generator Skill

A powerful AI agent skill that automatically extracts your git commits across multiple active workspaces and generates a concise, professional daily report (one point, one sentence).

## Features
- **Cross-Repository**: Automatically iterates over all your active code workspaces.
- **Merge-Commit Filtering**: Skips noisy `Merge pull request` or branch merge commits to keep your report clean.
- **Smart Pruning**: Automatically ignores any repositories with zero commits in your chosen time range.
- **One-Sentence Trigger**: Simply ask your AI assistant "Write a daily report for today" to execute the entire workflow.

## Installation

### Method 1: Global Installation (Recommended)
Clone this repository directly into your IDE's global skills directory (works for Qoder, Gemini, Antigravity, etc.).

```bash
# If using Qoder
cd ~/.qoder/config/skills/
git clone https://github.com/hezhengxing98/daily-report-generator.git

# If using Gemini/Antigravity
cd ~/.gemini/config/skills/
git clone https://github.com/hezhengxing98/daily-report-generator.git
```
Restart your AI IDE or open a new chat, and the skill will be automatically discovered!

### Method 2: Project-Level Installation
If you only want this skill available in a specific project, clone it into your project's `.agents` folder:

```bash
cd your-project-root/
mkdir -p .agents/skills/
cd .agents/skills/
git clone https://github.com/hezhengxing98/daily-report-generator.git
```

## Usage

Simply invoke the AI assistant in your chat window:
- *"帮我写一份今天的日报"* (Write a daily report for today)
- *"提取一下最近 3 天我在所有项目的提交总结"* (Extract my commit summaries for the last 3 days across all projects)

The agent will seamlessly execute the Node.js script to extract your pure commits, filter them, and present a structured summary in the chat window.

## Requirements
- An AI IDE supporting the standard `.agents` / `config/skills` extension protocol.
- `Node.js` installed on your machine (used by the helper script to execute the git commands).
