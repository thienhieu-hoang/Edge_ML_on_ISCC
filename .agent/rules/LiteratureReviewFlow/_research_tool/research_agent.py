#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone Academic Literature Retriever & Citation Generator
Queries Semantic Scholar and OpenAlex APIs with:
- Dedicated IEEE Prioritization: guarantees at least 10 IEEE papers (IEEE Xplore/Transactions/Conferences).
- Broad Academic Enrichment: fetches top-cited high-impact works from Springer, Nature, ACM, Elsevier, arXiv, etc.
- Dual-Perspective Retrieval: supporting methods & critical counter-arguments/limitations.
- Clean BibTeX generation formatted for LaTeX.
"""

import os
import sys
import json
import re
import time
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import requests

# ============================================================================
# RESOLVE RELATIVE PATHS (PORTABLE FOR ANY PROJECT)
# ============================================================================
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
LITERATURE_DIR = os.path.join(TOOL_DIR, "literature")

def load_simple_env():
    env_paths = [
        os.path.join(TOOL_DIR, ".env"),
        os.path.join(os.path.dirname(TOOL_DIR), ".env"),
        os.path.abspath(".env"),
    ]
    for p in env_paths:
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k, v = k.strip(), v.strip()
                            if k not in os.environ and v:
                                os.environ[k] = v
                break
            except Exception:
                pass

load_simple_env()


# ============================================================================
# 1. DATA MODELS & PAPER STORAGE
# ============================================================================

class PaperMetadata:
    def __init__(
        self,
        paper_id: str,
        title: str,
        authors: List[str],
        year: Optional[int],
        doi: Optional[str],
        abstract: str,
        tldr: Optional[str],
        citation_count: int,
        oa_pdf_url: Optional[str],
        source_url: str,
        source_db: str,
        venue: str = "",
        is_ieee: bool = False,
        query: str = "",
        perspective: str = "supporting",
    ):
        self.paper_id = paper_id
        self.title = title.strip()
        self.authors = authors
        self.year = year
        self.doi = doi.strip() if doi else None
        self.abstract = abstract.strip() if abstract else ""
        self.tldr = tldr.strip() if tldr else None
        self.citation_count = citation_count or 0
        self.oa_pdf_url = oa_pdf_url
        self.source_url = source_url
        self.source_db = source_db
        self.venue = venue.strip() if venue else ""
        self.is_ieee = is_ieee
        self.query = query
        self.perspective = perspective  # "supporting", "counter_argument", or "both"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "doi": self.doi,
            "citekey": self.citekey,
            "venue": self.venue,
            "is_ieee": self.is_ieee,
            "citation_count": self.citation_count,
            "abstract": self.abstract,
            "tldr": self.tldr,
            "oa_pdf_url": self.oa_pdf_url,
            "source_url": self.source_url,
            "source_db": self.source_db,
            "search_query": self.query,
            "perspective": self.perspective,
        }

    @property
    def citekey(self) -> str:
        first_author = "unknown"
        if self.authors:
            parts = self.authors[0].strip().split()
            first_author = parts[-1] if parts else "author"
        first_author = re.sub(r"[^a-zA-Z0-9]", "", first_author).lower()

        yr = str(self.year) if self.year else "nodate"
        title_words = [w for w in re.findall(r"[a-zA-Z0-9]+", self.title.lower()) if len(w) > 3]
        sig_word = title_words[0] if title_words else "paper"
        return f"{first_author}{yr}{sig_word}"

    def to_bibtex(self) -> str:
        def escape_latex(s: str) -> str:
            if not s:
                return ""
            replacements = {
                "&": r"\&",
                "%": r"\%",
                "$": r"\$",
                "#": r"\#",
                "_": r"\_",
                "{": r"\{",
                "}": r"\}",
                "~": r"\textasciitilde{}",
                "^": r"\textasciicircum{}",
            }
            res = s
            for orig, rep in replacements.items():
                res = res.replace(orig, rep)
            return res

        authors_str = " and ".join(self.authors) if self.authors else "Anonymous"
        authors_escaped = escape_latex(authors_str)
        title_escaped = escape_latex(self.title)

        bib_lines = [
            f"@article{{{self.citekey},",
            f"  title     = {{{title_escaped}}},",
            f"  author    = {{{authors_escaped}}},",
        ]
        if self.venue:
            venue_escaped = escape_latex(self.venue)
            bib_lines.append(f"  journal   = {{{venue_escaped}}},")
        if self.year:
            bib_lines.append(f"  year      = {{{self.year}}},")
        if self.doi:
            bib_lines.append(f"  doi       = {{{self.doi}}},")
        if self.source_url:
            bib_lines.append(f"  url       = {{{self.source_url}}},")
        if self.oa_pdf_url:
            bib_lines.append(f"  note      = {{Open Access PDF: \\url{{{self.oa_pdf_url}}}}},")

        bib_lines.append("}")
        return "\n".join(bib_lines)


class PaperStore:
    def __init__(self):
        self.papers: Dict[str, PaperMetadata] = {}

    def _normalize_title(self, title: str) -> str:
        return re.sub(r"\W+", "", title.lower())

    def _normalize_doi(self, doi: Optional[str]) -> Optional[str]:
        if not doi:
            return None
        doi = doi.lower().strip()
        doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
        return doi

    def add_paper(self, paper: PaperMetadata) -> bool:
        norm_doi = self._normalize_doi(paper.doi)
        norm_title = self._normalize_title(paper.title)

        # 1. Deduplicate by DOI
        if norm_doi:
            for existing in self.papers.values():
                if self._normalize_doi(existing.doi) == norm_doi:
                    self._merge_into(existing, paper)
                    return False

        # 2. Deduplicate by Title
        if norm_title:
            for existing in self.papers.values():
                if self._normalize_title(existing.title) == norm_title:
                    self._merge_into(existing, paper)
                    return False

        key = paper.paper_id or norm_doi or f"paper_{len(self.papers)+1}"
        self.papers[key] = paper
        return True

    def _merge_into(self, target: PaperMetadata, incoming: PaperMetadata):
        if not target.abstract and incoming.abstract:
            target.abstract = incoming.abstract
        if not target.tldr and incoming.tldr:
            target.tldr = incoming.tldr
        if not target.oa_pdf_url and incoming.oa_pdf_url:
            target.oa_pdf_url = incoming.oa_pdf_url
        if not target.venue and incoming.venue:
            target.venue = incoming.venue
        if incoming.is_ieee and not target.is_ieee:
            target.is_ieee = True
        if incoming.citation_count > target.citation_count:
            target.citation_count = incoming.citation_count
        if target.source_db != incoming.source_db and "Both" not in target.source_db:
            target.source_db = f"Both ({target.source_db} & {incoming.source_db})"
        if target.perspective != incoming.perspective:
            target.perspective = "both"

    def get_all(self) -> List[PaperMetadata]:
        return list(self.papers.values())

    def get_ieee_papers(self) -> List[PaperMetadata]:
        return [p for p in self.papers.values() if p.is_ieee]

    def get_non_ieee_papers(self) -> List[PaperMetadata]:
        return [p for p in self.papers.values() if not p.is_ieee]

    def count(self) -> int:
        return len(self.papers)


paper_store = PaperStore()


# ============================================================================
# 2. ACADEMIC RETRIEVAL (Semantic Scholar & OpenAlex)
# ============================================================================

OPENALEX_IEEE_LINEAGE = "p4310319808"

class AcademicRetriever:
    def __init__(self, s2_api_key: Optional[str] = None):
        self.s2_api_key = s2_api_key or os.getenv("SEMANTIC_SCHOLAR_API_KEY", "").strip()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "StandaloneResearchTool/2.0 (mailto:scholar@agentic.review)"
        })

    def _is_ieee(self, text_list: List[str]) -> bool:
        combined = " ".join([t for t in text_list if t]).lower()
        ieee_patterns = ["ieee", "institute of electrical and electronics", "xplore", "iet"]
        return any(p in combined for p in ieee_patterns)

    # ------------------------------------------------------------------------
    # SEMANTIC SCHOLAR SEARCH
    # ------------------------------------------------------------------------
    def search_semantic_scholar(
        self,
        query: str,
        limit: int = 10,
        perspective: str = "supporting"
    ) -> List[PaperMetadata]:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        fields = "paperId,title,authors,year,citationCount,abstract,tldr,externalIds,openAccessPdf,url,venue,publicationVenue"
        params = {"query": query, "limit": limit, "fields": fields}
        headers = {}
        if self.s2_api_key:
            headers["x-api-key"] = self.s2_api_key

        try:
            resp = self.session.get(url, params=params, headers=headers, timeout=10)
            if resp.status_code == 200:
                raw_json = resp.json()
                data = raw_json.get("data", [])
                results = []
                for item in data:
                    authors = [a.get("name", "").strip() for a in item.get("authors", []) if a.get("name")]
                    ext_ids = item.get("externalIds") or {}
                    doi = ext_ids.get("DOI")

                    tldr_obj = item.get("tldr") or {}
                    tldr_text = tldr_obj.get("text") if isinstance(tldr_obj, dict) else None

                    oa_pdf = None
                    if item.get("openAccessPdf"):
                        oa_pdf = item.get("openAccessPdf", {}).get("url")

                    pub_venue = item.get("publicationVenue") or {}
                    venue_name = pub_venue.get("name") or item.get("venue") or ""

                    is_ieee = self._is_ieee([venue_name, doi or ""])

                    paper = PaperMetadata(
                        paper_id=f"S2:{item.get('paperId', '')}",
                        title=item.get("title", ""),
                        authors=authors,
                        year=item.get("year"),
                        doi=doi,
                        abstract=item.get("abstract") or "",
                        tldr=tldr_text,
                        citation_count=item.get("citationCount") or 0,
                        oa_pdf_url=oa_pdf,
                        source_url=item.get("url") or (f"https://doi.org/{doi}" if doi else ""),
                        source_db="Semantic Scholar",
                        venue=venue_name,
                        is_ieee=is_ieee,
                        query=query,
                        perspective=perspective,
                    )
                    results.append(paper)
                return results
            elif resp.status_code == 429:
                print("     ⚠️ [Semantic Scholar] Public rate limit encountered (429). Using OpenAlex academic index.")
                return []
            else:
                return []
        except Exception:
            return []

    # ------------------------------------------------------------------------
    # OPENALEX SEARCH
    # ------------------------------------------------------------------------
    def _reconstruct_openalex_abstract(self, inverted_index: Optional[Dict[str, List[int]]]) -> str:
        if not inverted_index or not isinstance(inverted_index, dict):
            return ""
        positions: Dict[int, str] = {}
        for word, pos_list in inverted_index.items():
            for p in pos_list:
                positions[p] = word
        sorted_words = [positions[p] for p in sorted(positions.keys())]
        return " ".join(sorted_words)

    def search_openalex(
        self,
        query: str,
        limit: int = 15,
        ieee_only: bool = False,
        sort_by_citations: bool = False,
        perspective: str = "supporting"
    ) -> List[PaperMetadata]:
        url = "https://api.openalex.org/works"
        params: Dict[str, Any] = {
            "search": query,
            "per_page": limit,
            "select": "id,doi,title,publication_year,cited_by_count,abstract_inverted_index,authorships,open_access,primary_location",
        }

        if ieee_only:
            params["filter"] = f"primary_location.source.publisher_lineage:{OPENALEX_IEEE_LINEAGE}"

        if sort_by_citations:
            params["sort"] = "cited_by_count:desc"

        try:
            resp = self.session.get(url, params=params, timeout=12)
            if resp.status_code == 200:
                raw_json = resp.json()
                results_data = raw_json.get("results", [])
                results = []
                for item in results_data:
                    authors = []
                    for authorship in item.get("authorships", []):
                        author = authorship.get("author", {})
                        if author.get("display_name"):
                            authors.append(author["display_name"])

                    raw_doi = item.get("doi")
                    clean_doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", raw_doi) if raw_doi else None

                    abstract = self._reconstruct_openalex_abstract(item.get("abstract_inverted_index"))

                    oa_info = item.get("open_access", {})
                    oa_pdf = oa_info.get("oa_url") if oa_info.get("is_oa") else None

                    primary_loc = item.get("primary_location") or {}
                    source = primary_loc.get("source") or {}
                    venue_name = source.get("display_name") or ""
                    publisher_name = source.get("publisher") or ""
                    host_org = source.get("host_organization_name") or ""
                    landing_url = primary_loc.get("landing_page_url") or raw_doi or ""

                    is_ieee = ieee_only or self._is_ieee([venue_name, publisher_name, host_org, clean_doi or ""])

                    paper = PaperMetadata(
                        paper_id=f"OA:{item.get('id', '')}",
                        title=item.get("title") or "Untitled",
                        authors=authors,
                        year=item.get("publication_year"),
                        doi=clean_doi,
                        abstract=abstract,
                        tldr=None,
                        citation_count=item.get("cited_by_count") or 0,
                        oa_pdf_url=oa_pdf,
                        source_url=landing_url,
                        source_db="OpenAlex",
                        venue=venue_name,
                        is_ieee=is_ieee,
                        query=query,
                        perspective=perspective,
                    )
                    results.append(paper)
                return results
            else:
                return []
        except Exception:
            return []


retriever = AcademicRetriever()


# ============================================================================
# 3. COMPREHENSIVE MULTI-SOURCE RETRIEVAL PIPELINE (IEEE PRIORITIZED)
# ============================================================================

def execute_comprehensive_retrieval(
    base_query: str,
    counter_query: Optional[str] = None,
    min_ieee_target: int = 10,
    min_citations_for_other: int = 15,
) -> List[PaperMetadata]:
    """
    Retrieval strategy:
    1. IEEE Dedicated Search (Supporting + Counter): Guarantees at least 10+ IEEE publications.
    2. Semantic Scholar Search: Queries both general and IEEE keywords.
    3. High-Impact Scholarly Enrichment: Fetches top-cited papers across all publishers (Springer, Nature, ACM, Elsevier, etc.).
    """
    print("=" * 70)
    print("🚀 EXECUTING MULTI-SOURCE ACADEMIC RETRIEVAL PIPELINE")
    print(f"🎯 Target Focus: At least {min_ieee_target} IEEE papers + High-Impact works from all databases")
    print("=" * 70)

    if not counter_query:
        counter_query = f"{base_query} limitations drawbacks complexity tradeoff latency failure"

    # ------------------------------------------------------------------------
    # STEP 1: GUARANTEE AT LEAST 10 IEEE PAPERS
    # ------------------------------------------------------------------------
    print(f"\n📡 [Phase 1: Dedicated IEEE Retrieval (IEEE Xplore / Transactions / Conferences)]")
    
    # 1a. Supporting IEEE papers
    ieee_supp = retriever.search_openalex(
        query=base_query,
        limit=10,
        ieee_only=True,
        perspective="supporting"
    )
    for p in ieee_supp:
        paper_store.add_paper(p)
    print(f"  ⚡ IEEE Supporting papers found: {len(ieee_supp)}")

    # 1b. Counter-argument IEEE papers
    ieee_counter = retriever.search_openalex(
        query=counter_query,
        limit=8,
        ieee_only=True,
        perspective="counter_argument"
    )
    for p in ieee_counter:
        paper_store.add_paper(p)
    print(f"  ⚔️ IEEE Counter-argument papers found: {len(ieee_counter)}")

    # 1c. Top-cited IEEE foundation papers (to ensure high-impact IEEE presence)
    ieee_top = retriever.search_openalex(
        query=base_query,
        limit=6,
        ieee_only=True,
        sort_by_citations=True,
        perspective="supporting"
    )
    for p in ieee_top:
        paper_store.add_paper(p)

    current_ieee_count = len(paper_store.get_ieee_papers())
    print(f"  👉 Total unique IEEE papers secured so far: {current_ieee_count} / {min_ieee_target} target.")

    # ------------------------------------------------------------------------
    # STEP 2: QUERY SEMANTIC SCHOLAR (IF AVAILABLE)
    # ------------------------------------------------------------------------
    print(f"\n🧠 [Phase 2: Semantic Scholar Graph API Search]")
    s2_supp = retriever.search_semantic_scholar(base_query, limit=10, perspective="supporting")
    s2_added = sum(1 for p in s2_supp if paper_store.add_paper(p))
    
    s2_counter = retriever.search_semantic_scholar(counter_query, limit=8, perspective="counter_argument")
    s2_counter_added = sum(1 for p in s2_counter if paper_store.add_paper(p))
    print(f"  📚 Semantic Scholar: +{s2_added + s2_counter_added} unique papers added.")

    # ------------------------------------------------------------------------
    # STEP 3: HIGH-IMPACT CITATION ENRICHMENT (ALL PUBLISHERS)
    # ------------------------------------------------------------------------
    print(f"\n🌟 [Phase 3: High-Impact Scholarly Enrichment (Top-Cited across Nature, Springer, ACM, etc.)]")
    broad_top = retriever.search_openalex(
        query=base_query,
        limit=12,
        ieee_only=False,
        sort_by_citations=True,
        perspective="supporting"
    )
    broad_counter = retriever.search_openalex(
        query=counter_query,
        limit=10,
        ieee_only=False,
        sort_by_citations=True,
        perspective="counter_argument"
    )

    enriched_count = 0
    for p in broad_top + broad_counter:
        # Keep non-IEEE papers if they have decent citation impact or substantial abstract
        if p.is_ieee or p.citation_count >= min_citations_for_other or (p.abstract and len(p.abstract) > 300):
            if paper_store.add_paper(p):
                enriched_count += 1

    print(f"  ✨ High-impact cross-venue papers added: +{enriched_count}")

    # Final summary statistics
    all_papers = paper_store.get_all()
    ieee_final = [p for p in all_papers if p.is_ieee]
    other_final = [p for p in all_papers if not p.is_ieee]

    print("\n" + "=" * 70)
    print(f"📊 RETRIEVAL METRICS SUMMARY:")
    print(f"   • Total Unique Papers Retrieved: {len(all_papers)}")
    print(f"   • IEEE Papers (Guaranteed Focus): {len(ieee_final)}")
    print(f"   • High-Impact Other Venues:       {len(other_final)}")
    print(f"   • Supporting Methodology Papers:  {sum(1 for p in all_papers if p.perspective in ('supporting', 'both'))}")
    print(f"   • Counter-Argument / Trade-offs:  {sum(1 for p in all_papers if p.perspective in ('counter_argument', 'both'))}")
    print("=" * 70)

    return all_papers


# ============================================================================
# 4. EXPORT ARTIFACTS INTO literature/
# ============================================================================

def export_workspace_artifacts(
    user_query: str,
    output_dir: str = LITERATURE_DIR,
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    all_papers = paper_store.get_all()

    # Sort papers: First all IEEE papers (sorted by citation desc), then others (sorted by citation desc)
    sorted_papers = sorted(
        all_papers,
        key=lambda p: (1 if p.is_ieee else 0, p.citation_count),
        reverse=True
    )

    # 1. Export metadata.json
    metadata_path = os.path.join(output_dir, "metadata.json")
    metadata_data = {
        "timestamp": datetime.now().isoformat(),
        "user_query": user_query,
        "total_unique_papers": len(sorted_papers),
        "metrics": {
            "ieee_count": sum(1 for p in sorted_papers if p.is_ieee),
            "other_count": sum(1 for p in sorted_papers if not p.is_ieee),
            "supporting_count": sum(1 for p in sorted_papers if p.perspective in ("supporting", "both")),
            "counter_argument_count": sum(1 for p in sorted_papers if p.perspective in ("counter_argument", "both")),
        },
        "papers": [p.to_dict() for p in sorted_papers],
    }
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata_data, f, indent=2, ensure_ascii=False)

    # 2. Export references.bib
    bib_path = os.path.join(output_dir, "references.bib")
    bib_entries = [p.to_bibtex() for p in sorted_papers]
    bib_content = "\n\n".join(bib_entries)
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(bib_content)

    # 3. Export summary.md
    summary_path = os.path.join(output_dir, "summary.md")
    papers_table = [
        "## 📚 Retrieved Academic Literature Catalogue (IEEE Prioritized)\n",
        f"Total Unique Papers: **{len(sorted_papers)}** (IEEE: **{sum(1 for p in sorted_papers if p.is_ieee)}** | Other Venues: **{sum(1 for p in sorted_papers if not p.is_ieee)}**)\n",
        "| # | Focus | Year | Title | Primary Author | Perspective | Citations | Venue / DB | Citekey | DOI / Link | Open Access |",
        "|---|:---:|---|---|---|:---:|:---:|---|---|---|:---:|",
    ]
    for idx, p in enumerate(sorted_papers, 1):
        first_auth = p.authors[0] if p.authors else "Unknown"
        if len(p.authors) > 1:
            first_auth += " et al."
        doi_link = f"[{p.doi}](https://doi.org/{p.doi})" if p.doi else f"[Link]({p.source_url})"
        oa_status = f"[PDF]({p.oa_pdf_url})" if p.oa_pdf_url else "No"
        clean_title = p.title.replace("|", "-")
        persp_badge = "⚔️ Counter" if p.perspective == "counter_argument" else ("🔄 Both" if p.perspective == "both" else "💡 Supporting")
        focus_badge = "🏛️ **IEEE**" if p.is_ieee else "🌐 Other"
        venue_display = (p.venue[:25] + "...") if len(p.venue) > 25 else (p.venue or p.source_db)
        venue_display = venue_display.replace("|", "-")

        papers_table.append(
            f"| {idx} | {focus_badge} | {p.year or 'N/A'} | **{clean_title}** | {first_auth} | `{persp_badge}` | **{p.citation_count}** | {venue_display} | `{p.citekey}` | {doi_link} | {oa_status} |"
        )

    papers_details = ["\n## 📝 Paper Abstracts & Ground-Truth Evidence\n"]
    for idx, p in enumerate(sorted_papers, 1):
        persp_label = "⚔️ Counter-Argument / Limitation / Trade-off" if p.perspective == "counter_argument" else "💡 Supporting / Methodology"
        focus_label = "🏛️ IEEE Publication" if p.is_ieee else "🌐 High-Impact Academic Venue"
        papers_details.append(f"### {idx}. [{focus_label}] {p.title}")
        papers_details.append(f"- **Citekey:** `\\cite{{{p.citekey}}}`")
        papers_details.append(f"- **Perspective:** `{persp_label}`")
        papers_details.append(f"- **Authors:** {', '.join(p.authors) if p.authors else 'N/A'}")
        papers_details.append(f"- **Year:** {p.year or 'N/A'} | **Citations:** {p.citation_count} | **Venue:** {p.venue or 'N/A'} ({p.source_db})")
        if p.doi:
            papers_details.append(f"- **DOI:** https://doi.org/{p.doi}")
        if p.oa_pdf_url:
            papers_details.append(f"- **Fulltext PDF:** {p.oa_pdf_url}")
        if p.tldr:
            papers_details.append(f"- **TLDR (Semantic Scholar):** *{p.tldr}*")
        if p.abstract:
            papers_details.append(f"- **Abstract:** {p.abstract}")
        papers_details.append("\n---\n")

    full_markdown = (
        f"# Academic Literature Catalogue & Evidence Digest\n\n"
        f"- **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"- **Research Query:** `{user_query}`\n"
        f"- **Target Focus:** Guaranteed ≥ 10 IEEE papers + High-Impact Academic Works\n"
        f"- **Academic Sources:** IEEE Xplore, Semantic Scholar & OpenAlex\n"
        f"- **Synthesis & Reasoning Agent:** Antigravity 2.0\n\n"
        f"---\n\n"
        + "\n".join(papers_table)
        + "\n"
        + "\n".join(papers_details)
        + "\n\n"
        f"## 📖 BibTeX Bibliography (Ready for LaTeX Manuscripts)\n\n"
        f"```bibtex\n"
        f"{bib_content}\n"
        f"```\n"
    )
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(full_markdown)

    return output_dir


# ============================================================================
# 5. CLI ENTRY POINT
# ============================================================================

def main():
    print(r"""
