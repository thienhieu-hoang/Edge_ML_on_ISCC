# Git Subtree Architecture (Single Local Repo with Dual Remotes)

This architecture maintains **a single local working directory** on your machine while synchronizing with **two independent remote repositories** on GitHub:
1. **Personal Remote (`origin`)**: Private repository containing the complete project (`src/`, `_note/`, `_plan/`) with full commit history.
2. **Collab Remote (`collab`)**: Team/Lab repository containing **only** the source code (`src/`), completely isolated from private notes and roadmaps.

```
[GitHub Collab (Team)]                                     [GitHub Personal (Private)]
https://github.com/lab/collab.git                          https://github.com/you/private.git
(Contains ONLY code from src/)                             (Contains EVERYTHING: _note/ + _plan/ + src/)
          ▲                                                          ▲
          │                                                          │
          │ git subtree pull/push                                    │ git push origin main
          │                                                          │
          └──────────────────────────┬───────────────────────────────┘
                                     │
                      [SINGLE LOCAL DIRECTORY ON DISK]
                      \Project_Private/
                      ├── .git/
                      ├── src/                             # Team codebase (managed via Subtree)
                      ├── _note/                           # Private research notes
                      └── _plan/                           # Private roadmaps
```

---

## 1. Directory Structure (Single Local Repository)

No Windows Junctions or duplicate local folders are required. Everything resides in one clean directory:

```text
Project_Private/
├── .git/                # Single local Git database
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

---

## 2. One-Time Setup

Run these commands once in your local `Project_Private` root:

### Step A: Initialize Git and Register Both Remotes
```bash
git init
git remote add origin https://github.com/you/my_project_private.git
git remote add collab https://github.com/lab/collab_project.git
```

### Step B: Import Team Codebase as a Subtree
Pull the team repository directly into the `src/` prefix:
```bash
git subtree add --prefix=src collab main
```
*(Git automatically downloads the code and imports the team's entire commit history into your local repository).*

### Step C: Configure Convenient Aliases (Recommended)
Set up shortcuts so you never have to type long subtree commands:
```bash
git config alias.pull-collab "subtree pull --prefix=src collab main"
git config alias.push-collab "subtree push --prefix=src collab main"
```

---

## 3. Daily Friction-Free Workflow

You do **not** need to push to the team continuously. Commit locally throughout the day and push to the team in a single batch at the end of the day.

### A. Morning: Pull Latest Code from Team
```bash
git pull-collab
```
*(Equivalent to `git subtree pull --prefix=src collab main`. Merges the latest team changes and their commit messages into your local `src/`).*

### B. Throughout the Day: Code, Run Experiments, Commit Locally
`git commit` is **100% local**. You do **NOT** need to specify whether a commit belongs to Collab or Personal:
```bash
# 10:00 - Implement a new feature in code
git add src/
git commit -m "feat(model): add Frequency Mixer architecture"

# 14:00 - Log benchmark results
git add _note/
git commit -m "docs(worklog): record stage 1 NMSE comparison"

# 16:30 - Fix a bug in data loader
git add src/
git commit -m "fix(data): resolve subcarrier indexing bug"
```
*(Optional: You can push to your private GitHub anytime for cloud backup: `git push origin main`).*

### C. End of the Day: Batch Push to Team & Personal Backup
When your daily features are verified, run two simple commands:

#### 1. Push All Code Commits to the Team:
```bash
git push-collab
```
*(Equivalent to `git subtree push --prefix=src collab main`).*

**What happens behind the scenes:**
- Git Subtree scans all commits made today (or this week).
- It extracts **only** the commits that modified `src/`.
- It packages and pushes them to the team's GitHub repository.
- Each code commit appears on the team's GitHub with its original commit message and timestamp.
- **Your `_note/` and `_plan/` directories are completely excluded and never seen by the team.**

#### 2. Backup Everything to Your Private GitHub:
```bash
git push origin main
```
Pushes all code, notes, and plans to your private repository.

---

## 4. Key Advantages of This Setup

| Feature | Windows Junction Approach | Git Subtree Approach |
| :--- | :--- | :--- |
| **Local Directories** | Requires 2 separate folders on disk | **1 single folder on disk (Zero disk duplication)** |
| **OS Independence** | Windows-only (`mklink /J`) | **100% Cross-Platform (Windows, Mac, Linux)** |
| **Commit History on Private GitHub** | Lost (flattened into 1 commit) | **Preserved (Full commit messages & author history)** |
| **Accidental Deletion Risk** | High (`Remove-Item` bug) | **Zero (Standard Git directories)** |
| **Team Privacy** | Full privacy (code only) | **Full privacy (notes/plans never exported)** |
