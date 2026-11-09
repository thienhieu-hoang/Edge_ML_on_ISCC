---
trigger: always_on
description: Operational directives for Claude Code - Multi-agent orchestration, sub-agents, worktrees, shift-based execution, mechanistic verification, and core immutability
---

# Autonomous Multi-Agent Directives (Claude Code Workflow)

These guidelines govern autonomous execution, sub-agent delegation, and long-running workflows when operating within **Claude Code** (CLI, Desktop, and Cloud sessions).

---

## 1. Architectural Philosophy: The Three Pillars

### A. Context Preservation & Anti-"Context Rot"
- **The Problem:** Processing massive raw build logs, grepping 50+ files, or analyzing long test outputs in the main session rapidly pollutes the context window, degrading architectural reasoning.
- **The Rule:** The Lead Agent acts as **Architect / Lead Scientist**. Whenever a task requires deep code searches, log parsing, or isolated verification, **fork a dedicated sub-agent**.
- Sub-agents operate in their own isolated context and must return **only concise summaries, diff patches, or key metrics** back to the primary session.

### B. Separation of "What" (Skills) and "Who" (Sub-Agents)
- **Skills (`SKILL.md` / `rules/`):** Define the *Standard Operating Procedures (SOP)*, coding conventions, verification checklists, and output formats.
- **Sub-Agents (`.claude/agents/*.yaml` or `--agents`):** Define the *Executor* profiles with fine-grained tool scoping (e.g., read-only code reviewer vs. bash-enabled test runner).
- Agents dynamically adopt skills relevant to their assigned scope without loading unnecessary global logic.

### C. Parallel Execution via Git Worktrees
- For parallel or multi-branch feature execution across accounts or stages:
  - Spawn sub-agents into isolated git worktrees (`git worktree add ../feature-branch`).
  - Keep backend and frontend tasks decoupled in separate worktrees to eliminate workspace lock conflicts.
  - Review and merge back into the main branch only after automated validation passes.

---

## 2. Shift-Based Execution & Mechanistic Verification Gatekeeper

### A. Shift-Based Protocol (`_plan/tasks.json`)
- Never start a session without reading `_plan/tasks.json`.
- Pick the first task with `"status": "todo"`. Set `"status": "in_progress"`.
- Keep the current context strictly focused on this single task. Once complete, save `tasks.json` and hand off to the next shift with a fresh context.

### B. Mechanistic Verification Gatekeeper (Zero Trust in Self-Claims)
A task is **NEVER** marked `"done"` based on self-claim. It is marked `"done"` ONLY when:
1. Terminal command returns **Exit Code 0** (`$? == 0`).
2. Target artifact exists on disk (e.g., `results/result.json`) with file size $> 0$.
3. Parsed JSON contains all required keys and **zero** invalid numerical values (`NaN`, `Infinity`, `null`).

### C. Circuit Breakers (Anti-Burnout & Loop Prevention)
- **Max Retries**: Each task is allowed a maximum of **2 retries**. If a task fails twice, mark it as `"failed"`, record the traceback in `error.log`, and advance to the next task. Never retry in an infinite loop.
- **Emergency Halt**: If **3 consecutive tasks** fail, halt autonomous execution immediately and alert the user.
- **Timeout Guard**: Terminate and log any individual task that exceeds 30 minutes runtime.

### D. Immutability of Core & Deterministic Seed Locking
- **Core Immutability**: `src/core/` is frozen (Read-Only) during experiments. Agents must NEVER alter evaluation metrics, loss functions, or dataloaders in `src/core/` while tuning an approach.
- **Deterministic Seeds**: Random seeds must be strictly fixed to `[0, 1, 2]`. Results must always be reported as **`Mean ± Std`** over all 3 seeds.
- **Ablation Tagging**: Any underperforming model must be pushed with status `Degraded (Ablation Asset)` and accompanied by a physical failure diagnosis in `_plan/PLAN1.md` for publication ablation studies.

### E. Worklog Summary & Detailed Note Offloading (`_note/helperWorklog/`)
When recording benchmark/stage outputs in the project worklog:
1. **Main `_note/WORKLOG.md` Format (Day Only, Reverse-Chronological)**:
   - Header by **Day only** (`## YYYY-MM-DD`). Do **NOT** put hour/time in the main worklog headers.
   - **Reverse-Chronological Ordering**: Always place later / newer notes on **higher lines (top of the file)**.
   - **Summary Only**: Record only the top-level metrics table (mean ± std), key comparison plot, and bullet conclusions.
2. **Offload Details to `_note/helperWorklog/` with Year-Month-Day-Time**:
   - Save full diagnostics, raw per-seed numbers, and configurations in `_note/helperWorklog/details_yymmdd-hhmm.md`.
   - In `_note/WORKLOG.md`, link directly to this file:
     `[Detailed Experiment Log & Analysis](./helperWorklog/details_yymmdd-hhmm.md)`.
3. **Atomic Git Commits & State Persistence**:
   - Update `_plan/tasks.json` on disk.
   - Commit the summary, detail note, and task state together:
     ```bash
     git add _note/WORKLOG.md _note/helperWorklog/ _plan/tasks.json
     git commit -m "stage(<stage-name>): complete benchmark run with <metric-summary>"
     ```

---

## 3. Remote Control & Pre-Push Guardrail

- **Pre-Push Check**: Before running `git push-collab`, execute `python autoAgentFlow/pre_push_check.py` to ensure no heavy binaries (`*.pt`, `*.mat` > 10MB) or private notes are tracked.
- **Cloud Handoff (`claude --cloud`):** Launch long-running jobs on remote workstations or cloud compute instances.
- **Monitoring & Intervention:** Monitor progress from mobile or desktop apps; send steering prompts if early logs diverge.
- **Local Synchronization:** Pull finalized commits and generated figures (`git pull`) back to the local development environment for manuscript compilation.
