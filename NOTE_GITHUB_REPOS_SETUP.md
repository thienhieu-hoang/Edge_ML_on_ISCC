# GitHub Repositories Setup & Subtree Linking Guide

> **Project Root**: `C:\Users\AT30890\Hoctap\4_Edge_ML_on_wirelessSys`  
> **Architecture**: Git Subtree Dual-Remote Architecture (Single Local Directory)  
> **Reference Documents**: `.agent/rules/note_folder_organize_wSubtree.md`, `.agent/rules/main.md`, `.agent/rules/main2.md`

---

## 1. Executive Summary: Which GitHub Repositories to Create

To maintain complete privacy for your research ideas, agent rules, and worklogs while collaborating cleanly with lab members, create **two separate repositories** on GitHub:

| Attribute | 1. Personal Remote (`origin`) | 2. Collaborative Remote (`collab`) |
| :--- | :--- | :--- |
| **Suggested Repo Name** | `Edge_ML_on_wirelessSys_private` *(or `4_Edge_ML_on_wirelessSys`)* | `Edge_ML_on_wirelessSys` *(or `<lab_org>/Edge_ML_wireless`)* |
| **Visibility** | **Private** (Strictly personal) | **Private (Team/Lab Organization)** or **Public** |
| **Owner** | Personal Account (`thienhieu-hoang`) | Lab Organization or Team Member Repository |
| **What It Contains** | **The ENTIRE Project**: <br>• `.agent/` (Agent rules, prompts, workflows)<br>• `_plan/` (Hypotheses, roadmaps, `tasks.json`)<br>• `_note/` (`WORKLOG.md`, detailed notes)<br>• `_research_tool/` & `ref/` (Literature & PDFs)<br>• `src/` (All implementation code) | **ONLY Pure Source Code from `src/`**: <br>• `core/` (Dataloaders, metrics, physics channel models)<br>• `approaches/` (Candidate ML architectures)<br>• `run.py` (Master benchmark runner)<br>• `requirements.txt` / environment specs |
| **Local Folder Mapping** | Project root: `4_Edge_ML_on_wirelessSys/` | Subdirectory: `4_Edge_ML_on_wirelessSys/src/` |
| **Sync Mechanism** | Standard `git push origin main` | Subtree: `git subtree push/pull --prefix=src collab main` |

---

## 2. Architecture & Linking Blueprint

You keep **only one local folder** on your machine. You do **not** need Windows Junctions (`mklink /J`) or duplicate checkouts. Git Subtree automatically extracts and synchronizes only the `src/` folder with the collab remote, while standard Git tracks the full repository into your private remote.

```
[GitHub Collab (Team / Lab)]                               [GitHub Personal (Private)]
git@github.com:lab/Edge_ML_on_wirelessSys.git               git@github.com:thienhieu-hoang/Edge_ML_on_wirelessSys_private.git
(Contains ONLY code from src/)                              (Contains EVERYTHING: _note/ + _plan/ + .agent/ + src/)
          ▲                                                           ▲
          │                                                           │
          │ git push-collab / pull-collab                             │ git push origin main
          │ (Subtree on "src/")                                       │ (Full project backup)
          │                                                           │
          └───────────────────────────┬───────────────────────────────┘
                                      │
                     [SINGLE LOCAL DIRECTORY ON DISK]
                     C:\Users\AT30890\Hoctap\4_Edge_ML_on_wirelessSys/
                     ├── .git/                # Single Git database with dual remotes
                     ├── .gitignore           # Excludes >10MB weights (*.pt, *.mat, *.h5)
                     ├── src/                 # <─── Synced with Team Collab Remote
                     │   ├── core/            #      Shared dataloaders, channel models
                     │   ├── approaches/      #      Modular ML methods
                     │   └── run.py           #      Master runner script
                     ├── _note/               # [Private] WORKLOG.md & helperWorklog/
                     ├── _plan/               # [Private] PLAN1.md, tasks.json
                     ├── .agent/              # [Private] System prompts, multi-agent rules
                     ├── _research_tool/      # [Private] Literature scrapers & local tools
                     └── ref/                 # [Private] Research reference papers
```

---

