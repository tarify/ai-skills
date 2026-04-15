---
name: github
description: "Interact with GitHub using the `gh` CLI. Use `gh repo create` for creating repos, `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries."
---

# GitHub Skill

Use the `gh` CLI to interact with GitHub. Always specify `--repo owner/repo` when not in a git directory, or use URLs directly.

## Repositories

### Create a new repository

Create a public repository:
```bash
gh repo create my-repo --public --description "My project description"
```

Create a private repository:
```bash
gh repo create my-repo --private --description "My private project"
```

Create from local directory and push:
```bash
cd my-project
gh repo create my-repo --public --source=. --remote=origin --push
```

Create with specific settings:
```bash
gh repo create ai-skills \
  --public \
  --description "通用 AI 技能集合，支持 Codex、CodeBuddy 和 OpenClaw" \
  --source=. \
  --remote=origin \
  --push
```

### Clone a repository

```bash
gh repo clone owner/repo
git clone https://github.com/owner/repo.git
```

### View repository

```bash
gh repo view
gh repo view owner/repo --web  # Open in browser
```

## Pull Requests

Check CI status on a PR:
```bash
gh pr checks 55 --repo owner/repo
```

List recent workflow runs:
```bash
gh run list --repo owner/repo --limit 10
```

View a run and see which steps failed:
```bash
gh run view <run-id> --repo owner/repo
```

View logs for failed steps only:
```bash
gh run view <run-id> --repo owner/repo --log-failed
```

## Issues

List issues:
```bash
gh issue list --repo owner/repo
```

Create an issue:
```bash
gh issue create --title "Bug report" --body "Description"
```

## API for Advanced Queries

The `gh api` command is useful for accessing data not available through other subcommands.

Get PR with specific fields:
```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

## JSON Output

Most commands support `--json` for structured output.  You can use `--jq` to filter:

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```
