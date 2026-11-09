---
trigger: always_on
description: Standard operational rules for worklog tracking, benchmark logging, and manuscript figure integration
---

# Universal Worklog & Benchmark Tracking Rules

## 1. Target Worklog Location & Reverse-Chronological Ordering
- **Target File**: Locate `WORKLOG.md` (or `.note_worklog/WORKLOG.md`, or `worklog/WORKLOG.md` as defined by the project root).
- **Explicit Trigger Only**: Do NOT automatically append entries to `WORKLOG.md` on routine edits or debugging. ONLY update when the user explicitly requests to record, update, or summarize results/worklog.
- **Date Header Only (Day Level)**:
  - In `WORKLOG.md`, header entries by **Day only** (e.g., `## YYYY-MM-DD` or `## DD/MM/YYYY`).
  - Do **NOT** record the hour/minute in the main `WORKLOG.md` headers (keep the clean day-level structure).
- **Reverse-Chronological Ordering (Latest at the Top)**:
  - ALWAYS place newer / later entries on **higher lines (top of the file)**.
  - The most recent date header must sit at the very top.
  - If multiple entries are recorded for the **same day**, insert the newer action as the **higher row / top entry under that day's header**.

---

## 2. Summary-Only Rule & Offloading Details (`helperWorklog/`)
To keep `WORKLOG.md` concise, clean, and focused on core executive decisions and top-level benchmarks:
- **Summary Results Only in `WORKLOG.md`**:
  - In `WORKLOG.md`, record **ONLY the concise summary results**: top-line comparison table (mean ± std), primary comparison plot, and executive takeaway bullets.
  - **Do NOT dump long conversational text, raw per-step logs, extensive hyperparameters, or lengthy theoretical derivations directly into `WORKLOG.md`**.
- **Detailed Note Offloading in `helperWorklog/`**:
  - Store full logs, individual seed breakdowns, complete configuration dictionaries, and comprehensive discussions in a dedicated file inside the **`helperWorklog/`** folder (located at the **same level** as `WORKLOG.md`).
  - **Mandatory Naming Syntax (Year-Month-Day-Time)**:
    `helperWorklog/details_yymmdd-hhmm.md` (or `details_yyyymmdd-hhmm.md`)
    where:
    - `yy` = 2-digit year (e.g., `26`)
    - `mm` = 2-digit month (e.g., `11`)
    - `dd` = 2-digit day (e.g., `04`)
    - `hh` = 2-digit hour in 24-hour format (e.g., `15`)
    - `mm` = 2-digit minute (e.g., `30`)
    *(Example: `helperWorklog/details_261104-1530.md` for November 4, 2026 at 15:30).*
  - **Linking**: In the `WORKLOG.md` summary entry, provide a direct relative link to the detailed file:
    ```markdown
    [Detailed Experiment Log & Analysis](./helperWorklog/details_261104-1530.md)
    ```

---

## 3. Image Path Strategy: Local vs. Commit-Pinned Remote

### A. Default / In-Progress (Local Relative Paths)
- When logging intermediate results, daily runs, or uncommitted work:
- Use local relative paths with forward slashes:
  ```markdown
  ![Figure description](./results/figures/comparison.png)
  ```
- **Why**: Keeps links functioning immediately offline in local viewers (Obsidian, VS Code) before committing/pushing.

### B. Explicit "Update Worklog" (Batch Remote Commit-Pinning)
When explicitly told to *"update worklog"* or *"freeze worklog links"*:
1. **Query Remote & Hash Once**:
   - Get the repository's latest commit hash: `git rev-parse HEAD`.
   - Inspect the remote GitHub repository URL: `git config --get remote.origin.url` (parse `<owner>/<repo>`).
2. **Batch Apply (No Per-File Checking)**:
   - Convert all active local paths in new/modified entries to:
     `https://raw.githubusercontent.com/<owner>/<repo>/<latest-commit-hash>/<path-to-image>`
   - Do **NOT** run per-file git log lookups.
3. **Preserve Older Remote Links**:
   - If a link is already an external GitHub link with a previous commit hash, **do not touch it**. This preserves historical experiment states frozen in time.

---

## 4. Visual Styling & HTML Badges (`<mark style="...">`)
When formatting summary tables, metrics, or status tags, use standard inline badges:

- **Status / Workflow**:
  - `completed`: `<mark style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 4px;">completed</mark>`
  - `in-progress`: `<mark style="background-color: #fff3cd; color: #856404; padding: 2px 6px; border-radius: 4px;">in-progress</mark>`
  - `failed`: `<mark style="background-color: #ffebe9; color: #cf222e; padding: 2px 6px; border-radius: 4px;">failed</mark>`
  - `baseline`: `<mark style="background-color: #e2e3e5; color: #383d41; padding: 2px 6px; border-radius: 4px;">baseline</mark>`
  - `proposed`: `<mark style="background-color: #cce5ff; color: #004085; padding: 2px 6px; border-radius: 4px; font-weight: 600;">proposed</mark>`

---

## 5. LaTeX & Manuscript Integration Rules
When importing results or figures from `WORKLOG.md` into a LaTeX document or paper draft:
1. **Convert Remote GitHub Links back to Local Paths**:
   - Strip `https://raw.githubusercontent.com/.../<commit>/` to map directly to the workspace path (LaTeX engines cannot fetch raw URLs via `\includegraphics`).
2. **Always Reference the Latest Local Workspace Version**:
   - Manuscripts must compile from the current local workspace, not historical frozen commits.
3. **Vector Priority (`.pdf` / `.eps`)**:
   - Always replace raster extensions (`.png`, `.jpg`) with vector format (`.pdf`) if available:
     `\includegraphics[width=\linewidth]{figures/comparison.pdf}`
4. **Exact Metrics**:
   - Check the accompanying `results.json` or numerical output file in the figure directory to cite exact numerical metrics rather than guessing from plots.

---

## 6. GitHub Markdown Math & Formatting Compatibility
- **Inline Math (`$...$`):** No spaces after the opening `$` and no spaces before the closing `$` (e.g., `$\mathbf{y} = \mathbf{H}\mathbf{x}$`, NOT `$ \mathbf{y} $`).
- **Display Math (`$$`):** Put `$$` on standalone lines with empty lines above and below.
- **Never Put Math Inside HTML Tags:** GitHub's renderer will fail to render math inside raw HTML blocks (`<div>`, `<span>`, `<p>`). Equations must sit outside HTML layout tags.
