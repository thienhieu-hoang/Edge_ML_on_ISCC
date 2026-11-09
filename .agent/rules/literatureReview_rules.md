---
### WORKFLOW: LITERATURE REVIEW & HYPOTHESIS VERIFICATION
When the user asks a research question, requests academic papers, or seeks to verify a scientific hypothesis:

1. **Decompose Queries**:
   Break down the question into technical English search terms, distinguishing between:
   - Primary/supporting exploration queries.
   - Critical counter-arguments, complexity, latency, hardware, or limitation queries.

2. **Execute Retriever**:
   Run the local multi-source retriever (prioritizes IEEE + high-impact works, no API key required):
   `python _research_tool/research_agent.py --query "<primary academic query>" --counter-query "<counter/limitation query>" --min-ieee 10`

3. **Inspect Evidence**:
   Inspect the extracted literature records at:
   - `_research_tool/literature/summary.md`
   - `_research_tool/literature/references.bib`
   - `_research_tool/literature/metadata.json`

4. **Synthesize & Hyperlink in Markdown**:
   Antigravity acts as the Lead Scientist to synthesize findings, address dual perspectives, and generate Markdown reports following these citation linking rules:
   - **Internal Anchor Links**: Do NOT leave bare `\cite{...}` in Markdown prose. Instead, format in-text citations as clickable Markdown anchor links: `([Author et al., Year](#ref-citekey))`.
   - **Interactive Reference List**: Include a dedicated `## References` section at the end of the Markdown document where each entry has an anchor tag `<a id="ref-citekey"></a>` along with direct hyperlinks to the paper's DOI, publisher page, and open-access PDF.
   - **LaTeX Snippet**: Always provide an optional standalone LaTeX `\section{Related Work}` block with standard `\cite{citekey}` commands for easy copy-pasting into `.tex` manuscripts.
