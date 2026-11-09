# _research_tool: Standalone Literature Review & Evidence Retrieval Module

A lightweight, portable academic research module designed for seamless integration into any research repository with **Google Antigravity 2.0**.

No LLM API keys required. All search and retrieval operations are performed directly against public academic APIs (**Semantic Scholar** & **OpenAlex**), while advanced synthesis, hypothesis verification, and LaTeX citation drafting are handled by **Antigravity 2.0**.

---

## 📁 Directory Structure

```text
_research_tool/
├── research_agent.py      # Core Dual-Perspective retrieval & BibTeX generator
├── requirements.txt       # Minimal dependencies (requests only)
├── rules_snippet.md       # Pre-built agent workflow rule to paste into .agent/rules
├── run.bat                # 1-click interactive CLI launcher for Windows
├── .env.example           # Optional configurations (e.g., SEMANTIC_SCHOLAR_API_KEY)
└── literature/            # Generated workspace outputs (auto-created)
    ├── metadata.json      # Structured paper catalogue (abstracts, DOI, authors)
    ├── summary.md         # Evidence digest and abstracts formatted for Antigravity
    └── references.bib     # Formatted BibTeX entries ready for LaTeX
```

---

## ⚡ Quick Setup

1. **Copy folder into your project**:
   Copy `_research_tool/` into your active project workspace.

2. **Install dependency** (only standard `requests` is required):
   ```bash
   pip install -r _research_tool/requirements.txt
   ```

3. **Add Agent Rule**:
   Copy the content of [`rules_snippet.md`](rules_snippet.md) into your project's `.agent/rules` (or `CLAUDE.md`).

---

## 🚀 How to Run

### Option 1: Autonomous Agent Workflow (Recommended with Antigravity 2.0)
Just ask your research questions directly to **Antigravity 2.0** in the chat:
> *"What are the current performance limits of Transformers compared to CNNs in wireless channel estimation?"*

Antigravity will:
1. Decompose the question into targeted positive and counter-argument queries.
2. Run `python _research_tool/research_agent.py --query "..."`.
3. Read `literature/summary.md` and `literature/references.bib`.
4. Perform critical cross-verification and draft your literature review with `\cite{...}` commands into your `.tex` paper.

### Option 2: Command Line (CLI)
```bash
python _research_tool/research_agent.py --query "wireless channel estimation transformer vs cnn"
```

Optional specific counter-argument search:
```bash
python _research_tool/research_agent.py --query "channel estimation transformers" --counter-query "transformer computational complexity latency limitations"
```

### Option 3: 1-Click Batch File (`run.bat`)
Double-click `run.bat` to launch interactive mode in Windows Command Prompt.

---

## 🛡️ Output Artifacts (`literature/`)

- **`metadata.json`**: Complete machine-readable metadata, DOIs, open-access PDF links, and abstracts.
- **`summary.md`**: Human- and LLM-readable summary table of retrieved works with detailed Abstract and TLDR records.
- **`references.bib`**: Clean, standardized BibTeX entries escaping LaTeX special characters, ready for your `.bib` bibliography.
