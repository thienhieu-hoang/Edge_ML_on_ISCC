# Project Master Guidelines

## 1. Project Architecture & Directory Layout
- **Project Root**: `<absolute_path_to_project>`
- **Source Code (Team Sync)**: `./src`
- **Research Notes & Worklogs (Private)**: `./_note`
- **Execution Plans & Task Queue (Private)**: `./_plan`
- **Agent Directives & System Rules**: `./.agent/rules`

### 💡 Project Directory Structure
To enable parallel agent experimentation, shift-based execution, and conflict-free Git synchronization, the repository is organized as follows:

```text
MyProject/
├── .agent/
│   └── rules/                            # Autonomous agent directives & protocols
│       ├── main.md                       # Master index & routing (this file)
│       ├── note_folder_organize_wSubtree.md # Git Subtree dual-remote guide
│       ├── autoAgentFlow/                # Multi-agent, task queue & plan rules
│       ├── LiteratureReviewFlow/         # Academic retrieval & citation rules
│       └── takeWorkLogFlow/              # Worklog & metric formatting rules
├── .git/                                 # Single local Git repository with dual remotes
├── src/                 # Pure source code (synced to Collab repo)
│   ├── core/            # Shared foundation: dataloaders, metrics
│   ├── approaches/      # Modular candidate approaches
│   └── run.py           # Master runner script
├── _note/               # Private research notes
│   ├── helperWorklog/   # Detailed per-run traces (details_yymmdd-hhmm.md)
│   └── WORKLOG.md       # Executive benchmark summaries
├── _plan/               # Private experimental roadmaps (2-round workflow)
│   ├── PLAN1.md
│   └── PLAN2.md
├── .gitignore           # Ignores large binaries (*.pt, *.mat), NOT src/
└── README.md
```

> **Golden Rule**: Whenever developing or testing a new method, agents/developers **must create a dedicated subfolder under `src/approaches/<approach_name>/`** with its own `results/` folder. Never overwrite files in another approach's folder. When merging experimental branches into `main`, Git will add the new folder seamlessly with zero merge conflicts.

---

## 2. Git Subtree Architecture (Dual Remotes)

The repository maintains **a single local working directory** on your machine synchronized with **two independent remote repositories** on GitHub (as detailed in [`note_folder_organize_wSubtree.md`](./note_folder_organize_wSubtree.md)):

```
[GitHub Collab (Team)]                                     [GitHub Personal (Private)]
https://github.com/lab/collab.git                          https://github.com/you/private.git
(Contains ONLY code from src/)                             (Contains EVERYTHING: _note/ + _plan/ + src/)
          ▲                                                          ▲
          │                                                          │
          │ git push-collab (Subtree)                                │ git push (Default)
          │                                                          │
          └──────────────────────────┬───────────────────────────────┘
                                     │
                      [SINGLE LOCAL REPOSITORY ON DISK]
                      MyProject/
```

### A. One-Time Setup Commands
```bash
git init
git remote add origin https://github.com/you/my_project_private.git
git remote add collab https://github.com/lab/collab_project.git
git subtree add --prefix=src collab main
git push -u origin main

# Configure shortcuts
git config alias.pull-collab "subtree pull --prefix=src collab main"
git config alias.push-collab "subtree push --prefix=src collab main"
```

### B. Daily Command Reference
- **Morning (Pull Team Updates)**:
  `git pull-collab`
- **Throughout the Day (Local Commits)**:
  Commit freely on local disk without worrying about remotes:
  `git add . && git commit -m "feat/docs: concise explanation"`
- **Backup Everything to Personal GitHub**:
  `git push` *(Bare `git push` defaults strictly to `origin/main` — 100% safe, never pushes to collab).*
- **Push Code to Team/Lab (End of Day / Verified Milestones)**:
  `git push-collab` *(Subtree extracts only `src/` commits and sends them with full commit history to the team).*

---

## 3. General Git & Branching Policy
- **Branch Tracking**: All valid experiment branches (`exp/r1-*`, `exp/r2-*`) must be pushed to remote for ablation study tracking.
- **Clean Main Invariance**: Experimental code lives only on feature branches. The `main` branch only receives validated merges.
- **Binary Exclusion**: Heavy model weights (`*.pt`, `*.ckpt` > 10MB) and raw datasets (`*.mat`, `*.h5`) are strictly forbidden from Git tracking (`.gitignore`).
- **Pre-Push Guardrail**: Run `python .agent/rules/autoAgentFlow/pre_push_check.py` before pushing to ensure zero heavy binary leaks.
- **Commit Pinning**: Pin image links in `WORKLOG.md` to immutable commit hashes once pushed to remote.

---

## 4. Specialized Workflow Routing
When performing specialized workflows, consult the dedicated guideline files:
- **Git Subtree Architecture & Remote Sync**: Follow [`note_folder_organize_wSubtree.md`](./note_folder_organize_wSubtree.md).
- **Shift-Based Execution & Task Queue**: Follow `_plan/tasks.json` and [`autoAgentFlow/rules_plan_workflow.md`](./autoAgentFlow/rules_plan_workflow.md).
- **Worklog & Benchmark Recording**: Follow [`takeWorkLogFlow/rules_worklog.md`](./takeWorkLogFlow/rules_worklog.md).
- **Autonomous & Overnight Pipeline Execution**: Follow [`autoAgentFlow/rules_autoAgent_AGY.md`](./autoAgentFlow/rules_autoAgent_AGY.md) (or `rules_autoAgent_Claude.md`).
- **2-Round Research Planning & Hypotheses**: Follow [`autoAgentFlow/rules_plan_workflow.md`](./autoAgentFlow/rules_plan_workflow.md) and [`autoAgentFlow/template_PLAN.md`](./autoAgentFlow/template_PLAN.md).
- **Literature Review & Citations**: Follow [`LiteratureReviewFlow/literatureReview_rules.md`](./LiteratureReviewFlow/literatureReview_rules.md).
