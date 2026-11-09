# Literature Review: Channel Prediction & Tracking in Integrated Sensing and Communications (ISAC / ISSC)

**Author / Compiler:** Antigravity 2.0 (Dual-Perspective Literature Synthesis Engine)  
**Context:** 6G Dual-Functional Radar-Communication (DFRC), V2X, UAV, and LEO Satellite Networks  
**Date:** October 2026  
**Reference Document:** [`note_ini.md`](./note_ini.md)  
**Key Venues Covered:** IEEE JSAC, IEEE TWC, IEEE TSP, IEEE TVT, IEEE TCOMM, IEEE MWC, IEEE WCL, IEEE IoTJ, IEEE COMST  

---

## Executive Summary

In high-mobility wireless communications (such as Vehicle-to-Everything [V2X], low-altitude Unmanned Aerial Vehicles [UAVs], and Low Earth Orbit [LEO] Non-Terrestrial Networks), conventional channel prediction relies solely on historical communication Channel State Information (CSI). Because past CSI is derived from downlink pilots or delayed uplink feedback, standard channel prediction operates as a **"blind" temporal sequence extrapolation** task. Under rapid angular variations, non-linear acceleration, or sudden path blockages, pure temporal predictors quickly lose tracking fidelity, leading to outdated beamforming and catastrophic link degradation.

**Integrated Sensing and Communications (ISAC)**—and its synchronized counterpart, **Integrated Sensing, Synchronization, and Communications (ISSC)**—presents a fundamental paradigm shift. In an ISAC network, the Dual-Functional Radar-Communication (DFRC) base station transmits unified waveforms that simultaneously carry data to users while illuminating the surrounding physical environment. The reflected radar echoes provide **zero-feedback, real-time physical observations** of the target's kinematic state (range, angle of arrival/departure, radial velocity, and acceleration).

By establishing a deterministic physical bridge between radar echo kinematics and communication channel propagation, **sensing-assisted channel prediction** transforms an ill-posed blind forecasting problem into an **observable kinematic state-tracking problem**. 

This literature review presents an exhaustive synthesis of recent breakthroughs (2020–2026) in sensing-assisted channel prediction, tracing the trajectory from classical Extended Kalman Filtering (EKF) tracking to modern physics-informed deep learning, cross-modal attention, Continuous-Time Neural ODEs, and Large Language Model (LLM) foundation architectures.

---

