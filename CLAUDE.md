# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Test Convention (Given / When / Then)

**Every test you add must be structured with `# given`, `# when`, `# then` comments.**

```python
def test_rejects_negative_price():
    # given
    trade = Trade(price=-1)

    # when
    result = validate(trade)

    # then
    assert not result.is_valid
```

- One behavior per test; name it after the behavior.
- Use the same three comment markers in any language (`//` instead of `#` where needed).
- Don't rewrite existing tests to this format unless asked.

## 6. Python Style (PEP 8)

**Follow PEP 8 (https://peps.python.org/pep-0008/) for all new Python code, with one exception: no underscore-prefixed names.**

- Never create functions, methods, or attributes whose names start with an underscore (`_helper`, `_internal`). Private is not a Python concept; give them normal public names.
- Required dunder methods (`__init__`, `__str__`, etc.) are fine.
- This overrides PEP 8's recommendation to prefix non-public names with `_`.
- Don't rename existing underscore-prefixed names unless asked.
- Match the repo's existing formatting for untouched code (surgical changes still apply).

## 7. Commit Messages

**Format: `<ticket number> => <what the commit does>`**

Example: `AN-2365 => Adding new feature`

- Ticket number comes first (e.g. `AN-2365`), then ` => `, then a short description.
- Take the ticket from the branch name if it contains one; otherwise ask me. Never invent a ticket number.
- Don't commit or push unless I ask.

## 8. Python Environment Lookup (per repo)

**Before running any Python, pip, or test command, find the current repo's folder name in the table below and activate its venv in PowerShell first.**

| Repo (folder name) | Activate command | PYTHONPATH needed? |
|---|---|---|
| Phoenix-MarketDatabases | `C:\Users\JOSP\venv38\Scripts\Activate.ps1` | No |
| Phoenix-Python | `C:\Users\JOSP\Phoenix-Python\.venvPhoenix\Scripts\Activate.ps1` | Yes: `$env:PYTHONPATH = "C:\Users\JOSP\Phoenix-Python;C:\Users\JOSP\Cassandra-MarketDB;C:\Users\JOSP\Cassandra-RiskModels"` |
| ContentDev-MAC | `C:\Users\JOSP\ContentDev-MAC\venvmac\Scripts\Activate.ps1` | No |
| DerivedCurves | `C:\Users\JOSP\DerivedCurves\venvcc\Scripts\Activate.ps1` | No |
| data-platform-api | `.\.venv\Scripts\activate` (venv inside the repo; Poetry project for dependencies). Run locally: `python -m uvicorn src.api.main:app --reload --host localhost --env-file .env` | No - pytest sets `pythonpath = ["src", "."]` in `packages\data-platform-py` |
| Dataplatform | No venv found - ask | No |
| Other repos (Cassandra-*, Phoenix-Main, Phoenix-Research*, GraphRisk, ...) | No venv found - ask | No |

Only Phoenix-Python needs PYTHONPATH. Set it per session in PowerShell, not permanently.

Shared venvs in `C:\Users\JOSP\`: `venv38` (Python 3.8), `venvscripts` and `venv_deploy_utils` (Python 3.13).

- Match by repo folder name (case-insensitive, partial match is fine).
- If the repo isn't listed, ask which venv to use. Don't create a new venv or install packages globally.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
