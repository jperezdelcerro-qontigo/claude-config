---
name: update-tickets
description: Update Jira tickets after a deployment in Phoenix-MarketDatabases. Use when the user says "update tickets", "mark tickets deployed", or gives AN- keys plus an environment (DEV/UAT/PROD). Installs the Python dependencies if missing, asks who the user is (remembered afterwards), sets the Environment field, transitions to "Needs testing" and adds a "Deployed on <date> to <env>" comment.
---

# update-tickets

Run everything from the repo root (`git rev-parse --show-toplevel`).

## 1. Setup (automatic, idempotent)
Check the dependencies and install only what is missing:
```powershell
python -c "import jira, pytz" 2>$null; if ($LASTEXITCODE -ne 0) { python -m pip install -r dbtools/bin/requirements.txt }
```
If `python` is not found, tell the user to install Python 3 and stop. If pip fails, show the error and stop.

## 2. Who is the user?
The name goes into the Jira comment ("Ticket status updated by <user>").
- Read the saved name: `.claude/skills/update-tickets/user.txt` (single line). If it exists and is non-empty, use it silently and mention which user is being used.
- Otherwise ask once with `AskUserQuestion`. Offer, as first option, a guess derived from the git identity (`git config user.name`, e.g. first initial + surname lowercased, like `jperez`), plus "Other" for free text. Save the answer to `user.txt` so it is the default from then on.
- If the user says "as <someone else>" in the request, use that for this run only and do not overwrite `user.txt`. If they say to change their default, overwrite it.

## 3. Inputs
- **Tickets**: Jira keys (`AN-16916, AN-17576`), uppercased; commas and/or spaces accepted.
- **Environment**: value for the Jira Environment field (`DEV`, `UAT`, `PROD`). Never guess; ask if missing.

## 4. Run
This writes to Jira. Unless the user gave both tickets and environment explicitly, confirm them first.
```powershell
$env:PYTHONPATH = ".;dbtools/bin"; python .claude/skills/update-tickets/update_tickets.py --tickets "AN-16916, AN-17576" --env UAT --user <user>
```
(`dbtools/bin` must be on the path because `release_utils` imports sibling modules such as `ddl_utils`.)

For each ticket the script:
1. Sets Environment (`customfield_10056`) if different.
2. Transitions to **Needs testing**.
3. Comments `Ticket status updated by <user>. Deployed on <UTC date> to <env>`.

Optional flags: `--fix-version <name>` and `--update-gallery true` (the gallery field id in the script is a placeholder, `customfield_12345`; verify before using).

## 5. Report
Summarise the output per ticket (✅ / ℹ️ / ⚠️ / ❌). "No transition found" means the ticket's current state does not allow "Needs testing": tell the user, do not force it. If authentication fails, report it and do not try other credentials.
