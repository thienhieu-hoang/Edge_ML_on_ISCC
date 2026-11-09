# Standard 2-Column LaTeX Template (`IEEEtran`)

This document defines the mandatory 2-column LaTeX structure and preamble configurations for all technical notes, simulation reports, and manuscript draft `.tex` files in this repository.

---

## 1. Core Structure & Guidelines

1. **Document Class & Layout:**
   - Always use `\documentclass[journal]{IEEEtran}` (standard 2-column format).
2. **Graphics & Tables:**
   - Use `\graphicspath{{./Figures/}}` for figure assets.
   - Use `tabularx`, `booktabs`, `multirow`, and `makecell` for clean, professional IEEE-style tables.
3. **Units & Notation:**
   - Always use `siunitx` for units (e.g., `\SI{2.0}{\giga\hertz}`, `\SI{30}{\mega\hertz}`, `\SI{0}{\decibel}`).
4. **Action Items & Notes:**
   - Use `\Todoitem{Category}{Task description}` for action items.
   - Use custom color commands (`\tnd{}`, `\note{}`, `\fromAI{}`) and `tcolorbox` blocks for revision notes.

---

## 2. Standard Boilerplate Template

```latex
\documentclass[journal]{IEEEtran}

% ============================================================
% 1. PACKAGES
% ============================================================
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=black, urlcolor=black, citecolor=black}

\usepackage{ifpdf}
\ifCLASSINFOpdf
  \usepackage[pdftex]{graphicx}
  \graphicspath{{./Figures/}}
  \DeclareGraphicsExtensions{.pdf,.jpeg,.png}
\else
  \usepackage[dvips]{graphicx}
  \DeclareGraphicsExtensions{.pdf}
  \usepackage{svg}
  \usepackage[caption=false, font=footnotesize]{subfig}
\fi

\usepackage{xcolor}
\usepackage{tabularx, booktabs}
\usepackage{amssymb}
\usepackage{amsthm}
\usepackage[ruled,vlined,linesnumbered]{algorithm2e}
\usepackage{aligned-overset}
\usepackage{array}
\usepackage{balance}
\usepackage{cite}
\usepackage{color}
\usepackage{epstopdf}
\usepackage{enumitem}
\usepackage{mathtools}
\usepackage{makecell}
\usepackage{multicol}
\usepackage{multirow}
\usepackage[caption=false,font=small]{subfig}
\usepackage{textcomp}
\usepackage{stfloats}
\usepackage{url}
\usepackage{verbatim}
\usepackage{siunitx}
\usepackage{listings}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}

% ============================================================
% 2. THEOREMS, ENVIRONMENTS & MACROS
% ============================================================
\newtheorem{lemma}{Lemma}
\newtheorem{theorem}{Theorem}
\newtheorem{claim}{Claim}
\newtheorem{definition}{Definition}
\newtheorem{observation}{Observation}
\newtheorem{proposition}{Proposition}
\newtheorem{assumption}{Assumption}
\newtheorem{remark}{Remark}
\newtheorem{corollary}{Corollary}

\definecolor{blue}{RGB}{0, 102, 204}
\definecolor{red}{RGB}{204, 0, 0}
\definecolor{green}{RGB}{0, 153, 0}
\definecolor{purple}{RGB}{102, 51, 153}

\newcommand{\tnd}[1]{{\color{red}\noindent{#1}}}
\newcommand{\note}[1]{{\fontfamily{cmss}\selectfont\color{green}\noindent{#1}}}
\newcommand{\fromAI}[1]{{\color{purple}\noindent{#1}}}

\newtcolorbox{originalbox}{
  colback=gray!10, colframe=gray!50, 
  title=\textbf{Original}, fonttitle=\small
}
\newtcolorbox{revisedbox}{
  colback=blue!5, colframe=blue!50, 
  title=\textbf{Revised}, fonttitle=\small
}

\newcommand{\Todoitem}[2]{%
\begin{tcolorbox}[breakable, enhanced,
  colback=yellow!12, colframe=yellow!70!black,
  title={\textbf{TODO [#1]}}, fonttitle=\footnotesize]
\footnotesize\color{black} #2%
\end{tcolorbox}}

% ============================================================
% 3. DOCUMENT BODY
% ============================================================
\begin{document}

\title{Document Title: Simulation Notes or Report}

\author{Thien~Hieu~Hoang, Tri~Nhu~Do, and~Georges~Kaddoum
\thanks{Author affiliations and notes.}
}

\maketitle

\begin{abstract}
Summary of the simulation setup, mathematical models, or empirical findings.
\end{abstract}

\begin{IEEEkeywords}
Non-Terrestrial Networks (NTN), Channel Estimation, Domain Adaptation, Simulation Notes.
\end{IEEEkeywords}

\section{Introduction / System Model}
\label{sec:system_model}
Description of system geometry, link parameters, or problem formulation.

\section{Channel Model & Mathematical Formulation}
\label{sec:channel_model}
\begin{equation}
    h(t, \tau) = \sum_{l=0}^{L-1} \alpha_l(t) e^{j 2\pi f_{\mathrm{D}, l} t} \delta(\tau - \tau_l(t)).
    \label{eq:channel}
\end{equation}

\section{Simulation Setup & Parameters}
\label{sec:simulation}

\begin{table}[htbp]
\centering
\caption{System Simulation Parameters}
\label{tab:params}
\begin{tabularx}{\columnwidth}{lX}
\toprule
\textbf{Parameter} & \textbf{Value} \\
\midrule
Carrier Frequency ($f_{\mathrm{c}}$) & \SI{2.0}{\giga\hertz} \\
Bandwidth ($B$)                     & \SI{30}{\mega\hertz} \\
Subcarriers ($K$)                   & 132 \\
OFDM Symbols ($N$)                  & 14 \\
\bottomrule
\end{tabularx}
\end{table}

\Todoitem{Simulation}{Add new simulation logs or figure comparisons here.}

\section{Results / Findings}
\label{sec:results}
Performance comparisons (NMSE, BER, convergence curves).

\section{Conclusion}
\label{sec:conclusion}
Summary of insights and next action items.

\bibliographystyle{IEEEtran}
% \bibliography{references}

\end{document}
```
