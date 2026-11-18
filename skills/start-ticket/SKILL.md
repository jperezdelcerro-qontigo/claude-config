---
name: start-ticket
description: Start work on a Jira ticket in Phoenix-MarketDatabases. Use when the user pastes a ticket key or URL (AN-12345) or says "start ticket". Creates feature/AN-xxxxx from prod, runs 3 parallel solution-design agents, asks the user which solution to implement, then implements it and builds the deployment manifest.
---

# start-ticket

Input: a Jira key (`AN-12345`) or a browse URL. Extract the key; uppercase it.

## 1. Read the ticket
Use the Atlassian MCP (`getJiraIssue`, cloud `qontigo-cloud.atlassian.net`) for summary, description, acceptance criteria, comments and linked issues. If MCP is unavailable, ask the user to paste the ticket text.

## 2. Create the branch from prod
```bash
git status --porcelain            # untracked files are fine; stop and ask if tracked changes exist
git fetch origin --prune
git checkout -b feature/AN-xxxxx origin/prod --no-track
```
If the branch already exists locally or on origin, ask whether to reuse it. Never branch from the current HEAD. Prod is the base; back-ports to uat/devtest happen later via PRs.

### Commit identity (ask once)
Right after creating the branch, use `AskUserQuestion` once to ask which git user to commit as (name and email). Offer the current `git config user.name` / `user.email` as the first option. Store the answer repo-locally so it is never asked again, for this or later tickets:
```bash
git config --local user.name "<name>"
git config --local user.email "<email>"
```
If `git config --local user.name` and `user.email` are already set, skip the question. All commits in this flow use that identity.

## 3. Three design agents in parallel
Launch **three `Explore`/`general-purpose` agents in a single message** (read-only, no edits). Give each the full ticket text and a distinct angle:
1. **Minimal change**: smallest diff that satisfies the ticket (alter existing procs/tables only).
2. **Robust / data-safe**: handles edge cases, backfill of existing data, NULLs, idempotent re-runs, rollback; adds data/DDL scripts if needed.
3. **Consistency / reuse**: follows existing patterns in sibling objects, shared procs, naming; checks downstream consumers and other databases that reference the objects.

Each agent must return: affected objects (database, schema, name, type), files to change, data/DDL scripts needed, risks, test approach. Repo layout: stored procs/views/functions/tables live in `<Database>/<schema>/<Stored Procedures|Views|Functions|Tables>/*.sql`; one-off scripts in `dbtools/data_scripts/AN-xxxxx*.sql` and `dbtools/ddl_scripts/AN-xxxxx*.sql`.

## 4. Ask the user to choose
Summarise the three options side by side (scope, risk, files touched) with a recommendation, then use `AskUserQuestion`. Do not write code before the user picks. Allow "Other" to combine options.

## 5. Implement
Implement the chosen solution on the branch. Tests are written and run after the dev deploy (step 8).

## 6. Manifest (required)
Every change needs `dbtools/manifests/AN-xxxxx.xlsx`, listing every affected object. Generate it:
```bash
python .claude/skills/start-ticket/make_manifest.py AN-xxxxx rows.json
```
`rows.json` is a list of `[Database, Object Name, Object Type, Base Table or null, Schema]`. Object Type is one of: BCP_IN_FILE, DATA_SCRIPT, DDL_SCRIPT, DEFAULT_DATA_PROC, INDEX, STORED_PROC, TABLE, TRIGGER, TRIGGER_ON_VIEW, VIEW, FUNCTION. DATA_SCRIPT/DDL_SCRIPT names are the file name without `.sql` (they must exist, `dbtools/bin/cleanupManifests.py` checks). Cross-check that every changed `.sql` outside `dbtools/` has a manifest row and vice versa.

## 7. Deploy to dev (ask first)
Before wrapping up, use `AskUserQuestion` to ask whether to deploy the ticket to dev. If yes, ask whether they have a Python venv and its path (example: `C:\Users\JOSP\venv38`). Never assume a path. Then, from the repo root in PowerShell, activate it and deploy:
```powershell
<venv path>\Scripts\Activate.ps1

python dbtools/bin/deploy_sql.py --host dev-mac-db AN-xxxxx
```
If they have no venv, offer to create one (`python -m venv <path>` then `pip install -r dbtools/bin/requirements.txt`) before deploying. Report the deploy output faithfully, including failures. Commit first (with the step 2 identity) so the deployed state matches the branch.

## 8. Test on the same environment
Only after a successful deploy. Create `dbtools/data_scripts/AN-xxxxx_tests.sql`: self-checking T-SQL that returns one `PASS`/`FAIL` row per check, with a short description, for every object and behaviour changed (pattern: `AN-20947_tests.sql` on branch `feature/AN-20947`; it is not on prod yet). It must be non-destructive: no permanent data changes, and wrap any writes in a transaction that rolls back. Add it to the manifest as a `DATA_SCRIPT` row (regenerate the manifest) only if it should deploy; otherwise leave it out. Run it against **the same host the deploy used** (`dev-mac-db`), never another:
```powershell
sqlcmd -S dev-mac-db -E -b -i dbtools/data_scripts/AN-xxxxx_tests.sql
```
(Add `-U <user> -P <password>` instead of `-E` if the deploy used `--dbuser`.) Report every PASS/FAIL row faithfully. On any FAIL or SQL error, show the output, fix the code, redeploy, and rerun. Do not claim success until all checks pass.

## 9. Wrap up: PR, Jira status, link
Run only after every test check passed.
1. **Commit** with the identity chosen in step 2, as `AN-xxxxx => <description>` (include the tests file and manifest).
2. **Push and open the PR** against `prod` (the branch's base):
   ```bash
   git push -u origin feature/AN-xxxxx
   gh pr create --base prod --head feature/AN-xxxxx --title "(PROD) [AN-xxxxx] <description>" --body-file <body>
   ```
   Fill the body from `.github/pull_request_template.md`, replacing `PUT_JIRA_TICKET_ID` with `AN-xxxxx`, plus a short summary of the chosen solution, the objects in the manifest, and the dev deploy and test results. Back-ports to UAT/devtest use `(UAT)` and their own PRs, and are not part of this flow.
3. **Move the Jira ticket to Code Review.** Call `getTransitionsForJiraIssue` for the ticket, pick the transition whose target status is "Code Review" (match by name, case-insensitive), and apply it with `transitionJiraIssue`. If no such transition is available from the current status, do not guess another one: tell the user the transitions that are available.
4. **Send the PR link to the user** as the final message: the clickable PR URL, the branch name, and the Jira status now set. Report failures (push, PR, transition) faithfully instead of claiming completion.