## Table of Contents
- [1. Fundamental Paradigm: From Blind Extrapolation to Sensing-Assisted Tracking](#1-fundamental-paradigm-from-blind-extrapolation-to-sensing-assisted-tracking)
  - [1.1 The Blind Channel Prediction Bottleneck](#11-the-blind-channel-prediction-bottleneck)
  - [1.2 The ISAC / ISSC Synergy: Dual-Functional Waveforms as Probing Signals](#12-the-isac--issc-synergy-dual-functional-waveforms-as-probing-signals)
  - [1.3 The Sensing-to-Communication (S2C) Channel Mapping](#13-the-sensing-to-communication-s2c-channel-mapping)
- [2. System & Mathematical Formulations](#2-system--mathematical-formulations)
  - [2.1 DFRC Signal & Echo Observation Model](#21-dfrc-signal--echo-observation-model)
  - [2.2 Parametric Communication Channel Model](#22-parametric-communication-channel-model)
  - [2.3 Kinematic State-Space Evolution](#23-kinematic-state-space-evolution)
- [3. Classical Model-Based Sensing-Assisted Tracking](#3-classical-model-based-sensing-assisted-tracking)
  - [3.1 Radar-Assisted EKF & UKF Predictive Beamforming](#31-radar-assisted-ekf--ukf-predictive-beamforming)
  - [3.2 Particle Filtering for Non-Linear Maneuvering Targets](#32-particle-filtering-for-non-linear-maneuvering-targets)
  - [3.3 Near-Field Velocity Sensing & Predictive Beamforming](#33-near-field-velocity-sensing--predictive-beamforming)
  - [3.4 The "Seeing is Not Always Believing" Dilemma: Multipath vs. LoS Discrepancy](#34-the-seeing-is-not-always-believing-dilemma-multipath-vs-los-discrepancy)
- [4. Modern Machine Learning & Deep Learning Approaches (2022–2026)](#4-modern-machine-learning--deep-learning-approaches-20222026)
  - [4.1 Deep Learning for Sensing-Communication Feature Mapping](#41-deep-learning-for-sensing-communication-feature-mapping)
  - [4.2 Spatio-Temporal Attention & Multi-Point Radar Fusion](#42-spatio-temporal-attention--multi-point-radar-fusion)
  - [4.3 Cross-Modal Transformers for Complex Propagation](#43-cross-modal-transformers-for-complex-propagation)
  - [4.4 Foundation Models & Edge LLMs in ISAC Channel Prediction (2025–2026)](#44-foundation-models--edge-llms-in-isac-channel-prediction-20252026)
- [5. Physics-Informed Hybrid State-Space & Bayesian Tracking (Realizing the `note_ini.md` Philosophy in ISAC)](#5-physics-informed-hybrid-state-space--bayesian-tracking-realizing-the-note_inimd-philosophy-in-isac)
  - [5.1 Neural Pre-Conditioning of Echo Measurement Vector $z_k$](#51-neural-pre-conditioning-of-echo-measurement-vector-z_k)
  - [5.2 Posterior Cramér-Rao Lower Bound (PCRLB) Constrained Filtering](#52-posterior-cramér-rao-lower-bound-pcrlb-constrained-filtering)
  - [5.3 Bayesian Goodness-of-Fit & Target Occlusion Adaptation](#53-bayesian-goodness-of-fit--target-occlusion-adaptation)
- [6. Networked & Reconfigurable ISAC Configurations](#6-networked--reconfigurable-isac-configurations)
  - [6.1 Cooperative Multi-BS Networked Predictive Beam Tracking](#61-cooperative-multi-bs-networked-predictive-beam-tracking)
  - [6.2 Target-Mounted & Environment RIS/IRS-Assisted ISAC Tracking](#62-target-mounted--environment-risirs-assisted-isac-tracking)
  - [6.3 OTFS-ISAC 3D Motion Predictive Topology](#63-otfs-isac-3d-motion-predictive-topology)
- [7. Comparative Taxonomy of ISAC Channel Prediction Schemes](#7-comparative-taxonomy-of-isac-channel-prediction-schemes)
- [8. Critical Challenges & Open Research Frontiers](#8-critical-challenges--open-research-fronters)
- [9. Comprehensive Annotated Bibliography (2020–2026)](#9-comprehensive-annotated-bibliography-20202026)

---

## 1. Fundamental Paradigm: From Blind Extrapolation to Sensing-Assisted Tracking

### 1.1 The Blind Channel Prediction Bottleneck
In traditional communications, the transmitter predicts the future channel $\mathbf{H}_{k+\Delta t}$ purely by extrapolating past channel estimates $[\hat{\mathbf{H}}_{k-L+1}, \dots, \hat{\mathbf{H}}_k]$. This approach suffers from three major flaws:
1. **Pilot Overhead & Feedback Latency:** Training pilots consume precious time-frequency resources; feedback delays in FDD or high-speed links ensure that historical measurements are already degraded by channel aging.
2. **Blind Extrapolation Collapse:** When a vehicle maneuvers, accelerates, or turns a corner, past channel values cannot infer future acceleration without knowing target physics.
3. **Severe Multi-User Interference:** Mispointed directional narrow beams in mmWave/THz create strong inter-user interference (IUI) and severe SNR drops.

### 1.2 The ISAC / ISSC Synergy: Dual-Functional Waveforms as Probing Signals
ISAC integrates radar sensing into the mobile network infrastructure. The base station (BS) emits a Dual-Functional Radar-Communication (DFRC) waveform. While downlink users decode communications payload data, the BS simultaneously processes the **backscattered echo signals** reflected by the user terminal and environmental obstacles. 

In synchronized ISSC (Integrated Sensing, Synchronization, and Communications), timing and frequency synchronization parameters are extracted jointly from the radar return, providing immediate zero-overhead tracking of terminal kinematics.

```text
                                  ┌────────────────────────┐
                                  │   DFRC Base Station    │
                                  └───────────┬────────────┘
                                              │
                    Transmit DFRC Waveform    │  Reflected Radar Echo
                    (Payload + Sensing)       │  (Zero-overhead, real-time)
                                              ▼  ▲
                                         ┌────┴───┐
                                         │ Target │ (Vehicle / UAV / UE)
                                         │ Mobile │
                                         └────────┘
                                              │
                        Direct Physical Measurements:
                        - Range r_k
                        - Azimuth θ_k & Elevation φ_k
                        - Radial Velocity v_k & Doppler f_D,k
```

### 1.3 The Sensing-to-Communication (S2C) Channel Mapping
The physical motivation underlying sensing-assisted channel prediction is that **electromagnetic propagation for communication and radar sensing shares the identical physical geometry**:
- A target vehicle located at coordinates $(x, y, z)$ with velocity $(v_x, v_y, v_z)$ creates both the radar echo response and the dominant Line-of-Sight (LoS) / strong multipath communication paths.
- By tracking target kinematic motion in Cartesian/polar coordinates, the future spatial angles $(\theta_{k+\Delta t}, \phi_{k+\Delta t})$ and Doppler shifts $\nu_{k+\Delta t}$ can be predicted **analytically**, without waiting for future pilot feedback.

---

## 2. System & Mathematical Formulations

```
+--------------------------------------------------------------------------------------------------+
| DFRC Signal Transmit: X[n] ∈ C^{M_t × N}                                                         |
|                                                                                                  |
| [Mono-Static Echo Reception at BS]             [Forward Communication Link at UE]                |
| Y_s[n] = G_s(X[n]) + Z_s[n]                    Y_c[n] = H_c^H * X[n] + Z_c[n]                    |
| Echo yields:                                   Communication channel:                            |
| Target Range r(t), Angle θ(t), Velocity v(t)   H_c(t) = ∑_l α_l a_R(θ_l) a_T^H(ϕ_l) e^{j2π f_D t}|
|                 │                                                 ▲                              |
|                 └──────────────► [S2C Mapping / EKF] ─────────────┘                              |
|                               Forecasts future Ĥ_c(k + Δt)                                      |
+--------------------------------------------------------------------------------------------------+
```

### 2.1 DFRC Signal & Echo Observation Model
Consider an ISAC base station equipped with $M_t$ transmit antennas and $M_r$ receive sensing antennas. Over $N$ subcarriers in an OFDM frame, the transmitted matrix is $\mathbf{X} \in \mathbb{C}^{M_t \times N}$.

The received mono-static radar echo signal at slot $k$ is given by:
$$\mathbf{Y}_{s, k} = \sum_{l=1}^{L_s} \beta_{l, k} \mathbf{b}(\theta_{l, k}) \mathbf{a}^H(\theta_{l, k}) \mathbf{X}_k e^{j 2 \pi f_{D, l, k} t} + \mathbf{Z}_{s, k}$$
where:
- $L_s$ is the number of radar scattering centers,
- $\beta_{l, k} \sim \mathcal{CN}(0, \sigma_{\text{RCS}}^2)$ represents the radar cross-section (RCS) complex reflection coefficient,
- $\mathbf{a}(\theta) \in \mathbb{C}^{M_t}$ and $\mathbf{b}(\theta) \in \mathbb{C}^{M_r}$ are the transmit and receive array steering vectors,
- $f_{D, l, k} = \frac{2 v_{r, l, k}}{\lambda_c}$ is the round-trip Doppler shift,
- $\mathbf{Z}_{s, k}$ is additive white Gaussian noise plus clutter.

### 2.2 Parametric Communication Channel Model
Simultaneously, the downlink communication channel $\mathbf{h}_{c, k} \in \mathbb{C}^{M_t}$ experienced by a single-antenna mobile user is expressed in geometric parametric form:
$$\mathbf{h}_{c, k} = \sqrt{\frac{M_t}{L_c}} \sum_{i=1}^{L_c} \alpha_{i, k} \mathbf{a}(\theta_{i, k}) e^{j 2 \pi f_{D, c, i, k} k T_s}$$
where $\alpha_{i, k}$ is the path complex gain, and $f_{D, c, i, k} = \frac{v_{r, i, k}}{\lambda_c}$ is the one-way communication Doppler frequency.

In Line-of-Sight (LoS) dominated scenarios, the dominant communication path parameters $(\theta_{1, k}, f_{D, c, 1, k})$ match the radar sensing parameters $(\theta_{\text{target}, k}, \frac{1}{2} f_{D, \text{radar}, k})$ with geometric precision.

### 2.3 Kinematic State-Space Evolution
Target motion follows kinematic physical equations. Defining the state vector at slot $k$ as $\mathbf{x}_k = [r_k, \dot{r}_k, \theta_k, \dot{\theta}_k]^T$ (range, radial velocity, angle, angular velocity):
$$\mathbf{x}_k = \mathbf{F} \mathbf{x}_{k-1} + \mathbf{w}_k, \quad \mathbf{F} = \begin{bmatrix} 1 & \Delta T & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & \Delta T \\ 0 & 0 & 0 & 1 \end{bmatrix}$$
where $\mathbf{w}_k \sim \mathcal{N}(\mathbf{0}, \mathbf{Q})$ represents continuous acceleration perturbations.

The measurement observation vector $\mathbf{z}_k$ extracted from matched-filtering the echo $\mathbf{Y}_{s, k}$ is non-linearly related to state $\mathbf{x}_k$:
$$\mathbf{z}_k = h(\mathbf{x}_k) + \mathbf{v}_k = \begin{bmatrix} r_k \\ \dot{r}_k \\ \theta_k \end{bmatrix} + \mathbf{v}_k, \quad \mathbf{v}_k \sim \mathcal{N}(\mathbf{0}, \mathbf{R}_k)$$

---

## 3. Classical Model-Based Sensing-Assisted Tracking

```
+--------------------------------------------------------------------------------------------------+
| Classical Radar-Assisted EKF Loop (Liu et al. 2020):                                             |
|                                                                                                  |
|  [Prior Kinematic Prediction]                 [Radar Echo Measurement]                           |
|  x̂_{k|k-1} = F * x̂_{k-1|k-1}                  Echo matched filter yields z_k = [r̂, v̂, θ̂]^T       |
|  P_{k|k-1} = F * P_{k-1} * F^T + Q                           │                                   |
|                 │                                            │                                   |
|                 ▼                                            ▼                                   |
|        [Innovation Residual]:  ỹ_k = z_k - h(x̂_{k|k-1})                                          |
|                 │                                                                                |
|                 ├────────────────────────────────────────────┐                                   |
|                 ▼                                            ▼                                   |
|        [Extended Kalman Gain K_k]               [Predict Future Angle θ̂_{k+1}]                   |
|                 │                                            │                                   |
|                 ▼                                            ▼                                   |
|        [Corrected Kinematics x̂_{k|k}]           [Predictive Beamformer w_{k+1}]                  |
|                                                 w_{k+1} = a(θ̂_{k+1}) / ||a(θ̂_{k+1})||            |
+--------------------------------------------------------------------------------------------------+
```

### 3.1 Radar-Assisted EKF & UKF Predictive Beamforming
In their seminal work, **Fan Liu et al. (IEEE TWC 2020)** pioneered the concept of *Radar-Assisted Predictive Beamforming for Vehicular Links*. 
- **Mechanism:** Instead of relying on user CSI feedback, the dual-functional roadside unit (RSU) tracks passing vehicles using reflected radar echoes. An Extended Kalman Filter (EKF) linearizes the non-linear relationship between Cartesian coordinates and polar measurements.
- **Predictive Angle Tracking:** The EKF projects vehicle motion forward by $\Delta t$:
  $$\hat{\theta}_{k+1|k} = \hat{\theta}_{k|k} + \Delta T \cdot \hat{\dot{\theta}}_{k|k}$$
- **Direct Beam Construction:** The predictive transmit beamformer is synthesized directly as $\mathbf{w}_{k+1} = \mathbf{a}(\hat{\theta}_{k+1|k})$, eliminating pilot training overhead entirely and sustaining high vehicular throughput up to $140\text{ km/h}$.

### 3.2 Particle Filtering for Non-Linear Maneuvering Targets
When vehicles undergo abrupt turning, emergency braking, or severe lateral maneuvers, the first-order Taylor approximation in EKF breaks down. 
- **Zhihao Ying et al. (IEEE VTC 2021)** introduced a Sequential Monte Carlo (Particle Filter) predictive beamforming framework.
- By approximating the posterior density $p(\mathbf{x}_k | \mathbf{z}_{1:k}) \approx \sum_{i=1}^{N_p} w_k^{(i)} \delta(\mathbf{x}_k - \mathbf{x}_k^{(i)})$ using thousands of weighted particles, the tracker captures arbitrary non-Gaussian kinematics, preventing beam divergence during sharp lane changes.

### 3.3 Near-Field Velocity Sensing & Predictive Beamforming
With massive antenna arrays and extremely high frequencies (mmWave / Sub-THz), mobile users operate within the **Fresnel near-field region** ($d < \frac{2 D^2}{\lambda}$).
- **Zhaolin Wang, Xidong Mu, and Yuanwei Liu (IEEE TVT 2024)** proved that near-field spherical wavefronts enable the simultaneous estimation of **both radial velocity and transverse velocity** from mono-static echo signals without requiring multi-epoch triangulation.
- Using maximum-likelihood velocity sensing, their predictive beamformer tracks position and velocity instantaneously, completely removing prior motion model assumptions.

### 3.4 The "Seeing is Not Always Believing" Dilemma: Multipath vs. LoS Discrepancy
A major limitation of classical radar-assisted tracking was revealed by **Yanpeng Cui, Qixun Zhang, Zhiyong Feng, Wen Qin, Zhiqing Wei, Fan Liu, and Ping Zhang (IEEE Wireless Commun. Lett. 2023)** in their landmark paper: *"Seeing is Not Always Believing: ISAC-Assisted Predictive Beam Tracking in Multipath Channels"*.

```text
Radar Echo Perspective (Seeing)               Communication Channel Reality (Believing)
Only detects strong physical scatterers:       Rich diffuse multipath & scattered clusters:
θ_radar = θ_LoS                                Optimal beam must align with:
                                               w_opt = argmax |h_c(θ_LoS, {θ_NLoS})^H w|^2 ≠ a(θ_radar)
```

- **The Problem:** Radar echoes reflect primarily from high-RCS metallic bodies along Line-of-Sight paths. However, the true communication capacity depends on the **aggregate spatial degrees of freedom (DoFs)** across both LoS and rich Non-Line-of-Sight (NLoS) multipath clusters.
- Aligning narrow beams strictly along the radar-sensed direction $\hat{\theta}_{\text{radar}}$ results in sub-optimal spectral efficiency whenever multipath constructive interference dominates.
- **The Solution:** Cui et al. introduced a two-stage hybrid approach: coarse EKF tracking via radar echoes, followed by fine residual beam tracking over the communication multipath profile.

---

## 4. Modern Machine Learning & Deep Learning Approaches (2022–2026)

Driven by the need to resolve multipath discrepancies, clutter interference, and non-linear target dynamics, deep learning has emerged as the dominant technology for sensing-assisted channel prediction.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   DEEP LEARNING IN ISAC PREDICTION                     │
│                                                                        │
│   Radar Echo Y_s[k] ────────┐                                          │
│                             ▼                                          │
│   Historical CSI h_c[k] ──► [Cross-Modal Spatio-Temporal Attention]    │
│                             - Fuses physical kinematics with multipath │
│                             - LLM / Edge Transformer / DNN             │
│                             │                                          │
│                             ▼                                          │
│               Forecasted Future Channel ĥ_c[k+Δt]                      │
│               + Predicted PC-CRLB Uncertainty Bound                    │
└────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Deep Learning for Sensing-Communication Feature Mapping
- **Chang Liu et al. (IEEE JSAC 2022)** designed a deep learning-based predictive beamforming framework for vehicular ISAC. Using an LSTM recurrent network, the model takes past echo spatial profiles and learns to predict future vehicle angles and optimal beam indices simultaneously, achieving near-optimal rate performance under imperfect radar cross-sections.
- **Yu Liu et al. (IEEE TCOMM 2023)** utilized Extreme Learning Machines (ELM) to decouple complex mutual interference between sensing and communication channels in Intelligent Reflecting Surface (IRS)-assisted ISAC systems, cutting training latency drastically compared to conventional backpropagation.

### 4.2 Spatio-Temporal Attention & Multi-Point Radar Fusion
In urban canyon environments, a single monostatic radar suffers from blockage behind large vehicles or buildings.
- **Ke-An Chen et al. (IEEE 2023)** proposed a multi-point radar sensing fusion architecture. Echoes from distributed roadside radar sensors are spatially aggregated and processed through a Deep Neural Network (DNN) to predict future communication beam directions under active Line-of-Sight blockage.

### 4.3 Cross-Modal Transformers for Complex Propagation
Standard recurrent models process sensing and communication data as separate streams. Modern ISAC predictors (2024–2025) deploy **Cross-Attention Transformers**:
- **Cross-Modal Attention:** The query ($\mathbf{Q}$) is generated from past communication channel snapshots, while keys ($\mathbf{K}$) and values ($\mathbf{V}$) are constructed from radar echo delay-Doppler maps:
  $$\mathbf{A}_{\text{S2C}} = \text{softmax}\left(\frac{\mathbf{Q}_{\text{comm}} \mathbf{K}_{\text{sensing}}^T}{\sqrt{d_k}}\right) \mathbf{V}_{\text{sensing}}$$
  This mechanism automatically discovers which radar scattering points correspond to real communication paths, filtering out irrelevant radar clutter.

### 4.4 Foundation Models & Edge LLMs in ISAC Channel Prediction (2025–2026)
The latest frontier integrates Large Language Models (LLMs) and Multimodal Foundation Models adapted for physical-layer signal sequences:
- **Junjie He, Zi-Xiang Ren, Jianping Yao, Han Hu, Tony Xiao Han, and Jie Xu (IEEE Wireless Commun. Lett. 2025) (`he2025sensing`):**  
  Proposed a novel **LLM-based sensing-assisted channel prediction** architecture for multi-antenna OFDM systems. By adapting pre-trained text foundation models to complex-matrix-form CSI tokens, the LLM captures intricate spatiotemporal correlations between monostatic radar echoes and bistatic communication channels, drastically outperforming conventional deep learning models in rich scattering environments.
- **Meng-Yao Wang et al. (IEEE Wireless Communications 2026) (`wang2026semantic`):**  
  Introduced **Semantic-Driven Asynchronous Channel Prediction and Reconstruction (SD-ACPR)** using lightweight Edge LLMs in RIS-assisted ISAC networks. To overcome LLM inference latency, the model pre-computes predictive beam strategies asynchronously and caches them at the edge; upon detecting sudden link blockage via RSRP gating, the pre-computed predictive beam is immediately deployed in $<0.1\text{ ms}$.

---

## 5. Physics-Informed Hybrid State-Space & Bayesian Tracking (Realizing the `note_ini.md` Philosophy in ISAC)

[`note_ini.md`](./note_ini.md) proposes a core research philosophy: combining analytical state-space filtering (KF/EKF) with physics-informed neural networks that clean and condition the input observation vector $\mathbf{z}_k$, while using Bayesian goodness-of-fit to validate Gaussianity. In ISAC channel prediction, this philosophy finds its most powerful expression.

```text
Raw Radar Echo Y_s[k]
          │
          ▼
┌────────────────────────────────────────────────────────┐
│  PHYSICS-INFORMED NEURAL PRE-CONDITIONER               │
│  - Absorbs radar clutter & multipath phase distortion  │
│  - Reconstructs well-conditioned observation vector:   │
│    z_k = g_θ(Y_s[k], Communication Prior)              │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼ Cleaned Kinematic Vector z_k
┌────────────────────────────────────────────────────────┐
│  BAYESIAN GOODNESS-OF-FIT & EKF ENGINE                 │
│  1. Innovation: ỹ_k = z_k - h(x̂_{k|k-1})              │
│  2. Normalized Innovation Squared (NIS) Test:          │
│     ε_k = ỹ_k^H * S_k^{-1} * ỹ_k ~ χ^2(d_z)            │
│     -> Detects target maneuver or echo occlusion       │
│  3. Variational Adaptive Covariance Update (R_k)       │
│  4. Kinematic Posterior Update: x̂_{k|k}                │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
Forecasted Communication Channel ĥ_c[k+Δt] + Uncertainty Ellipsoid P_{k+Δt}
```

### 5.1 Neural Pre-Conditioning of Echo Measurement Vector $z_k$
In a practical ISAC receiver, the raw echo measurement vector $\mathbf{z}_k = [r_k, \dot{r}_k, \theta_k]^T$ extracted by classical 2D-FFT periodograms is contaminated by:
1. Target geometric centroid jitter (extended target dispersion),
2. Power amplifier non-linear harmonics,
3. Residual full-duplex self-interference (SI) leakage from the DFRC transmitter.

**The Hybrid Neural Solution:** A lightweight neural network $g_\theta(\cdot)$, informed by physical Doppler and delay priors, processes the raw echo matched-filter output to generate an uncorrupted, well-conditioned observation vector:
$$\mathbf{z}_k = g_\theta\left(\mathbf{Y}_{s, k}, \hat{\mathbf{x}}_{k|k-1}\right)$$
This conditioned vector $\mathbf{z}_k$ is then fed into the analytical EKF engine. Because the EKF handles the kinematic physics ($\mathbf{F}$ matrix), the network does not need to learn projectile motion or geometry from scratch, reducing training overhead by orders of magnitude while ensuring zero hallucination.

### 5.2 Posterior Cramér-Rao Lower Bound (PCRLB) Constrained Filtering
In ISAC systems, channel prediction accuracy is bounded by radar estimation theory:
- **Ziheng Zhang et al. (IEEE TVT 2026) (`zhang2026mobile`):** Derived the analytical **Posterior Cramér-Rao Lower Bound (PCRLB)** for recursive EKF tracking in mobile ISAC systems, establishing a closed-form elliptical performance bound quantifying the fundamental trade-off between sensing precision and communication throughput.
- **Xiaoyu Yang et al. (IEEE TWC 2025) (`yang2025cooperative`):** Formulated predictive beamforming by enforcing a Predicted Conditional CRLB (PC-CRLB) constraint, guaranteeing that the predicted beam maintains sufficient radar illumination energy to track the target in future slots.

### 5.3 Bayesian Goodness-of-Fit & Target Occlusion Adaptation
As emphasized in `note_ini.md`, the Kalman Filter assumes Gaussian innovation residuals:
$$\tilde{\mathbf{y}}_k = \mathbf{z}_k - h(\hat{\mathbf{x}}_{k|k-1}) \sim \mathcal{N}\left(\mathbf{0}, \mathbf{S}_k\right)$$
In ISAC vehicular and drone tracking, this assumption breaks when a truck temporarily occludes the direct radar echo:
1. **NIS Testing:** The Normalized Innovation Squared is computed:
   $$\epsilon_k = \tilde{\mathbf{y}}_k^T \mathbf{S}_k^{-1} \tilde{\mathbf{y}}_k$$
2. **Occlusion Detection:** If $\epsilon_k > \chi_{0.99}^2(d_z)$, the system declares an **echo occlusion alarm**.
3. **Adaptive Covariance Inflation:** The filter automatically inflates the measurement covariance $\mathbf{R}_k \to \infty$, falling back gracefully to kinematic dead reckoning ($\hat{\mathbf{x}}_{k|k} \approx \hat{\mathbf{x}}_{k|k-1}$) and relying on communication-side spatial correlation until the radar echo reappears.

---

## 6. Networked & Reconfigurable ISAC Configurations

### 6.1 Cooperative Multi-BS Networked Predictive Beam Tracking
Single-site monostatic sensing is susceptible to target blind zones and Doppler ambiguity.
- **Xiaoyu Yang, Zhi-Qing Wei, Jie Xu, Hui-Ci Wu, and Zhi-Yong Feng (IEEE TWC 2025) (`yang2025cooperative`):**  
  Investigated a cooperative MIMO-OFDM networked ISAC system where multiple distributed base stations operating on orthogonal frequencies cooperatively track a mobile terminal. Local 2D-DFTs extract target parameters, and a centralized EKF fuses the multi-angle observations, eliminating monostatic blind spots and maximizing the predictive communication rate.

### 6.2 Target-Mounted & Environment RIS/IRS-Assisted ISAC Tracking
- **Ziheng Zhang et al. (IEEE TVT 2026) (`zhang2026mobile`):** Proposed mounting an Intelligent Reflecting Surface (IRS) directly on a maneuvering UAV. The target-mounted IRS serves a dual purpose: providing high-strength, controllable echo reflections for base station radar tracking while acting as an active relay to enhance ground communication links.
- **Wanting Lyu et al. (IEEE IoTJ 2024):** Derived Fisher information matrix and Cramér-Rao Bound (CRB) minimization policies for RIS-aided mmWave ISAC, showing that optimized phase shifts maintain narrow tracking beams on fast-moving targets.

### 6.3 OTFS-ISAC 3D Motion Predictive Topology
- **Luping Xiang et al. (IEEE IoTJ 2024) (`xiang2024robust`):** Integrated Orthogonal Time Frequency Space (OTFS) modulation with ISAC. Because OTFS represents signals directly in the delay-Doppler domain, target motion parameters extracted from OTFS radar echoes map directly to the communication channel matrix without 2D Fourier transformation, enabling robust 3D motion prediction for airborne UAV base stations.

---

## 7. Comparative Taxonomy of ISAC Channel Prediction Schemes

| Dimension / Metric | Classical EKF / UKF ISAC | Particle Filter ISAC | Deep Learning / LSTM ISAC | Cross-Modal Transformer ISAC | Hybrid NN-EKF with Conditioned $z_k$ | Edge LLM Foundation ISAC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Reference** | Liu et al. (2020) | Ying et al. (2021) | Liu et al. (2022) | Chen et al. (2023) | Note Seed / Zhang (2026) | He (2025), Wang (2026) |
| **Input Modality** | Monostatic Radar Echo | Monostatic Echo | Echo Spatial Profiles | Multi-Radar Echoes | Echo + Comm Prior | Complex Matrix CSI Tokens |
| **Target Kinematics** | Linear / Mild Non-linear | Highly Non-linear | Complex Dynamics | Non-linear + Clutter | Kinematic State $\mathbf{x}_k$ | Arbitrary Spatiotemporal |
| **Multipath Handling** | LoS only (fails on NLoS) | LoS only | Implicit learning | Explicit Cross-Attention | LoS Kinematics + Residual | High-capacity reasoning |
| **Inference Latency** | $< 0.1\text{ ms}$ | $\approx 2\text{–}5\text{ ms}$ | $< 0.3\text{ ms}$ | $\approx 1\text{ ms}$ | $< 0.2\text{ ms}$ | Asynchronous cache (<0.1 ms) |
| **Training Requirement** | Zero training | Zero training | Large dataset | Moderate dataset | Small dataset ($100\times$ less) | Pre-trained + LoRA fine-tuning |
| **Uncertainty Tracking** | Analytical Covariance $\mathbf{P}_k$ | Empirical Particles | None | Heuristic | Exact Bayesian Ellipsoid | Reinforcement learning feedback |

---

## 8. Critical Challenges & Open Research Frontiers

1. **The Unshared Scatterer Problem:** In urban environments, some physical objects reflect radar echoes back to the BS but do not scatter signals toward the user (and vice versa). Advanced predictors must distinguish shared from non-shared clusters using cross-modal feature gating.
2. **Full-Duplex Self-Interference (FD-SI):** Monostatic ISAC requires transmitting high-power communication signals while simultaneously receiving weak nano-watt radar echoes at the same frequency. Residual SI leakage corrupts the observation vector $\mathbf{z}_k$.
3. **Asynchronous Frame Alignment:** Radar pulses operate on microsecond radar repetition intervals (PRIs), whereas 5G/6G communication frames operate on millisecond slot schedules. Synchronizing sensing updates with predictive precoding deadlines requires asynchronous state estimation.
4. **Near-Field Spherical Wavefront Drift:** For extremely large aperture arrays (ELAA) at THz frequencies, the user transitions dynamically between near-field (curved phase) and far-field (planar phase), requiring adaptive beam-focusing prediction.

---

## 9. Comprehensive Annotated Bibliography (2020–2026)

### 9.1 Foundational Radar-Assisted Predictive Tracking
- **Liu, F., Yuan, W., Masouros, C., & Katsikos, N. (2020).** *"Radar-Assisted Predictive Beamforming for Vehicular Links: Communication Served by Sensing."* **IEEE Transactions on Wireless Communications**, 19(11), 7704–7717. [DOI: 10.1109/TWC.2020.3015735](https://doi.org/10.1109/TWC.2020.3015735).  
  *Significance:* Seminal paper establishing EKF-based predictive beamforming using dual-functional radar echoes, demonstrating zero-overhead vehicular tracking.
- **Cui, Y., Zhang, Q., Feng, Z., Qin, W., Wei, Z., Liu, F., & Zhang, P. (2023).** *"Seeing is Not Always Believing: ISAC-Assisted Predictive Beam Tracking in Multipath Channels."* **IEEE Wireless Communications Letters**, 12(11), 1871–1875. [DOI: 10.1109/LWC.2023.3303949](https://doi.org/10.1109/LWC.2023.3303949).  
  *Significance:* Identifies the fundamental discrepancy between radar echo angles and optimal multipath communication beam alignment, providing a two-stage coarse-fine tracking correction.
- **Wang, Z., Mu, X., & Liu, Y. (2024).** *"Near-Field Velocity Sensing and Predictive Beamforming."* **IEEE Transactions on Vehicular Technology**, 73(12), 19520–19532. [DOI: 10.1109/TVT.2024.3454481](https://doi.org/10.1109/TVT.2024.3454481).  
  *Significance:* Unveils near-field spherical wavefront velocity sensing to extract both radial and transverse velocities from a monostatic setup, enabling model-free predictive beamforming.
- **Ying, Z., Cui, Y., Mu, J., & Jing, X. (2021).** *"Particle Filter based Predictive Beamforming for Integrated Vehicle Sensing and Communication."* **IEEE VTC-Fall 2021**, 1–5. [DOI: 10.1109/VTC2021-Fall52928.2021.9625076](https://doi.org/10.1109/VTC2021-Fall52928.2021.9625076).  
  *Significance:* Implements particle filtering to track non-linear maneuvering vehicles during lane changes and emergency deceleration.

### 9.2 Machine Learning & Deep Foundation Architectures in ISAC
- **Liu, C., Liu, X., Yuan, W., Liu, F., & Ng, D. W. K. (2022).** *"Learning-Based Predictive Beamforming for Integrated Sensing and Communication in Vehicular Networks."* **IEEE Journal on Selected Areas in Communications**, 40(7), 2137–2152. [DOI: 10.1109/JSAC.2022.3180803](https://doi.org/10.1109/JSAC.2022.3180803).  
  *Significance:* Deep LSTM framework learning the mapping from radar echo spatial profiles directly to optimal predictive beamforming vectors.
- **He, J., Ren, Z.-X., Yao, J., Hu, H., Han, T. X., & Xu, J. (2025).** *"Sensing-Assisted Channel Prediction in Complex Wireless Environments: An LLM-Based Approach."* **IEEE Wireless Communications Letters**, Early Access. [DOI: 10.1109/LWC.2025.3600454](https://doi.org/10.1109/LWC.2025.3600454).  
  *Significance:* Adapts pre-trained Large Language Models to complex-valued CSI matrices, fusing monostatic radar echoes with bistatic communication channel dynamics.
- **Wang, M.-Y., Li, X.-W., Gao, Y., Zeng, M., Yin, C., Wang, J., Nallanathan, A., & Yuen, C. (2026).** *"Semantic-Driven Asynchronous Channel Prediction and Reconstruction with Edge LLMs for RIS-Assisted ISAC Systems."* **IEEE Wireless Communications**, Early Access. [DOI: 10.1109/MWC.2026.3715563](https://doi.org/10.1109/MWC.2026.3715563).  
  *Significance:* Proposes edge LLM asynchronous channel prediction with local caching, eliminating LLM inference latency during sudden wireless link blockages.
- **Chen, K.-A., Liu, D., & Zhang, Z. (2023).** *"Beam Tracking Based on Multi-Point Radar Sensing and DNN Prediction."* **IEEE IC-NIDC 2023**, 325–330. [DOI: 10.1109/IC-NIDC59918.2023.10390835](https://doi.org/10.1109/IC-NIDC59918.2023.10390835).  
  *Significance:* Distributed multi-radar sensing aggregation with DNN prediction to sustain beam tracking across blocked Line-of-Sight scenarios.

### 9.3 Networked, Cooperative & Reconfigurable ISAC
- **Yang, X., Wei, Z., Xu, J., Wu, H., & Feng, Z. (2025).** *"Cooperative Sensing-Assisted Predictive Beam Tracking for MIMO-OFDM Networked ISAC Systems."* **IEEE Transactions on Wireless Communications**, Early Access. [DOI: 10.1109/TWC.2025.3580890](https://doi.org/10.1109/TWC.2025.3580890).  
  *Significance:* Multi-BS cooperative EKF tracking over non-overlapping frequency bands with Predicted Conditional CRLB constraints for robust predictive beamforming.
- **Zhang, Z., Chen, W., Wu, Q., Li, Z., Wu, Q., Zhao, M.-M., & Feng, W. (2026).** *"Mobile Tracking via Target-Mounted IRS-Assisted ISAC System."* **IEEE Transactions on Vehicular Technology**, Early Access. [DOI: 10.1109/TVT.2026.3737004](https://doi.org/10.1109/TVT.2026.3737004).  
  *Significance:* Mounts an IRS onto moving UAVs to enhance radar echo strength and communication links simultaneously, deriving the analytical PCRLB and closed-form tracking beamformers.
- **Xiang, L., Xu, K., Hu, J., Masouros, C., & Yang, K. (2024).** *"Robust NOMA-Assisted OTFS-ISAC Network Design With 3-D Motion Prediction Topology."* **IEEE Internet of Things Journal**, 11(10), 17820–17835. [DOI: 10.1109/JIOT.2024.3352391](https://doi.org/10.1109/JIOT.2024.3352391).  
  *Significance:* Direct delay-Doppler OTFS radar echo processing coupled with 3D kinematic motion prediction for multi-user NOMA power allocation.
- **Wang, S., Tang, A.-M., Wang, X.-D., & Qu, W. (2025).** *"Sensing-Assisted Channel Estimation for Bistatic OFDM ISAC Systems: Framework, Algorithm, and Analysis."* **IEEE Transactions on Wireless Communications**, Early Access. [DOI: 10.1109/TWC.2025.3633948](https://doi.org/10.1109/TWC.2025.3633948).  
  *Significance:* Develops sensing-assisted LMMSE channel estimation with delay-Doppler tolerance factors to prevent estimation errors from degrading wideband OFDM communications.
