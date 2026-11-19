# Skills

- `start-ticket/`: Phoenix-MarketDatabases ticket workflow. Paste an AN- ticket to get a branch from prod, three parallel design agents, a manifest, a dev deploy, tests and a PR.
  Install by copying the folder to `<Phoenix-MarketDatabases>/.claude/skills/start-ticket/`. `make_manifest.py` resolves the repo root from its own location, so it must live there.

- `update-tickets/`: Updates Jira tickets after a deployment (sets Environment, moves to "Needs testing", adds a comment). Installs its own dependencies and remembers your user name.
  Install by copying the folder to `<Phoenix-MarketDatabases>/.claude/skills/update-tickets/`. See its README.
