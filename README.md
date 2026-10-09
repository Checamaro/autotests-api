# API Course Automation Tests

[![API tests](https://github.com/Checamaro/autotests-api/actions/workflows/tests.yml/badge.svg)](https://github.com/Checamaro/autotests-api/actions/workflows/tests.yml)
[![Allure Report](https://img.shields.io/badge/report-Allure-orange)](https://checamaro.github.io/autotests-api/)

This project implements automated tests for
the [API Course Test Server](https://github.com/Nikita-Filonov/qa-automation-engineer-api-course) (an LMS REST API).
The tests are written using **Python**, **Pytest**, **Allure**, **Pydantic**, **Faker** and **HTTPX**.

On top of the classic test framework the project runs an **AI-assisted QA workflow** built on
[Claude Code](https://claude.com/claude-code): AI agents analyse the API, design test cases in a TMS,
write autotests, open pull requests and triage failed CI runs — with a human approving every step.
See [AI-assisted QA workflow](#ai-assisted-qa-workflow).

## Project Overview

The goal of this project is to automate the testing of the API Course server, focusing on REST API testing.
The project incorporates best practices such as:

- API clients for structured interaction with endpoints;
- Pytest fixtures for reusable and maintainable test setups;
- Pydantic models for strict data validation;
- JSON Schema validation to ensure API contract correctness;
- Fake data generation to simulate real-world scenarios;
- Test cases managed in **Qase** and linked to autotests;
- Bugs tracked in **GitHub Issues** and linked to tests via `xfail(strict=True)`;
- CI on **GitHub Actions** with an Allure report published to **GitHub Pages**;
- AI agents for test design, automation and failure triage.

## Tech Stack

| Area | Tools |
|---|---|
| Tests | Python 3.12, pytest, pytest-xdist, pytest-rerunfailures |
| HTTP & data | HTTPX, Pydantic v2, pydantic-settings, jsonschema, Faker |
| Reporting | Allure (allure-pytest), GitHub Pages |
| Test management | [Qase](https://qase.io) (Free plan) + `qase-pytest` |
| Bug tracking | GitHub Issues |
| CI | GitHub Actions |
| AI | Claude Code, subagents, Qase MCP server, `anthropics/claude-code-action` |

## Project Structure

```
autotests-api/
├─ clients/            # API clients and Pydantic request/response schemas, one package per entity
├─ fixtures/           # pytest fixtures (users, files, courses, exercises, auth, allure)
├─ tests/              # tests grouped by entity
├─ tools/
│  ├─ assertions/      # assert_* helpers, each wrapped in an Allure step
│  ├─ allure/          # Allure epics / features / stories / tags
│  ├─ ai/              # summarize_allure.py — compact failure summary for AI triage
│  ├─ fakers.py, routes.py, logger.py
├─ docs/
│  ├─ test-cases/      # test case drafts with Qase IDs and automation status
│  └─ ai-metrics.md    # AI workflow metrics
├─ templates/          # test case and bug report templates used by agents
├─ .claude/            # Claude Code: agents, skills, permissions
├─ .mcp.json           # MCP servers (Qase)
├─ CLAUDE.md           # project rules for AI agents
├─ AI_SETUP.md         # step-by-step setup of the AI workflow
└─ .github/workflows/  # tests.yml (CI) and ai-triage.yml (AI failure triage)
```

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Checamaro/autotests-api.git
cd autotests-api
```

### Start the Test Server

Clone the server next to this repository (the AI analyst agent reads its source code from
`../qa-automation-engineer-api-course`):

```bash
git clone https://github.com/Nikita-Filonov/qa-automation-engineer-api-course.git ../qa-automation-engineer-api-course
```

Install its dependencies and start it on `http://localhost:8000` with the environment variables used in
[`.github/workflows/tests.yml`](.github/workflows/tests.yml) (`APP_HOST`, `DATABASE_URL`, `JWT_*`).
Swagger UI: http://localhost:8000/docs.

### Create a Virtual Environment

#### Linux / MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Tests

Run the regression suite in parallel and collect Allure results:

```bash
pytest -m regression --alluredir=./allure-results -n 2
```

Run tests for one entity using markers: `pytest -m courses`
(available markers: `users`, `files`, `courses`, `exercises`, `authentication`, `regression`).

### Sending Results to Qase

```bash
export QASE_MODE=testops
export QASE_TESTOPS_PROJECT=LMS
export QASE_TESTOPS_API_TOKEN=<your token>
pytest -m regression
```

Tests are linked to Qase cases with `@qase.id(N)`; the case ID is also shown in the Allure title (`[LMS-N] ...`).

### Viewing the Allure Report

```bash
allure serve allure-results
```

The report from every CI run on `main` is published to
[GitHub Pages](https://checamaro.github.io/autotests-api/) with history.

## CI

[`tests.yml`](.github/workflows/tests.yml) runs on every push and pull request to `main`:

1. starts the test server inside the runner;
2. runs `pytest -m regression` in 2 workers;
3. uploads `allure-results` as an artifact;
4. builds the Allure report with history and deploys it to GitHub Pages.

If the run fails, [`ai-triage.yml`](.github/workflows/ai-triage.yml) starts automatically (see below).

---

## AI-assisted QA workflow

### The idea

Routine QA work — reading the API contract, enumerating test cases, writing boilerplate tests,
sorting out red CI runs — is delegated to AI agents. The engineer acts as a reviewer and decision maker:
nothing is created in Qase, GitHub Issues or `main` without explicit approval.

```
                 /qa-pipeline <entity>
                          │
   ┌──────────────────────▼───────────────────────┐
   │ 1. requirements-analyst                      │  OpenAPI + server code → contract,
   │                                              │  business rules, risks, coverage gaps
   ├──────────────────────────────────────────────┤
   │ 2. test-designer                 ──► Qase    │  test design techniques → cases (after approval)
   ├──────────────────────────────────────────────┤
   │ 3. autotest-writer               ──► PR      │  pytest tests in project style, green run,
   │                                              │  branch ai/<entity>-…, pull request
   └──────────────────────┬───────────────────────┘
                          ▼
              GitHub Actions: API tests
                          │ failed?
                          ▼
   ┌──────────────────────────────────────────────┐
   │ 4. AI triage (ai-triage.yml / run-triager)   │  BUG / TEST / ENV / FLAKY,
   │                                  ──► Issues  │  bug reports, suggested fixes
   └──────────────────────────────────────────────┘
```

### Agents

| Agent | File | What it does | Writes to |
|---|---|---|---|
| requirements-analyst | [`.claude/agents/requirements-analyst.md`](.claude/agents/requirements-analyst.md) | Reads OpenAPI and server code, describes the contract and business rules, finds risks and coverage gaps | — (read only) |
| test-designer | [`.claude/agents/test-designer.md`](.claude/agents/test-designer.md) | Designs cases (equivalence classes, boundary values, decision tables, auth negatives), saves drafts to `docs/test-cases/` | Qase (after approval) |
| autotest-writer | [`.claude/agents/autotest-writer.md`](.claude/agents/autotest-writer.md) | Writes tests and missing clients/fixtures/assertions, runs them until green, stops on contract violations instead of "fixing" the test | Git branch + PR (after approval) |
| run-triager | [`.claude/agents/run-triager.md`](.claude/agents/run-triager.md) | Classifies failures of a local or CI run, groups them by root cause, drafts bug reports | GitHub Issues (after approval) |

### Commands

Run inside `claude` in the project root:

| Command | Purpose |
|---|---|
| `/qa-pipeline <entity or endpoint>` | Full pipeline: analysis → cases → autotests → run → triage, with a stop after each step |
| `/bug-report <description>` | Reproduce, fill [`templates/bug.md`](templates/bug.md), check duplicates, create an issue |
| `Use run-triager for the last CI run` | Download the CI artifact and triage it locally |

### AI triage in CI

[`ai-triage.yml`](.github/workflows/ai-triage.yml) is triggered by `workflow_run` when **API tests** fails:

1. downloads `allure-results` of the failed run;
2. builds a compact summary with [`tools/ai/summarize_allure.py`](tools/ai/summarize_allure.py)
   (failed step, message, end of the trace, curl attachment);
3. runs Claude via `anthropics/claude-code-action` with a restricted tool list;
4. Claude classifies every failure, files new bugs (or comments on duplicates) and creates one
   **"AI triage of run #N"** issue with a summary table and suggested fixes.

### Guardrails

- [`CLAUDE.md`](CLAUDE.md) holds the project conventions, so generated code matches the existing style.
- [`.claude/settings.json`](.claude/settings.json) allows tests and read-only git/gh commands; `git push`,
  `gh pr create` and `gh issue create` always ask for confirmation; force push, pushing to `main` and `rm -rf` are denied.
- Tokens (`QASE_API_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN`) live in environment variables and GitHub Secrets only.
- A test that fails because of a confirmed server bug is marked `@pytest.mark.xfail(reason="#<issue>", strict=True)`:
  the suite stays green, and the test turns red as soon as the bug is fixed.
- Every AI change goes through a pull request and human code review.

### Results so far

| Entity | Cases in Qase | Autotests | Bugs found |
|---|---|---|---|
| courses | 71 (LMS-1 … LMS-71) | 73 (was 3) | 5 — issues [#1](https://github.com/Checamaro/autotests-api/issues/1)–[#5](https://github.com/Checamaro/autotests-api/issues/5) |

Bugs found by the agents include updating and deleting another user's course, updating a non-existent course,
accepting `title = null` on update and course deletion not removing its exercises.
Detailed metrics are collected in [`docs/ai-metrics.md`](docs/ai-metrics.md).

### Setting it up

Full step-by-step instructions (Windows): [`AI_SETUP.md`](AI_SETUP.md). In short:

1. Install Claude Code, GitHub CLI, Node.js; run `gh auth login`.
2. Create a Qase project `LMS`, set `QASE_API_TOKEN` in the environment.
3. Run `claude` in the project root, approve the `qase` MCP server, check `/mcp` and `/agents`.
4. For CI triage: `claude setup-token` and `gh secret set CLAUDE_CODE_OAUTH_TOKEN`.
