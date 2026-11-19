# update-tickets

A Claude Code skill that updates Jira tickets after you deploy them.

For each ticket it:
1. Sets the **Environment** field (e.g. `UAT`) if it differs.
2. Moves the ticket to **Needs testing**.
3. Adds a comment: `Ticket status updated by <user>. Deployed on <UTC date> to <env>`.

## Install

Copy this folder to `<Phoenix-MarketDatabases>/.claude/skills/update-tickets/`.

The script imports `dbtools.bin.release_utils`, so it must live inside the repo. Python 3 must be installed. The skill installs the pip dependencies (`jira`, `pytz`) itself the first time.

## Use

In Claude Code, from the repo, just ask:

> update tickets AN-16916, AN-17576 to UAT

Claude will:
- install missing dependencies (first run only),
- ask which user you are (first run only, then remembered),
- confirm tickets and environment, then run the update and report each ticket.

Valid environments are the values of the Jira Environment field, such as `DEV`, `UAT` and `PROD`.

## Your user name

The name used in the comment is stored in `user.txt` in this folder (one line, e.g. `jperez`). To change it, say "change my default user to X" or edit the file. To use another name once, say "as X" in the request. Do not commit `user.txt`.

## Running it by hand

From the repo root, in PowerShell:

```powershell
python -m pip install -r dbtools/bin/requirements.txt
$env:PYTHONPATH = ".;dbtools/bin"
python .claude/skills/update-tickets/update_tickets.py --tickets "AN-16916, AN-17576" --env UAT --user jperez
```

Optional flags: `--fix-version <name>` and `--update-gallery true`. The gallery field id in the script is a placeholder (`customfield_12345`), so verify it before using that option.

## Troubleshooting

| Message | Meaning |
|---|---|
| `No transition found to 'Needs testing'` | The ticket's current status doesn't allow that transition. Move it manually. |
| `Failed to authenticate to JIRA` | Jira credentials from `dbtools/bin/refresh_utils.py` were rejected. |
| `ModuleNotFoundError: ddl_utils` | `dbtools/bin` is missing from `PYTHONPATH`. |
| `ModuleNotFoundError: pytz` / `jira` | Run the pip install command above. |

The script changes tickets in Jira and cannot undo them.