## 3. Remote URLs Tailored to Your SSH Setup

Based on your SSH configuration (`~/.ssh/config`), your GitHub account is configured under host alias:
- **SSH Host Alias**: `github.com-thienhieu-hoang`
- **Identity File**: `~/.ssh/rsa_thienhieu-hoang`

Use the corresponding URLs below:

### Option A: Using SSH (Recommended)
- **Personal (`origin`)**: `git@github.com-thienhieu-hoang:thienhieu-hoang/Edge_ML_on_wirelessSys_private.git`
- **Collab (`collab`)**: `git@github.com-thienhieu-hoang:<collab_org_or_user>/Edge_ML_on_wirelessSys.git`  
  *(or standard `git@github.com:...` depending on the collaborator's setup)*

### Option B: Using HTTPS
- **Personal (`origin`)**: `https://github.com/thienhieu-hoang/Edge_ML_on_wirelessSys_private.git`
- **Collab (`collab`)**: `https://github.com/<collab_org_or_user>/Edge_ML_on_wirelessSys.git`

---

## 4. Step-by-Step Setup Runbook

Open PowerShell in `C:\Users\AT30890\Hoctap\4_Edge_ML_on_wirelessSys`:

### Step 1: Create the Repositories on GitHub
1. Go to [GitHub New Repository](https://github.com/new).
2. **Repo 1 (Private)**:
   - Name: `Edge_ML_on_wirelessSys_private`
   - Visibility: **Private**
   - Initialize with README: **Unchecked** (empty repo)
3. **Repo 2 (Collab)**:
   - Name: `Edge_ML_on_wirelessSys` (under your account or lab organization)
   - Visibility: **Private** (or Public)
   - Initialize with README: **Checked** (recommended, so it has an initial `main` commit)

---

### Step 2: Initialize Local Git and Create `.gitignore`
In PowerShell:
```powershell
cd C:\Users\AT30890\Hoctap\4_Edge_ML_on_wirelessSys
git init
```

Create a robust `.gitignore` to prevent leaking large neural network weights, simulation data, or credentials:
```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
.mypy_cache/

# Large Datasets & Channel Realizations (>10MB)
*.mat
*.h5
*.hdf5
*.npy
*.npz

# Deep Learning Checkpoints & Weights
*.pt
*.pth
*.ckpt
*.onnx

# Environment & Credentials
.env
*.local

# Temporary files & OS files
.DS_Store
Thumbs.db
```

---

### Step 3: Register Dual Remotes
Link both remotes to your single local repository:

```powershell
# 1. Register Personal Private Remote as 'origin'
git remote add origin git@github.com-thienhieu-hoang:thienhieu-hoang/Edge_ML_on_wirelessSys_private.git

# 2. Register Collaborative Remote as 'collab'
git remote add collab git@github.com-thienhieu-hoang:<collab_user_or_org>/Edge_ML_on_wirelessSys.git

# Verify remotes
git remote -v
```

---

### Step 4: Initial Commit & Backup to Personal Private Repo
Stage your existing files and push the entire workspace to your private remote:

```powershell
git checkout -b main
git add .
git commit -m "chore: initial project workspace setup with rules and literature"
git push -u origin main
```
*At this point, your private GitHub has 100% of your project backed up.*

---

### Step 5: Link the `src/` Directory to the Team Collab Repo

Depending on whether your collab repository is brand new or already contains code:

#### Scenario A: If Collab repo already exists on GitHub (e.g. initialized with README)
Pull the collab remote's files directly into your local `src/` prefix:
```powershell
git subtree add --prefix=src collab main --squash
```
*(Git downloads the team's initial code and maps it into `src/` without touching `_note/` or `_plan/`).*

#### Scenario B: If Collab repo is completely empty on GitHub
Make sure you have at least one file inside `src/` (e.g., `src/README.md`), commit it locally, and push `src/` as the initial code for the collab remote:
```powershell
# Ensure src folder has an initial file if empty
if (-not (Test-Path "src/README.md")) {
    New-Item -ItemType File -Path "src/README.md" -Value "# Edge ML on Wireless Systems Source Code"
    git add src/README.md
    git commit -m "feat(src): initialize source codebase"
}

# Push ONLY src/ to the team repo's main branch
git subtree push --prefix=src collab main
```

---

### Step 6: Configure Convenience Aliases (Mandatory)
Avoid typing long subtree flags every day by configuring Git aliases:

```powershell
git config alias.pull-collab "subtree pull --prefix=src collab main"
git config alias.push-collab "subtree push --prefix=src collab main"
```

Now you have two fast shortcuts:
- `git pull-collab` $\rightarrow$ pulls latest team changes into `src/`.
- `git push-collab` $\rightarrow$ extracts commits touching `src/` and pushes them to team repo.

---

## 5. Daily Development & Collaboration Workflow

You do **not** need to worry about which repo you are touching while you code. Work naturally:

```
                  ┌──────────────────────────────────────────────┐
                  │ Morning: Start Work                          │
                  │   git pull-collab                            │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │ Throughout the Day: Local Coding & Testing   │
                  │   git add src/approaches/A1_ISAC/            │
                  │   git commit -m "feat(isac): add IB feature" │
                  │   git add _note/WORKLOG.md                   │
                  │   git commit -m "docs(worklog): log metrics" │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │ End of Day / Milestone: Batch Push           │
                  │   1. Push code to team:                      │
                  │        git push-collab                       │
                  │   2. Backup everything to private GitHub:    │
                  │        git push origin main                  │
                  └──────────────────────────────────────────────┘
```

### Detailed Day-to-Day Commands:

1. **Morning: Pull Latest Team Code**
   ```powershell
   git pull-collab
   ```
   *Fetches updates made by team members and merges them cleanly into your local `src/`.*

2. **During the Day: Code, Run Experiments, Commit Locally**
   All commits are 100% local. Commit messages made in `src/` will preserve their timestamps and messages when sent to the team:
   ```powershell
   # Work on a new ML approach in its isolated sandbox
   git add src/approaches/
   git commit -m "feat(model): implement task-oriented compression bottleneck"

   # Record benchmark observations in your private worklog
   git add _note/
   git commit -m "docs(worklog): record stage 1 NMSE and accuracy curves"
   ```

3. **End of Day: Two-Step Push**
   - **Push code to the Team (`collab`)**:
     ```powershell
     git push-collab
     ```
     *Git Subtree automatically filters out commits touching `_note/`, `_plan/`, `.agent/`, and `ref/`. Only `src/` changes are pushed to the team.*
   - **Backup entire research project to Personal (`origin`)**:
     ```powershell
     git push origin main
     ```
     *Backs up all code, notes, execution plans, and literature to your private cloud.*

---

## 6. Golden Rules & Safeguards for This Setup

1. **Approach Sandboxing**:
   Always place candidate models in dedicated folders under `src/approaches/<approach_name>/` (e.g. `src/approaches/A1_ISAC_baseline/`). Never overwrite files in another approach's directory. This guarantees zero merge conflicts when collaborating.
2. **Heavy Binary Guardrail**:
   Never commit `.pt`, `.mat`, or `.h5` files > 10MB to Git. Run the pre-push check script before pushing:
   ```powershell
   python .agent/rules/autoAgentFlow/pre_push_check.py
   ```
3. **Commit Pinning in `WORKLOG.md`**:
   When referencing evaluation curves or figures in `WORKLOG.md` that are pushed to your private repo, reference the immutable commit hash from `origin` so historical logs remain permanent.
4. **Clean Main Invariance**:
   Keep `main` stable. When testing risky or extensive changes, branch out (`git checkout -b exp/r1-compression`), verify tests locally, and merge back into `main`.

---

## 7. Quick Command Cheat Sheet

| Intent | Command | Target Remote |
| :--- | :--- | :--- |
| **Pull team updates** | `git pull-collab` | `collab/main` $\rightarrow$ `src/` |
| **Push code to team** | `git push-collab` | `src/` $\rightarrow$ `collab/main` |
| **Backup full project** | `git push origin main` | Full repo $\rightarrow$ `origin/main` |
| **Check remote URLs** | `git remote -v` | Shows `origin` and `collab` |
| **Check staged changes** | `git status` | Local working tree |
