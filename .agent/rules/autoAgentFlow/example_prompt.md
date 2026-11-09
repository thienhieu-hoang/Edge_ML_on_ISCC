# Battle-Tested Prompts for AI Research Agents

This document provides two production-grade prompt templates designed to activate your project's autonomous research workflow, shift-based execution, and mechanistic verification.

---

## 1. Prompt 1: Research Planning & Task Queue Generation

> **When to Use**: At the start of a new project, feature, or research milestone before any code is executed.
> **Deliverable**: Populates Section 0 & 1 of `_plan/PLAN1.md` and generates atomic execution items in `_plan/tasks.json`.

```text
Act as the Senior Lead Scientist and System Architect for this project.
I need you to investigate the following research problem and formulate a 2-round experimental plan:

### 1. Research Objectives & System Bounds:
- Core Problem: [Insert problem statement, e.g., Joint Power Allocation and Beamforming Optimization in Multi-User ISCC Networks]
- Performance Milestone: [Insert target metric, e.g., Achieve ≥ 15% system sum-throughput improvement over Greedy baseline with runtime < 10ms]
- Physical & Mathematical Constraints: [Insert constraints, e.g., Peak transmit power P_max, Rician fading channel, Doppler shift, positive semi-definite covariance]

### 2. Operational Directives:
1. Review the project directives in `.agent/rules/main.md` and `.agent/rules/autoAgentFlow/rules_plan_workflow.md`.
2. Strictly enforce the "First-Principles & Mathematics First" doctrine:
   - Identify the governing equations, dimensional scales, and boundary limits.
   - Define two mandatory baselines to beat: one classical/analytical baseline and one prior SOTA benchmark.
   - Propose 2 to 3 candidate approaches (A1, A2, A3) grounded in mathematical/physical mechanisms. Generic black-box proposals without theoretical justification are strictly prohibited.
3. Update the planning state on disk:
   - `_plan/PLAN1.md`: Fill Sections 0 and 1 with formulations, hypotheses, and benchmark execution scripts.
   - `_plan/tasks.json`: Generate the corresponding atomic task entries with execution commands, verification criteria, and circuit breaker limits.

Provide a concise mathematical summary of your proposed plan and confirm once both files are written to disk.
```

---

## 2. Prompt 2: Autonomous Overnight Execution (`/goal`)

> **When to Use**: In the evening before going to bed. 
> **Deliverable**: Autonomous execution of all pending tasks in `_plan/tasks.json`, mechanistic verification, atomic git commits, experimental branch pushes, and a morning briefing.

```text
/goal
Act as my Senior Autonomous Research Co-pilot. 
Tonight, your mission is to autonomously execute all pending tasks in `_plan/tasks.json` following our system protocols and deliver a complete research briefing by morning.

### Strict Operational Safeguards:
1. Shift-Based State Machine (`_plan/tasks.json`):
   - Shift Execution: Read `_plan/tasks.json`, pick the first task with status "todo", set it to "in_progress", and focus your context exclusively on that task.
   - Code Sandboxing: All approach-specific code must be placed inside `src/approaches/<approach_id>/`. The `src/core/` directory is frozen (Read-Only) to prevent regression drift.
   - Deterministic Evaluation: Benchmark all approaches locally on GPU/CPU across the fixed 3-seed suite: [0, 1, 2].

2. Mechanistic Verification Gatekeeper (Zero Trust in Self-Claims):
   - A task is NEVER marked "done" based on self-assessment. It is marked "done" ONLY when:
     a) Terminal command returns Exit Code 0 ($? == 0).
     b) Target output artifact (e.g., results/result.json) exists on disk with file size > 0.
     c) Parsed JSON contains all required keys and zero NaN, Infinity, or null values.
   - Circuit Breakers: Allow a maximum of 2 retries per task. If a task fails twice, log the traceback to error.log, mark it "failed", and proceed to the next task. If 3 consecutive tasks fail, halt execution.

3. Logging & Version Control:
   - Executive Summary (`_note/WORKLOG.md`): Append high-level metrics (Mean ± Std), primary comparison plots, and dated day-level headers (reverse-chronological).
   - Detailed Offloading (`_note/helperWorklog/`): Save complete logs, traces, and hyperparameter dictionaries into `details_yymmdd-hhmm.md` and link it from WORKLOG.md.
   - Branch Tracking: Commit atomic updates and push all valid experimental branches (exp/r1-*) to remote for ablation study archival.

When all tasks are complete:
- Generate camera-ready vector comparison plots (.pdf) in the results directory.
- Leave an Executive Briefing as your final chat response for when I wake up, summarizing winning/losing models and the underlying physical reasons for their performance.
```

---

## 3. Morning Deliverables Verification Checklist

When you wake up and inspect your workspace, verify the following state:

- [ ] **Chat Window**: Contains the high-level Executive Briefing summarizing benchmark outcomes and physical root-causes.
- [ ] **`_plan/tasks.json`**: All completed tasks display `"status": "done"` with timestamps and commit hashes.
- [ ] **`_note/WORKLOG.md`**: Top rows contain the latest dated entries with `Mean ± Std` comparison tables and links to `helperWorklog/`.
- [ ] **`_note/helperWorklog/`**: Contains timestamped detail files (`details_yymmdd-hhmm.md`) for every individual run.
- [ ] **GitHub Remote**: Experimental branches (`exp/r1-*`) are pushed to the remote repository for ablation tracking, while `main` remains clean.
