# LiteratureReviewFlow: Standalone Literature Review & Evidence Retrieval Module

A lightweight, portable academic research module designed for seamless drop-in integration into any research repository or paper-writing project with **Google Antigravity 2.0**.

No external LLM API keys required. All search and retrieval operations are performed directly against public academic endpoints (**OpenAlex** & **Semantic Scholar**) with **guaranteed IEEE prioritization (≥10 papers)**, while advanced synthesis, hypothesis verification, interactive Markdown linking, and LaTeX citation drafting are handled by **Antigravity 2.0**.

---

## 📁 Repository Structure

```text
LiteratureReviewFlow/
├── README.md              # Master guide & integration instructions (this file)
├── rules_snippet.md       # Pre-built agent workflow rule to copy into your project
│
└── _research_tool/        # 📦 PORTABLE DROP-IN MODULE (Copy ONLY this folder to your project)
    ├── research_agent.py  # Fast academic retrieval & BibTeX generator (< 2s)
    ├── requirements.txt   # Minimal dependencies (requests only)
    ├── run.bat            # 1-click interactive CLI launcher for Windows
    ├── .env.example       # Optional configs (e.g., SEMANTIC_SCHOLAR_API_KEY)
    ├── .env               # Local configuration file
    └── literature/        # Auto-created output directory
        ├── metadata.json  # Structured paper catalogue (abstracts, DOI, authors)
        ├── summary.md     # Evidence digest and abstracts formatted for Antigravity
        └── references.bib # Formatted BibTeX entries ready for LaTeX
```

> **Note:** The `_research_tool/` folder is intentionally kept 100% clean and minimal. It contains only the runtime script and configs so that copying it into any target project keeps that project lightweight (< 100 KB).

---

## ⚡ How to Integrate into Any Target Project

### Step 1: Copy `_research_tool/` into your project
Copy the entire `_research_tool/` folder into your active project workspace:
```text
YourProject/
├── _research_tool/        <-- Copied here
├── src/
├── paper.tex
└── ...
```

### Step 2: Install dependency
Only standard `requests` is required (if not already installed in your Python environment):
```bash
pip install -r _research_tool/requirements.txt
```

### Step 3: Add Agent Rule to your project
Copy the contents of [`rules_snippet.md`](rules_snippet.md) into your project's `.agent/rules` (or `CLAUDE.md`).

---

## 🎯 Architecture & Capabilities

1. **Keyless & Zero External LLM Configuration**:
   - Eliminates all dependencies on external Gemini API keys or billing quotas.
   - Searches public scholarly endpoints directly (**OpenAlex** & **Semantic Scholar**).

2. **Dedicated IEEE Prioritization (≥ 10 Papers)**:
   - Uses OpenAlex publisher lineage (`p4310319808`) to guarantee at least 10+ publications from IEEE (Transactions, Journals, Conferences, IEEE Access).
   - Enriches findings with top-cited high-impact works from Springer Nature, ACM, Elsevier, and arXiv.

3. **Dual-Perspective Retrieval**:
   - Gathers both affirmative literature (`supporting`) and critical counter-arguments/limitations (`counter_argument` — e.g., hardware latency, computational complexity, memory wall, green edge AI).

4. **Powered by Antigravity 2.0 as the Reasoning Engine**:
   - The Python script acts as a fast **Academic Retriever & BibTeX Generator** (takes < 2 seconds).
   - **Antigravity 2.0** acts as the **Lead Research Scientist**: breaking down hypotheses, synthesizing critical literature reviews, verifying cited claims against real abstracts, and integrating citations into LaTeX.

5. **Interactive Citation Linking in Markdown**:
   - Replaces bare `\cite{...}` in Markdown prose with clickable anchor links: `([Author et al., Year](#ref-citekey))`.
   - Generates a dedicated `## References` section with anchor tags `<a id="ref-citekey"></a>`, DOI links, and direct open-access PDF links.

---

## 🚀 How to Run

### Option 1: Autonomous Agent Workflow (Recommended with Antigravity 2.0)
Just ask your research questions directly to **Antigravity 2.0** in the chat:
> *"What are the current performance limits of Transformers compared to CNNs in wireless channel estimation?"*

Antigravity will automatically:
1. Decompose the question into targeted positive and counter-argument queries.
2. Run `python _research_tool/research_agent.py --query "..." --counter-query "..." --min-ieee 10`.
3. Read `literature/summary.md` and `literature/references.bib`.
4. Synthesize the findings into an interactive Markdown report and draft ready-to-use LaTeX `\cite{...}` snippets for your paper.

### Option 2: Command Line (CLI)
```bash
python _research_tool/research_agent.py --query "wireless channel estimation transformer vs cnn"
```

With specific counter-argument query and IEEE target:
```bash
python _research_tool/research_agent.py --query "channel estimation transformers" --counter-query "transformer hardware latency complexity limitations" --min-ieee 10
```

### Option 3: 1-Click Batch File (`run.bat`)
Double-click `_research_tool/run.bat` to launch interactive mode in Windows Command Prompt.

---

## 🛡️ Output Artifacts (`_research_tool/literature/`)

- **`metadata.json`**: Complete machine-readable metadata, DOIs, open-access PDF links, and abstracts.
- **`summary.md`**: Human- and LLM-readable summary table of retrieved works with detailed Abstract and TLDR records.
- **`references.bib`**: Clean, standardized BibTeX entries escaping LaTeX special characters and containing journal titles, ready for your `.bib` bibliography.
