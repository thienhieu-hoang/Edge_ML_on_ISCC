---
trigger: always_on
description: Operational directives for Google Antigravity 2.0 - Multi-agent orchestration, native subagents, reactive wakeup, shift-based execution, mechanistic verification, and core immutability
---

# Autonomous Multi-Agent Directives (Antigravity 2.0 Workflow)

These guidelines govern autonomous execution, subagent orchestration, and long-running benchmark runs when operating within **Google Antigravity (AGY)**.

---

## 1. Core Operating Modes & Slash Commands

Antigravity uses native slash commands to configure operational autonomy:

| Command | Recommended Usage |
| :--- | :--- |
| **`/goal`** | **Primary Autonomous Mode**: Activates deep reasoning and autonomous execution for long-running or overnight tasks. The agent will not stop prematurely or ask trivial questions; it executes task-by-task from `_plan/tasks.json`, verifies output artifacts, recovers from errors, and delivers the final synthesis. |
| **`/plan`** | Complex architectural refactoring or multi-file designs requiring review before execution. |
| **`/teamwork`** | Autonomous collaboration across specialized agents on large codebases. |
| **`/schedule`** | One-shot or recurring cron-based execution for periodic benchmarking or data synchronization. |

---

## 2. Antigravity Native Subagent Architecture

Antigravity provides built-in tools for spawning and managing subagents with isolated context windows to prevent "context rot":

### A. Subagent Types & Tool Permissions
- **`research` (Built-in Read-Only)**: Runs in a read-only sandbox. Delegate broad code searches, file reading, or documentation surveys here to keep the main conversation clean.
- **`define_subagent` (Custom Roles)**: Define fine-grained agents before invocation:
  - `EnableWriteTools: false` $\rightarrow$ Read-only auditor or reviewer.
  - `EnableWriteTools: true` $\rightarrow$ Dedicated code implementer.
  - `EnableMCPTools: true` $\rightarrow$ Domain tools (biomolecular viewers, database querying).
- **`invoke_subagent`**:
  - `Workspace: "branch"` or `"share"` $\rightarrow$ Spawns the agent in an isolated workspace branch (worktree) to avoid file lock conflicts.
  - `Model: "flash"` or `"flash_lite"` $\rightarrow$ Fast, lightweight execution for repetitive scans; `"pro"` or `"inherit"` for complex reasoning.

### B. Reactive Wakeup (Zero Polling Rule)
- **Do NOT run sleep or polling loops in terminal commands.**
- When running long background scripts (> 15s), use `run_command` in background/async mode (`WaitMsBeforeAsync: 500-1000`).
- The system automatically triggers a **reactive wakeup** when the background task finishes or when a subagent sends a message via `send_message`.

---

## 3. Shift-Based Execution & Mechanistic Verification Gatekeeper

### A. Shift-Based Context Protocol (`_plan/tasks.json`)
- Read `_plan/tasks.json` on disk to inspect current queue state.
- Pick the first task with `"status": "todo"`. Mark it as `"in_progress"`.
- Focus context exclusively on that atomic task to prevent context degradation.

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
When logging stage results or benchmark outputs:
1. **Main `_note/WORKLOG.md` Format (Day Only, Reverse-Chronological)**:
   - Header entries by **Day only** (`## YYYY-MM-DD`). Do **NOT** put hour/time in the main worklog headers.
   - **Reverse-Chronological Ordering**: Always place newer notes on **higher lines (top of the file)**.
   - **Summary Only**: Record only the top-line comparison table (mean ± std), primary comparison plot, and bullet conclusions.
2. **Offload Details to `_note/helperWorklog/details_yymmdd-hhmm.md`**:
   - Save full diagnostics, raw per-seed runs, and configuration details into `_note/helperWorklog/details_yymmdd-hhmm.md`.
   - In `_note/WORKLOG.md`, link directly to this file:
     `[Detailed Experiment Log & Analysis](./helperWorklog/details_yymmdd-hhmm.md)`.
3. **Atomic Git Commits & State Persistence**:
   - Update `_plan/tasks.json` on disk.
   - Commit both the worklog summary, detailed note, and task state together:
     ```bash
     git add _note/WORKLOG.md _note/helperWorklog/ _plan/tasks.json
     git commit -m "stage(<stage-name>): complete benchmark run with <metric-summary>"
     ```

---

## 4. Pre-Push Guardrail & Interactive Deliverables

- **Pre-Push Check**: Before running `git push-collab`, execute `python autoAgentFlow/pre_push_check.py` to ensure no heavy binaries (`*.pt`, `*.mat` > 10MB) or private notes are tracked.
- **Visual Loop**: For visual evaluation, surface interactive `sidecar://` links or Generative UI widgets so results can be inspected interactively.
- **Morning Briefing**: On task completion, summarize all stage outcomes, provide links to generated vector figures (`.pdf`), and report any edge-case failures.
