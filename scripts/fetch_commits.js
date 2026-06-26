const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function runGitLog(workspace, author, since, until) {
    if (!fs.existsSync(workspace) || !fs.statSync(workspace).isDirectory()) {
        return [];
    }

    const gitDir = path.join(workspace, '.git');
    if (!fs.existsSync(gitDir)) {
        return [];
    }

    const cmdArgs = ['git', 'log', '--no-merges', '--pretty=format:%s'];
    if (author) cmdArgs.push('--author', `"${author}"`);
    if (since) cmdArgs.push('--since', `"${since}"`);
    if (until) cmdArgs.push('--until', `"${until}"`);

    try {
        const output = execSync(cmdArgs.join(' '), { cwd: workspace, stdio: ['pipe', 'pipe', 'pipe'] }).toString().trim();
        if (!output) return [];
        return output.split('\n').map(line => line.trim()).filter(line => line);
    } catch (e) {
        return [];
    }
}

function main() {
    const args = process.argv.slice(2);
    let author = '', since = '', until = '', output = '';
    const workspaces = [];

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--author') author = args[++i];
        else if (args[i] === '--since') since = args[++i];
        else if (args[i] === '--until') until = args[++i];
        else if (args[i] === '--output') output = args[++i];
        else if (args[i] === '--workspaces') {
            i++;
            while (i < args.length && !args[i].startsWith('--')) {
                workspaces.push(args[i]);
                i++;
            }
            i--;
        }
    }

    if (!output || workspaces.length === 0) {
        console.error('Error: --output and --workspaces are required.');
        process.exit(1);
    }

    const report = {};

    for (const workspace of workspaces) {
        const projectName = path.basename(path.resolve(workspace));
        const commits = runGitLog(workspace, author, since, until);
        if (commits.length > 0) {
            report[projectName] = commits;
        }
    }

    try {
        fs.writeFileSync(output, JSON.stringify(report, null, 2), 'utf8');
        console.log(`Success! Data written to: ${output}`);
    } catch (e) {
        console.error(`Error writing to output file: ${e.message}`);
        process.exit(1);
    }
}

main();
