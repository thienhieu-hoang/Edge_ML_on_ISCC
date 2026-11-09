# Project Research & Execution Plan (PLAN.md)

> **Core Philosophy**: **First-Principles & Mathematics First**. 
> Agents must NEVER naively propose generic machine learning or black-box methods without demonstrating mathematical compatibility with the underlying system (e.g., governing equations, dimensional constraints, conservation laws, asymptotic extremes, or physical/structural invariants).

---

## 0. Problem Formulation & System Invariants

### A. Mathematical Formulation
- **Governing Equation / Objective**: [e.g., System model $\mathbf{y} = \mathcal{A}(\mathbf{x}) + \mathbf{n}$, or optimization problem $\min_{\mathbf{x}} f(\mathbf{x}) \text{ s.t. } g(\mathbf{x}) \le 0$]
- **Target Variable / Deliverable**: [State vector, control policy, reconstructed field, or optimization variable]
- **Structural Properties & Invariants**:
  - Resolution / Sampling Scale: [Discretization grid, temporal/spatial sampling limits, Nyquist bounds]
  - Algebraic / Geometric Invariants: [Symmetry, positive semi-definiteness, conservation laws, unitary constraints]
  - Dimensionality & Sparsity: [Input/output dimensions, degrees of freedom, sparsity regime]

### B. Baselines & Theoretical Limits
- **Classical / Analytical Baseline**: [Simple classical estimator, convex relaxation, greedy heuristic, or standard benchmark]
- **Theoretical Bound / Optimal Ceiling**: [Bayes optimal error, Cramér-Rao Bound, dual bound, or oracle benchmark]
- **Asymptotic & Regime Constraints**:
  - Low-Signal / Extreme Noise Regime: [Must filter noise robustly; must not diverge]
  - High-Signal / Asymptotic Limit: [Zero-error-floor or graceful convergence; must track or beat classical baselines]

---

## 1. Round 1: Theory-Driven Candidate Approaches

> **Proposal Gatekeeper**: Every approach must pass the **First-Principles Feasibility Check**. Any proposal that merely transfers an off-the-shelf deep learning or black-box technique without mapping its inductive bias to the problem's mathematical structure will be REJECTED.

| ID | Approach Name | Mathematical / Structural Rationale | Why Generic Black-Box ML Fails Here | Remote Branch / PR | Status | Summary Metrics |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A1** | [Name] | [Inductive bias, structural embedding, or residual formulation] | [Explain failure of naive unconstrained models] | `exp/r1-a1` | `Proposed` | `Pending` |
| **A2** | [Name] | [Domain-informed parameter estimation, decomposition, or physics priors] | [Dimensional or resolution mismatch of generic models] | `exp/r1-a2` | `Proposed` | `Pending` |

*(Status: `Proposed` | `Running` | `Validated (Potential Winner)` | `Degraded (Ablation Asset)` | `Crashed`)*

### Mathematical Specifications (Written by Proposer Agent)

#### Approach A1: [Name]
- **Mathematical Rationale**:
  - *Formulation / Architecture*: [Equations, inductive bias, constraint projection, or residual formulation].
  - *Domain Invariants*: [How does this guarantee physical/mathematical consistency?].
- **Anti-Hallucination Proof**: [Why is this mathematically sound rather than a brute-force black box?].
- **Execution Script**: `python run_benchmark.py --model a1 --seed 0,1,2`
- **Output Artifacts**: `results/r1_a1/result.json`
- **Worklog Detail Link**: `[Detailed Log](./helperWorklog/details_YYMMDD-HHMM.md)`

#### Approach A2: [Name]
- **Mathematical Rationale**:
  - *Formulation / Architecture*: [Equations, inductive bias, constraint projection, or residual formulation].
  - *Domain Invariants*: [How does this guarantee physical/mathematical consistency?].
- **Anti-Hallucination Proof**: [Why is this mathematically sound rather than a brute-force black box?].
- **Execution Script**: `python run_benchmark.py --model a2 --seed 0,1,2`
- **Output Artifacts**: `results/r1_a2/result.json`
- **Worklog Detail Link**: `[Detailed Log](./helperWorklog/details_YYMMDD-HHMM.md)`

---

## 2. Round 1 Review & Mathematical Root-Cause Audit (Written by Reviewer Agent)

> **Reviewer Protocol**: Reviewer must audit candidate behaviors using rigorous mathematics and system constraints. Never conclude with superficial explanations (e.g., "loss did not converge"). Always identify the structural cause.

- **Date of Review**: [YYYY-MM-DD]
- **Asymptotic Performance vs Baselines**:
  - Low-Signal / Stressed Regime: [Did it beat the classical baseline?]
  - High-Signal / Asymptotic Limit: [Did it saturate or suffer from an artificial error floor? Why?]
- **Mathematical Failure Diagnosis**:
  - *Algebraic / Rank Degeneracy*: [Did matrix projections, transformations, or attention collapse in rank?]
  - *Resolution / Discretization Mismatch*: [Were features lost due to bin size, spatial/temporal discretization, or over-smoothing?]
  - *Constraint / Domain Misspecification*: [Were governing physical, conservation, or boundary constraints violated?]
- **Ablation Value for Deliverable**:
  - [How this negative result proves why naive/generic techniques fail on this specific scientific problem].
- **Round 1 Verdict & Pivot Strategy**:
  - Retain: [Champion candidate to advance]
  - Archive: [Degraded branches preserved on GitHub as ablation evidence]
  - Round 2 Directive: [What mathematical correction or structural inductive bias must be introduced?]

---

## 3. Round 2: Refined Domain-Informed Approaches

| ID | Refined Approach | Mathematical Correction Applied | Remote Branch / PR | Status | Final Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B1** | [Refined Champion] | [Structural fix: e.g., expanded receptive field, projection onto constraint set, residual link] | `exp/r2-b1` | `Proposed` | `Pending` |
| **B2** | [Analytical Fallback] | [Hybrid solver combining classical optimization with learned acceleration] | `exp/r2-b2` | `Proposed` | `Pending` |

### Detailed Specifications (Round 2)
#### Refined Approach B1: [Name]
- **Mathematical Fix**: [Exact mathematical improvement made to eliminate the Round 1 bottleneck]
- **Execution Script**: `python run_benchmark.py --model b1 --seed 0,1,2`
- **Target Milestone**: [Metrics required to outperform both baselines and prior limits]
- **Worklog Detail Link**: `[Detailed Log](./helperWorklog/details_YYMMDD-HHMM.md)`

---

## 4. Final Champion Selection & Mainline Merge
- **Champion Model**: [e.g., B1 on branch `exp/r2-b1`]
- **Core Scientific / Technical Contribution**:
  - [Concise 3-bullet summary of the breakthrough for publications or technical reports].
- **Mainline Integration**:
  - `git checkout main && git merge exp/r2-b1 && git push origin main`
- **Ablation Archive**:
  - All non-champion branches remain preserved on remote GitHub for ablation study citations and reviewer defense.