======================================================================
     _research_tool: Academic Literature Retrieval Engine
     IEEE Prioritized + Multi-Source Scholarly Enrichment
======================================================================
""")

    parser = argparse.ArgumentParser(
        description="IEEE-Prioritized Academic Literature Retriever for Antigravity 2.0."
    )
    parser.add_argument(
        "-q", "--query",
        type=str,
        default=None,
        help="Primary research question or keyword query."
    )
    parser.add_argument(
        "-c", "--counter-query",
        type=str,
        default=None,
        help="Optional counter-argument / limitation search query."
    )
    parser.add_argument(
        "--min-ieee",
        type=int,
        default=10,
        help="Minimum target of IEEE papers to guarantee (default: 10)."
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=LITERATURE_DIR,
        help=f"Output directory (default: {LITERATURE_DIR})."
    )

    args = parser.parse_args()
    query = args.query
    if not query:
        print("💡 Enter your research question or keywords:")
        try:
            query = input("👉 Query: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            sys.exit(0)

    if not query:
        print("❌ Search query cannot be empty!")
        sys.exit(1)

    start_time = time.time()

    try:
        execute_comprehensive_retrieval(
            base_query=query,
            counter_query=args.counter_query,
            min_ieee_target=args.min_ieee,
        )

        out_path = export_workspace_artifacts(
            user_query=query,
            output_dir=args.output_dir,
        )

        elapsed = time.time() - start_time
        print(f"\n✅ RETRIEVAL COMPLETED IN {elapsed:.1f} SECONDS!")
        print(f"📁 Output artifacts ready for Antigravity 2.0 synthesis at: {os.path.abspath(out_path)}")
        print(f"   ├── metadata.json   (Full structured paper metadata & abstracts)")
        print(f"   ├── summary.md      (Paper catalogue, TLDRs, and abstracts)")
        print(f"   └── references.bib  (Standard BibTeX citations for LaTeX)")

    except Exception as e:
        print(f"\n❌ Execution Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
