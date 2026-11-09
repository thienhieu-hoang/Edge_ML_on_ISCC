# Literature Review: Wireless Channel Prediction & Tracking — From Classical State-Space Estimation to Modern Physics-Informed Deep Learning

**Author / Compiler:** Antigravity 2.0 (Dual-Perspective Literature Synthesis Engine)  
**Context:** Non-Terrestrial Networks (NTN), Massive MIMO & High-Mobility 6G Communications  
**Date:** October 2026  
**Reference Document:** [`note_ini.md`](./note_ini.md)  
**Key Venues Covered:** IEEE JSAC, IEEE TSP, IEEE TWC, IEEE TVT, IEEE TMC, IEEE COMST, IEEE OJ-SP, IEEE Access  

---

## Executive Summary

Channel State Information (CSI) is the linchpin of modern multi-antenna wireless communications, governing critical physical-layer operations such as spatial precoding, zero-forcing / MMSE beamforming, link adaptation, and resource scheduling. In static or quasi-static environments, instantaneous channel estimation within a transmission slot suffices. However, in emerging **high-mobility scenarios**—notably Low Earth Orbit (LEO) satellite Non-Terrestrial Networks (NTN), High-Speed Railway (HSR), and Vehicle-to-Everything (V2X)—rapid mobility induces severe Doppler shifts and continuous delay-phase evolution. This causes **channel aging**, rendering estimated CSI stale by the time it is processed and fed back to the transmitter.

To bridge this temporal gap, **channel prediction** forecasts future channel states $\mathbf{h}_{k+\Delta t}$ based on a sequence of historical observations $[\mathbf{h}_1, \dots, \mathbf{h}_k]$. This literature review synthesizes the evolutionary trajectory of channel prediction, categorized into three distinct eras:

1. **Classical Model-Based Filtering & Parametric Tracking:** Autoregressive (AR) models, Wiener predictors, Kalman Filtering (KF), and Extended Kalman Filtering (EKF).
2. **Pure Data-Driven Machine Learning (ML / DL):** Recurrent architectures (LSTM, GRU), Temporal Convolutional Networks (TCN), and Spatio-Temporal Transformers.
3. **Physics-Informed & Hybrid Model-Driven ML (The Current Frontier):** Deep unfolding, KalmanNet / Latent-KalmanNet, Neural-augmented observation vectors ($\mathbf{z}_k$), Bayesian goodness-of-fit adaptation, and Continuous-Time Neural ODEs.

Finally, this review synthesizes the core open challenges, real-time hardware execution budgets, and emerging system-level applications (such as predictive beamforming and proactive handover) for practical deployment in 5G-Advanced and 6G systems.

---

## Table of Contents
- [1. Theoretical Foundations & The Channel Aging Problem](#1-theoretical-foundations--the-channel-aging-problem)
  - [1.1 Channel Aging Mechanics](#11-channel-aging-mechanics)
  - [1.2 Estimation vs. Prediction: An Upstream-Downstream Continuum](#12-estimation-vs-prediction-an-upstream-downstream-continuum)
- [2. Classical Model-Based Channel Prediction](#2-classical-model-based-channel-prediction)
  - [2.1 Autoregressive (AR) and Wiener Prediction](#21-autoregressive-ar-and-wiener-prediction)
  - [2.2 State-Space Tracking via Kalman Filtering (KF)](#22-state-space-tracking-via-kalman-filtering-kf)
  - [2.3 Non-Linear Tracking: Extended Kalman Filtering (EKF) and UKF](#23-non-linear-tracking-extended-kalman-filtering-ekf-and-ukf)
  - [2.4 Inherent Bottlenecks of Pure Model-Based Predictors](#24-inherent-bottlenecks-of-pure-model-based-predictors)
- [3. Pure Data-Driven Deep Learning Predictors](#3-pure-data-driven-deep-learning-predictors)
  - [3.1 Recurrent Formulations (RNN, LSTM, GRU)](#31-recurrent-formulations-rnn-lstm-gru)
  - [3.2 Convolutional & Temporal Convolutional Networks (TCN)](#32-convolutional--temporal-convolutional-networks-tcn)
  - [3.3 Attention Mechanisms & Spatio-Temporal Transformers](#33-attention-mechanisms--spatio-temporal-transformers)
  - [3.4 Continuous-Time Neural ODEs & Non-Uniform Pilots](#34-continuous-time-neural-odes--non-uniform-pilots)
  - [3.5 Limitations of Pure Black-Box DL Models](#35-limitations-of-pure-black-box-dl-models)
- [4. The Modern Frontier: Physics-Informed & Hybrid Model-Driven ML](#4-the-modern-frontier-physics-informed--hybrid-model-driven-ml)
  - [4.1 Model-Based Deep Learning Taxonomy](#41-model-based-deep-learning-taxonomy)
  - [4.2 KalmanNet & Latent-KalmanNet](#42-kalmannet--latent-kalmannet)
  - [4.3 Neural-Enhanced EKF via Front-End Vector Conditioning ($z_k$)](#43-neural-enhanced-ekf-via-front-end-vector-conditioning-z_k)
  - [4.4 Hypernetworks for Non-Stationary Adaptation](#44-hypernetworks-for-non-stationary-adaptation)
- [5. Bayesian Goodness-of-Fit & Non-Gaussian Distributional Adaptation](#5-bayesian-goodness-of-fit--non-gaussian-distributional-adaptation)
  - [5.1 Breakdown of the Gaussian Residual Assumption](#51-breakdown-of-the-gaussian-residual-assumption)
  - [5.2 Bayesian Residual Evaluation & Dynamic Noise Covariance Estimation](#52-bayesian-residual-evaluation--dynamic-noise-covariance-estimation)
  - [5.3 Uncertainty Quantification (UQ) for Predictive Beamforming](#53-uncertainty-quantification-uq-for-predictive-beamforming)
- [6. Architectural Comparison & Taxonomy Matrix](#6-architectural-comparison--taxonomy-matrix)
- [7. Open Challenges, System Applications & Future Research Directions](#7-open-challenges-system-applications--future-research-directions)
  - [7.1 Predictive Beamforming, Link Adaptation & Proactive Handover](#71-predictive-beamforming-link-adaptation--proactive-handover)
  - [7.2 Real-Time Hardware Budgets & Inference Latency Deadlines (<1 ms)](#72-real-time-hardware-budgets--inference-latency-deadlines-1-ms)
  - [7.3 Self-Supervised & Label-Free Training Schemes](#73-self-supervised--label-free-training-schemes)
  - [7.4 Continuous-Time Prediction & Non-Uniform Pilot Sampling](#74-continuous-time-prediction--non-uniform-pilot-sampling)
- [8. Comprehensive Annotated Bibliography](#8-comprehensive-annotated-bibliography)

---

## 1. Theoretical Foundations & The Channel Aging Problem

### 1.1 Channel Aging Mechanics
In wireless communications, relative velocity $v$ between the transmitter and receiver induces a Doppler shift:
$$f_D = \frac{v}{\lambda_c} \cos(\theta)$$
where $\lambda_c$ is the carrier wavelength and $\theta$ is the angle of arrival/departure. In 5G-Advanced and 6G Non-Terrestrial Networks (NTN), LEO satellites orbit at orbital velocities $v \approx 7.5\text{ km/s}$, producing Doppler shifts upwards of $\pm 50\text{ kHz}$ at S-band and hundreds of kHz at Ka-band, accompanied by continuous Doppler rate-of-change $\dot{f}_D$.

According to Jakes' / Clarke's isotropic scattering model, the continuous temporal autocorrelation function of a Rayleigh fading channel is:
$$R_h(\Delta t) = \mathbb{E}[h(t) h^*(t + \Delta t)] = \sigma_h^2 J_0(2 \pi f_D \Delta t)$$
where $J_0(\cdot)$ is the zeroth-order Bessel function of the first kind.

```text
[Slot k: Pilot Transmission] ──> [CSI Estimation h_hat_k] ──> [CSI Feedback / Processing Delay Δt]
                                                                          │
                                                                          ▼
[Channel Reality at Transmission]: h(k + Δt) ≠ h_hat_k  <── [Channel Outdated / Mismatch!]
                                                         ──> Severe precoding leakage
                                                         ──> Multi-user interference (MUI)
                                                         ──> Severe SNR & Throughput Drop
```

When the loop delay $\Delta t$ (encompassing pilot transmission, channel estimation, precoding calculation, and feedback) exceeds the channel coherence time $T_c \approx \frac{9}{16 \pi f_D}$, the actual channel at transmission $\mathbf{h}_{k+\Delta t}$ deviates substantially from the estimated $\hat{\mathbf{h}}_k$. **Channel prediction** overcomes this by learning the mapping:
$$\mathcal{F}: \{\hat{\mathbf{h}}_{k-L+1}, \dots, \hat{\mathbf{h}}_k\} \longrightarrow \hat{\mathbf{h}}_{k+\Delta t}$$

### 1.2 Estimation vs. Prediction: An Upstream-Downstream Continuum

A prevalent ambiguity in communications research is conflating *channel estimation* with *channel prediction*. As detailed in `note_ini.md`, they represent two complementary stages of the physical-layer signal chain:

| Dimension | Intra-Slot Channel Estimation | Inter-Slot Channel Prediction / Tracking |
| :--- | :--- | :--- |
| **Domain** | Time-Frequency Resource Grid (within a slot) | Temporal Evolution (across successive slots/frames) |
| **Input** | Received pilot symbols $\mathbf{Y}_p$ at sparse subcarrier/symbol positions | Historical channel states $\hat{\mathbf{h}}_1, \dots, \hat{\mathbf{h}}_k$ |
| **Output** | Full 2D channel matrix $\hat{\mathbf{H}}_k \in \mathbb{C}^{K \times N}$ | Future channel vector/matrix $\hat{\mathbf{h}}_{k+\Delta t}$ |
| **Core Methodologies** | 2D Interpolation, LMMSE, Compressed Sensing, 2D CNNs, Super-Resolution | AR models, Kalman Filtering, RNN/LSTM, Transformers, SSMs |
| **Physical Focus** | Multipath delay spread, pilot contamination, frequency selectivity | Doppler spectrum, terminal trajectory, angular drift, aging |

Consequently, intra-slot channel estimation acts as the **direct upstream data source** for channel prediction: the output of a slot-level estimator provides instantaneous CSI snapshots $\hat{\mathbf{h}}_k$, which serve as the measurement observation $\mathbf{z}_k$ for downstream temporal tracking and future prediction.

---

## 2. Classical Model-Based Channel Prediction

```
+---------------------------------------------------------------------------------------------------+
| Classical Pipeline:                                                                               |
|                                                                                                   |
|  [State Evolution]                                [Measurement Model]                             |
|  x_k = F_k * x_{k-1} + w_k,  w_k ~ N(0, Q_k)       z_k = H_k * x_k + v_k,  v_k ~ N(0, R_k)        |
|                  │                                                  │                             |
|                  ▼                                                  ▼                             |
|         [Prior State Predict]                             [Measurement Residual]                  |
|         x̂_{k|k-1} = F_k * x̂_{k-1|k-1}                      ỹ_k = z_k - H_k * x̂_{k|k-1}            |
|                  │                                                  │                             |
|                  └───────────────► [Kalman Gain K_k] ◄──────────────┘                             |
|                                             │                                                     |
|                                             ▼                                                     |
|                                   [Posterior State Update]                                        |
|                             x̂_{k|k} = x̂_{k|k-1} + K_k * ỹ_k                                       |
+---------------------------------------------------------------------------------------------------+
```

### 2.1 Autoregressive (AR) and Wiener Prediction
The classical baseline for temporal channel forecasting assumes the channel follows a $p$-th order linear Autoregressive ($\text{AR}(p)$) process:
$$h_k = \sum_{i=1}^p a_i h_{k-i} + e_k$$
where $a_i$ are AR coefficients and $e_k$ is zero-mean driving noise.
- **Yule-Walker Equations:** Coefficients $\mathbf{a} = [a_1, \dots, a_p]^T$ are determined by solving $\mathbf{R}_{hh} \mathbf{a} = \mathbf{r}_h$, utilizing the known theoretical autocorrelation matrix derived from Bessel functions ($J_0(2 \pi f_D \tau)$).
- **Wiener-Hopf Predictor:** Under wide-sense stationary (WSS) conditions, the linear minimum mean square error (LMMSE) prediction is given analytically by the Wiener filter:
  $$\hat{h}_{k+d} = \mathbf{w}^H \mathbf{h}_{1:k}, \quad \mathbf{w} = (\mathbf{R}_{hh} + \sigma_v^2 \mathbf{I})^{-1} \mathbf{r}_{h, d}$$
- **Limitations:** AR and Wiener models assume perfect stationarity and known Doppler frequencies. In real mobile propagation, scattering environments change dynamically, leading to model mismatch.

### 2.2 State-Space Tracking via Kalman Filtering (KF)
To handle time-varying dynamics, channel prediction is framed as a Gauss-Markov state-space model:
$$\mathbf{x}_k = \mathbf{F}_k \mathbf{x}_{k-1} + \mathbf{w}_k, \quad \mathbf{w}_k \sim \mathcal{N}(\mathbf{0}, \mathbf{Q}_k)$$
$$\mathbf{z}_k = \mathbf{H}_k \mathbf{x}_k + \mathbf{v}_k, \quad \mathbf{v}_k \sim \mathcal{N}(\mathbf{0}, \mathbf{R}_k)$$

The Kalman Filter recursively computes the optimal MMSE state estimate through two phases:
1. **Time Update (Predict):**
   $$\hat{\mathbf{x}}_{k|k-1} = \mathbf{F}_k \hat{\mathbf{x}}_{k-1|k-1}$$
   $$\mathbf{P}_{k|k-1} = \mathbf{F}_k \mathbf{P}_{k-1|k-1} \mathbf{F}_k^H + \mathbf{Q}_k$$
2. **Measurement Update (Correct):**
   $$\mathbf{K}_k = \mathbf{P}_{k|k-1} \mathbf{H}_k^H (\mathbf{H}_k \mathbf{P}_{k|k-1} \mathbf{H}_k^H + \mathbf{R}_k)^{-1}$$
   $$\hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + \mathbf{K}_k (\mathbf{z}_k - \mathbf{H}_k \hat{\mathbf{x}}_{k|k-1})$$
   $$\mathbf{P}_{k|k} = (\mathbf{I} - \mathbf{K}_k \mathbf{H}_k) \mathbf{P}_{k|k-1}$$

Multi-step ahead prediction is achieved by projecting state evolution forward without measurement updates:
$$\hat{\mathbf{x}}_{k+d|k} = \mathbf{F}^{d} \hat{\mathbf{x}}_{k|k}$$

### 2.3 Non-Linear Tracking: Extended Kalman Filtering (EKF) and UKF
When tracking parametric physical models—such as path amplitudes $\alpha_l(t)$, time-varying Angles of Arrival $\theta_l(t)$, and Doppler frequency offsets $\omega_{D, l}(t)$—the state-space dynamics become non-linear:
$$\mathbf{x}_k = f(\mathbf{x}_{k-1}) + \mathbf{w}_k, \quad \mathbf{z}_k = h(\mathbf{x}_k) + \mathbf{v}_k$$
- **EKF:** Approximates non-linear transformations via first-order Taylor expansions using Jacobian matrices $\mathbf{F}_k = \left.\frac{\partial f}{\partial \mathbf{x}}\right|_{\hat{\mathbf{x}}_{k-1|k-1}}$ and $\mathbf{H}_k = \left.\frac{\partial h}{\partial \mathbf{x}}\right|_{\hat{\mathbf{x}}_{k|k-1}}$.
- **UKF:** Employs the unscented transform using deterministic sigma points to capture true mean and covariance up to 3rd-order Taylor accuracy for non-linear state distributions.

### 2.4 Inherent Bottlenecks of Pure Model-Based Predictors
1. **Severe Model Mismatch:** Classical filters require precise knowledge of system matrices $\mathbf{F}_k$, observation functions $h(\cdot)$, and statistical covariance matrices $\mathbf{Q}_k$ and $\mathbf{R}_k$. In fast-fading NTN channels, these change continuously and are impossible to calculate perfectly a priori.
2. **Gaussianity Assumption Vulnerability:** KF/EKF assume additive Gaussian noise. As proven in non-line-of-sight (NLoS) and urban multipath propagation, fading distributions exhibit heavy tails, impulsive interference, and non-Gaussian phase noise, causing EKF linearization errors and filter divergence.
3. **High Matrix Inversion Complexity:** Computing $\mathbf{K}_k$ involves inversions of size matching the measurement dimension $M$, scaling at $\mathcal{O}(M^3)$, which becomes computationally prohibitive for massive MIMO arrays ($M \ge 64, 128$).

---

## 3. Pure Data-Driven Deep Learning Predictors

Driven by the limitations of analytical models, the communications community has explored deep neural networks as universal function approximators to learn non-linear channel temporal dynamics directly from training data.

```text
Sequence of Past CSI:  [h_{k-L+1}, ..., h_{k-1}, h_k]
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Data-Driven Predictor:                                      │
│  - Recurrent (LSTM / GRU)                                    │
│  - Convolutional (TCN / Dilated CNN)                         │
│  - Attention / Transformer (LinFormer, Reverse-Positional)   │
│  - Continuous-Time (Neural ODE)                              │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
Predicted Future CSI:     ĥ_{k+d}
```

### 3.1 Recurrent Formulations (RNN, LSTM, GRU)
Recurrent Neural Networks maintain hidden states that evolve recursively with incoming channel frames:
$$\mathbf{s}_k = \sigma(\mathbf{W}_{xs} \mathbf{h}_k + \mathbf{W}_{ss} \mathbf{s}_{k-1} + \mathbf{b}_s)$$
- **Jiang & Schotten (2020) [IEEE OJ-COMS]** demonstrated that Long Short-Term Memory (LSTM) and Gated Recurrent Units (GRU) capture long-range temporal correlations across fading blocks, significantly outperforming shallow recurrent predictors and classical AR baselines.
- **Yuan et al. (2020) [IEEE TWC]** developed an autoregressive recurrent neural network with exogenous inputs for massive MIMO with channel aging, achieving superior spectral efficiency gains across both low and high terminal mobility.
- **Joo et al. (2019) [IEEE Access]** validated LSTM-based channel and power level forecasting using real-world vehicular IEEE 802.11p IQ measurement traces, documenting a 15%–25% reduction in root-mean-square error over static extrapolation.

### 3.2 Convolutional & Temporal Convolutional Networks (TCN)
While RNNs process channels sequentially, **Temporal Convolutional Networks (TCNs)** utilize 1D dilated causal convolutions:
- **Causality:** Prevents future information leakage into historical prediction.
- **Dilated Convolutions:** Expand the receptive field exponentially without escalating the parameter count:
  $$y_k = \sum_{i=0}^{K-1} f_i \cdot x_{k - d \cdot i}$$
  where $d$ is the dilation factor and $K$ is filter size.
- **Advantage:** Enables highly parallel training across historical sequences, circumventing the vanishing/exploding gradient bottlenecks common to unrolled LSTMs over long horizons.

### 3.3 Attention Mechanisms & Spatio-Temporal Transformers
Just as the introduction of spatial attention mechanisms overtook conventional CNNs in channel estimation, self-attention and Transformers have dramatically superseded recurrent neural networks (RNNs/LSTMs) in channel prediction. LSTMs suffer from sequential computation bottlenecks and vanishing gradients when forecasting beyond 5–10 historical slots. Transformers overcome this by applying multi-head self-attention across the temporal dimension:
$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q} \mathbf{K}^T}{\sqrt{d_k}}\right) \mathbf{V}$$

This allows every historical CSI snapshot to attend directly to all other snapshots, capturing long-term Doppler phase trajectories and spatial correlations across massive antenna arrays.

Key recent works demonstrating this paradigm shift include:
- **Jiang et al. (2023) [IEEE Wireless Communications Letters] (`AcsiNet`)**: Introduced an attention-based deep network for CSI prediction in FDD massive MIMO systems. By compressing uplink CSI via 3D-IDFT and processing temporal features through an attention network, AcsiNet directly predicts downlink CSI from uplink snapshots, outperforming standard CNN and LSTM baselines.
- **Stenhammar, Fodor, & Fischione (2024) [IEEE Wireless Communications]**: Provided a landmark benchmark comparing five deep learning architectures (CNNs, LSTMs, GRUs, TCNs, and Transformers) across standardized 3GPP tapped delay line (TDL) fading channels. Their evaluation proved that Transformers achieve the lowest prediction error and longest valid forecasting horizon, but underscored that quadratic attention complexity $\mathcal{O}(L^2)$ poses significant latency challenges for real-time edge hardware.
- **Rizzello et al. (2023) [IEEE OJ-SP]**: Introduced **reverse positional encoding** and reverse sequence-to-sequence attention for channel prediction. Reversing the sequence prior to attention computation forces the attention heads to prioritize the most recent channel snapshots while preserving long-term temporal trends, ensuring robustness against varying sequence lengths.
- **Jin et al. (2025) [IEEE TWC] (`LinFormer`)**: Addressed the quadratic complexity $\mathcal{O}(L^2)$ of standard Transformers by designing an all-linear, time-aware multi-layer perceptron (TMLP) encoder. LinFormer reduces inference latency drastically to linear scale $\mathcal{O}(L)$ while outperforming full-attention Transformers across high-mobility 6G scenarios.
- **Ying et al. (2024) [IEEE TWC]**: Designed a joint channel prediction and multibeam precoding scheme for LEO satellite IoT, combining spatiotemporal neural prediction with a variational autoencoder (VAE) channel augmentor to withstand severe Doppler shifts and long satellite propagation delays.

### 3.4 Continuous-Time Neural ODEs & Non-Uniform Pilots
Standard ML models operate over uniform discrete time steps ($k, k+1, \dots$). However, practical 5G/6G systems utilize non-uniform pilot allocations, and LEO satellite Doppler variations are inherently continuous.
- **Cui et al. (2024) [China Communications]**: Proposed Tensor Neural Ordinary Differential Equations (TN-ODE) for continuous-time channel prediction, replacing discrete recurrent transitions with a learned ODE:
  $$\frac{d\mathbf{z}(t)}{dt} = f_\theta(\mathbf{z}(t), t)$$
  This enables direct evaluation of the channel at arbitrary continuous timestamps $t$, avoiding conventional intra-frame interpolation losses.
- **Sang et al. (2026) [IEEE TWC]**: Integrated continuous-time transformers with Chebyshev polynomial-based non-uniform pilot patterns, achieving Doppler-aliasing-free channel prediction across wide mobility variations with reduced pilot overhead.

### 3.5 Limitations of Pure Black-Box DL Models
Despite empirical success, pure black-box neural predictors present critical deficiencies:
1. **High Sample Inefficiency:** Require millions of training channel snapshots; prone to catastrophic failure when the operational environment shifts from the training distribution.
2. **Lack of Physical Interpretability:** Unverifiable failure modes create safety hazards for mission-critical link scheduling and high-power satellite beam tracking.
3. **Inability to Enforce State-Space Constraints:** Pure NNs do not inherently respect fundamental propagation physics (e.g., energy conservation, phase rotation laws, or state kinematic continuity).

---

## 4. The Modern Frontier: Physics-Informed & Hybrid Model-Driven ML

The prevailing research paradigm bridges the divide between domain physics and machine learning through **Model-Based Deep Learning** (Shlezinger, Eldar, & Boyd, 2022).

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   SPECTRUM OF CHANNEL PREDICTION                       │
│                                                                        │
│  [Classical Model-Based]      [Hybrid / Physics-Informed]   [Pure Data-Driven] 
│  KF / EKF / AR               KalmanNet / NN-Conditioned z    LSTM / Transformer
│  • Fully interpretable       • Preserves state equations     • Black-box
│  • Requires exact Q, R       • Learns K_k or cleans z_k      • No physical prior
│  • Fails under non-linear    • Robust to model mismatch      • Sample inefficient
└────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Model-Based Deep Learning Taxonomy
As characterized by Shlezinger et al. (2020, 2022) [IEEE Access / IEEE TSP], hybrid methodologies fall into two primary structures:
- **Deep Unfolding:** Unrolling iterative model-based algorithms (e.g., ISTA, Richardson-Lucy) into layered deep networks where iteration steps become neural layers with learnable step sizes.
- **Neural Augmentation of State-Space Filters:** Preserving the analytical state-space backbone while embedding lightweight neural networks to learn difficult-to-model physical residuals or unknown parameter matrices.

### 4.2 KalmanNet & Latent-KalmanNet
Introduced by Revach, Shlezinger, van Sloun, and Eldar (2022 [IEEE TSP]), **KalmanNet** is a breakthrough hybrid architecture that retains the Kalman Filter's state-space update loop while computing the Kalman gain $\mathbf{K}_k$ via a Recurrent Neural Network:

$$\mathbf{K}_k = \text{RNN}_\theta\left(\Delta \tilde{\mathbf{y}}_k, \Delta \hat{\mathbf{x}}_k, \tilde{\mathbf{y}}_k\right)$$
$$\hat{\mathbf{x}}_{k|k} = \mathbf{F} \hat{\mathbf{x}}_{k-1|k-1} + \mathbf{K}_k (\mathbf{z}_k - \mathbf{H} \mathbf{F} \hat{\mathbf{x}}_{k-1|k-1})$$

```
+-----------------------------------------------------------------------------------------------+
| KalmanNet Architecture (Revach & Shlezinger 2022, Buchnik 2023):                             |
|                                                                                               |
|  x̂_{k|k-1} = F * x̂_{k-1|k-1}  (Physics-Based Prior)                                           |
|                  │                                                                            |
|                  ├──────────────────────────────────┐                                         |
|                  ▼                                  ▼                                         |
|         ỹ_k = z_k - H * x̂_{k|k-1}        [Feature Extractor / Diffs]                          |
|                  │                                  │                                         |
|                  │                                  ▼                                         |
|                  │                         ┌──────────────────┐                               |
|                  │                         │  RNN / GRU       │                               |
|                  │                         │  (Learns Gain)   │                               |
|                  │                         └────────┬─────────┘                               |
|                  │                                  │                                         |
|                  ▼                                  ▼                                         |
|         Innovation ỹ_k  ────────────►  Kalman Gain K_k = RNN_θ(...)                           |
|                  │                                  │                                         |
|                  └─────────────────┬────────────────┘                                         |
|                                    ▼                                                          |
|                  x̂_{k|k} = x̂_{k|k-1} + K_k * ỹ_k  (Exact State-Space Update)                  |
+-----------------------------------------------------------------------------------------------+
```

- **Latent-KalmanNet (Buchnik et al., 2023 [IEEE TSP]):** Extends KalmanNet to high-dimensional observation spaces by combining a learned convolutional/transformer encoder with latent-space tracking, circumventing the curse of dimensionality.
- **Adaptive KalmanNet (Ni et al., 2024 [IEEE ICASSP]):** Integrates a compact hypernetwork that generates context-dependent modulation weights, allowing the filter to adapt instantaneously to dynamic changes in process and measurement noise distributions without retraining.

### 4.3 Neural-Enhanced EKF via Front-End Vector Conditioning ($z_k$)
As highlighted in [`note_ini.md`](./note_ini.md), an exceptionally promising hybrid architecture places the neural network **at the front end of the Extended Kalman Filter**:

```text
Raw Distorted Observation                 Conditioned Observation                 Posterior State
[Received Pilots / Initial LS] ──► [Front-End Neural Network] ──► [Analytical EKF Engine] ──► [Predicted CSI]
(ICI, Doppler squint, PA skew)           z_k = g_θ(Y_k, Physics)         (State equations)          x̂_{k+1}
```

#### Mathematical Formulation:
In satellite and high-mobility communications, the true physical channel state vector $\mathbf{x}_k = [\boldsymbol{\alpha}_k^T, \boldsymbol{\tau}_k^T, \boldsymbol{\nu}_k^T]^T$ (path gains, delays, Doppler frequencies) is related to received pilot observations $\mathbf{Y}_k$ through non-ideal transformations contaminated by inter-carrier interference (ICI), RF amplifier non-linearities, and spatial beam squint:
$$\mathbf{Y}_k = \mathcal{G}_{\text{RF}}\left(\mathcal{H}(\mathbf{x}_k) \mathbf{S}_k\right) + \mathbf{N}_k$$

Instead of forcing the EKF to linearize this intractable observation operator:
1. **Front-End Neural Pre-Conditioning:** A specialized neural network $g_\theta(\cdot)$, informed by physical channel priors (e.g., fractional Fourier transforms or delay-Doppler symplectic transforms), maps the raw observation to a clean, well-conditioned linear measurement vector:
   $$\mathbf{z}_k = g_\theta(\mathbf{Y}_k, \hat{\mathbf{x}}_{k|k-1})$$
2. **Analytical EKF Update:** The conditioned vector $\mathbf{z}_k$ enters the classical EKF measurement update:
   $$\tilde{\mathbf{y}}_k = \mathbf{z}_k - h(\hat{\mathbf{x}}_{k|k-1})$$
   $$\hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + \mathbf{K}_k \tilde{\mathbf{y}}_k$$

This hybrid coupling guarantees:
- **Guaranteed Kinematic Stability:** State evolution remains constrained by physical motion equations.
- **Immunity to RF Non-Idealities:** The front-end NN absorbs non-linear RF distortions that would otherwise destabilize EKF Jacobian computations.
- **Interpretability:** The state vector $\mathbf{x}_k$ maintains physical units (Doppler in Hz, delays in ns, angles in radians).

### 4.4 Hypernetworks for Non-Stationary Adaptation
- **Liu et al. (2024) [IEEE TVT] (`LPCNet` / `JLPCNet`):** Developed a hypernetwork-based framework for non-stationary channel prediction. The hypernetwork dynamically generates and updates the weights of the primary predictor as terminal speed and channel statistics drift, maintaining superior downlink spectral efficiency under variable velocities.
- **Raviv & Shlezinger (2025) [IEEE OJ-SP]:** Demonstrated modular hypernetworks for adaptive deep receivers, dynamically modulating network parameters and architectures in response to instantaneous channel variations without retraining.

---

## 5. Bayesian Goodness-of-Fit & Non-Gaussian Distributional Adaptation

### 5.1 Breakdown of the Gaussian Residual Assumption
Classical Kalman filtering optimality hinges on the assumption that measurement residuals (innovations) are white zero-mean Gaussian:
$$\tilde{\mathbf{y}}_k = \mathbf{z}_k - \mathbf{H}_k \hat{\mathbf{x}}_{k|k-1} \sim \mathcal{N}\left(\mathbf{0}, \mathbf{S}_k\right), \quad \mathbf{S}_k = \mathbf{H}_k \mathbf{P}_{k|k-1} \mathbf{H}_k^H + \mathbf{R}_k$$

In practical non-terrestrial and high-mobility channels, this assumption breaks down due to:
- **Rician $K$-Factor Fluctuations:** Transitions between Line-of-Sight (LoS) and severe multipath shadowing yield non-stationary, heavy-tailed fading.
- **Non-Linear Front-End Saturation:** Power amplifier clipping and quantization noise introduce non-Gaussian kurtosis.
- **Doppler Dispersion Residuals:** When the front-end estimation vector $\mathbf{z}_k$ suffers residual Doppler leakage, the innovation distribution becomes skewed and multimodal. When unaddressed, standard EKF gain calculations become suboptimal or diverge entirely.

### 5.2 Bayesian Residual Evaluation & Dynamic Noise Covariance Estimation
To resolve this, Bayesian methods provide principled online validation and adaptation:

```text
Conditioned Measurement z_k
            │
            ▼
[Innovation Calculation]:  ỹ_k = z_k - H * x̂_{k|k-1}
            │
            ├──────────────────────────────────────────────┐
            ▼                                              ▼
[Empirical Goodness-of-Fit Test]             [Bayesian Covariance Update]
- Normalized Innovation Squared (NIS):       - Variational Bayesian (VB) Inference
  ε_k = ỹ_k^H * S_k^{-1} * ỹ_k ~ χ^2(d_z)     - Inverse-Wishart Prior on R_k:
- KL-Divergence / Kurtosis Check               R_k ~ Inv-Wishart(ν, Ψ)
            │                                              │
            ▼                                              ▼
[Distributional Alarm / Outlier Gating] ──► [Adaptive Measurement Covariance R_k]
                                                           │
                                                           ▼
                                            [Robust Posterior Update in EKF]
```

1. **Normalized Innovation Squared (NIS) Testing:**
   $$\epsilon_k = \tilde{\mathbf{y}}_k^H \mathbf{S}_k^{-1} \tilde{\mathbf{y}}_k$$
   Under standard Gaussian assumptions, $\epsilon_k$ follows a Chi-square distribution $\chi^2(d_z)$ with $d_z$ degrees of freedom. A Bayesian hypothesis test evaluates whether $\epsilon_k$ lies within confidence intervals $[c_{\text{lower}}, c_{\text{upper}}]$. Deviations signal either distribution shift, uncompensated Doppler burst, or sensor outlier.
2. **Variational Bayesian Adaptive Filtering (VBAKF):**
   Rather than assuming static $\mathbf{R}_k$, $\mathbf{R}_k$ is modeled as a latent random matrix governed by an Inverse-Wishart prior distribution:
   $$p(\mathbf{R}_k) = \mathcal{IW}(\mathbf{R}_k; \nu_0, \mathbf{\Psi}_0)$$
   Variational inference iteratively approximates the joint posterior of the channel state $\mathbf{x}_k$ and measurement noise covariance $\mathbf{R}_k$, dynamically adjusting the Kalman gain to prevent filter divergence under non-Gaussian noise bursts (Jia et al., 2024 [IEEE TAES]; Wang et al., 2026 [Information]).

### 5.3 Uncertainty Quantification (UQ) for Predictive Beamforming
Pure neural networks output point predictions $\hat{\mathbf{h}}_{k+\Delta t}$ without reliable confidence intervals. By maintaining the Bayesian state error covariance $\mathbf{P}_{k+\Delta t|k}$:
- The transmitter derives an explicit **ellipsoid of uncertainty**:
  $$\mathcal{E}_{1-\alpha} = \left\{\mathbf{h} : (\mathbf{h} - \hat{\mathbf{h}})^H \mathbf{P}^{-1} (\mathbf{h} - \hat{\mathbf{h}}) \le \chi^2_{d}(1-\alpha)\right\}$$
- **Robust Precoding Design:** Downlink beamformers can optimize worst-case Signal-to-Interference-plus-Noise Ratio (SINR) over the uncertainty ellipsoid rather than relying blindly on a single point prediction:
  $$\max_{\mathbf{w}} \min_{\mathbf{h} \in \mathcal{E}} \frac{|\mathbf{h}^H \mathbf{w}|^2}{\sum_{j \ne i} |\mathbf{h}_i^H \mathbf{w}_j|^2 + \sigma^2}$$
  This protects mobile LEO and V2X links against catastrophic beam mispointing.

---

## 6. Architectural Comparison & Taxonomy Matrix

The following matrix contrasts the prevailing paradigms in channel prediction:

| Metric / Dimension | Classical Predictors (AR, KF, EKF) | Pure Deep Learning (LSTM, TCN) | Modern Transformers (LinFormer, ST-Trans) | Hybrid Physics-Informed (KalmanNet, NN-EKF) |
| :--- | :--- | :--- | :--- | :--- |
| **Model Nature** | Model-based analytical | Data-driven black-box | Data-driven attention | Hybrid model-aided AI |
| **Physics Knowledge Required** | Complete ($\mathbf{F}, \mathbf{H}, \mathbf{Q}, \mathbf{R}$) | None (Data only) | None (Data only) | Partial / Domain physics |
| **Doppler Drift Tracking** | Poor (requires manual re-estimation) | Moderate | High | Excellent (adaptive gain / latent space) |
| **Long-Horizon Accuracy** | Rapid error compounding | Moderate decay | Superior attention span | Superior + bounded error covariance |
| **Inference Latency** | $\mathcal{O}(M^3)$ matrix inversion | Very low ($\approx 0.1\text{ ms}$) | $\mathcal{O}(L^2)$ or $\mathcal{O}(L)$ (LinFormer) | Low to moderate (< $0.5\text{ ms}$) |
| **Sample Efficiency** | Optimal (zero training) | Poor (requires $\ge 10^5$ samples) | Very poor (data hungry) | High (requires small training set) |
| **Distributional Robustness** | Fails under non-Gaussian noise | Unreliable outside training set | Degrades without fine-tuning | High (Bayesian adaptive noise tuning) |
| **Uncertainty Quantification** | Exact analytical ($\mathbf{P}_k$) | None / Heuristic dropout | Heuristic ensemble | Explicit Bayesian posterior $\mathbf{P}_k$ |
| **Representative Citations** | Das & Moura (2016) | Jiang (2020), Yuan (2020) | Jin (2025), Stenhammar (2024) | Shlezinger (2022), Revach (2022), Sun (2025) |

---

## 7. Open Challenges, System Applications & Future Research Directions

### 7.1 Predictive Beamforming, Link Adaptation & Proactive Handover
The ultimate operational objective of channel prediction is closing the feedback loop under rapid terminal and satellite mobility:
- **Predictive Zero-Forcing / MMSE Beamforming:** Instead of calculating spatial precoders $\mathbf{W}_k = \mathbf{H}_k^H (\mathbf{H}_k \mathbf{H}_k^H + \alpha \mathbf{I})^{-1}$ with outdated CSI $\mathbf{H}_k$, the base station computes precoding vectors using forecasted CSI $\hat{\mathbf{H}}_{k+\Delta t}$. This eliminates multi-user interference (MUI) leakage and restores the theoretical sum-rate capacity of massive MIMO downlinks.
- **Proactive Cell Handover:** By predicting reference signal received power (RSRP) and beam quality across neighboring candidate cells ([Li et al., IEEE Wireless Communications 2026](https://doi.org/10.1109/mwc.2026.3691074)), mobile networks execute proactive handovers before link dropouts occur, drastically suppressing handover failure rates.
- **Doppler Pre-Compensation:** In high-speed rail and LEO satellite links, forecasted Doppler drift trajectories enable anticipatory carrier frequency offset (CFO) compensation, preserving subcarrier orthogonality and suppressing inter-carrier interference (ICI).

### 7.2 Real-Time Hardware Budgets & Inference Latency Deadlines (<1 ms)
In practical 5G-NR and 6G standards, the slot duration at subcarrier spacing (SCS) of $15\text{ kHz}$ is $1\text{ ms}$, dropping to $0.5\text{ ms}$ at $30\text{ kHz}$ and $0.125\text{ ms}$ at $120\text{ kHz}$ (mmWave):
- **The Latency Paradox:** If a deep neural predictor requires $2\text{ ms}$ to predict the channel at $\Delta t = 1\text{ ms}$, the forecasted channel is already outdated before inference finishes.
- **Lightweight Architectures:** Recent works like `LinFormer` ([Jin et al., IEEE TWC 2025](https://doi.org/10.1109/twc.2025.3558950)) and model-unfolded filters demonstrate that all-linear time-aware MLPs or recurrent state updates with $\le 50\text{k}$ parameters achieve sub-millisecond execution on baseband DSP/FPGA engines.
- **Quantization & Operator Fusion:** Fixed-point INT8/FP8 quantization and fused complex-valued kernel executions are essential to satisfy baseband power and latency envelopes without destabilizing matrix operations.

### 7.3 Self-Supervised & Label-Free Training Schemes
A major operational bottleneck of supervised deep learning in channel prediction is the lack of "clean ground-truth" future channels $\mathbf{H}_{k+\Delta t}$ in live commercial deployments:
- **Measurement-Only Self-Supervision:** Emerging frameworks utilize self-supervised next-step prediction, where the future received pilot observations $\mathbf{Y}_{k+\Delta t}$ serve as supervisory signals under maximum likelihood or variational loss criteria.
- **Label-Free State-Space Models:** As demonstrated by [Sun et al., IEEE TMC 2025](https://doi.org/10.1109/tmc.2025.3564260), embedding data-driven networks into state-space models enables training solely on unlabelled historical CSI measurements, achieving robust mmWave tracking without requiring synthetic or offline channel ground truth.

### 7.4 Continuous-Time Prediction & Non-Uniform Pilot Sampling
Traditional discrete sequence models predict channels at fixed integer time steps ($k+1, k+2, \dots$). However, modern cellular protocols dynamically adapt pilot density:
- **Continuous Temporal Dynamics:** Utilizing Neural Ordinary Differential Equations (Neural ODEs) ([Cui et al., China Communications 2024](https://doi.org/10.23919/jcc.fa.2022-0712.202401); [Sang et al., IEEE TWC 2026](https://doi.org/10.1109/twc.2026.3665056)) enables continuous-time channel tracking, evaluating future CSI at arbitrary continuous timestamps $\tau \in \mathbb{R}^+$.
- **Sparse Non-Uniform Pilots:** Optimized non-uniform pilot patterns (such as Chebyshev polynomial root layouts) eliminate Doppler aliasing at extreme velocities while significantly reducing pilot power and spectral overhead.

---

## 8. Comprehensive Annotated Bibliography

### 8.1 Model-Based Deep Learning & Hybrid Filtering Foundations
- **Shlezinger, N., Eldar, Y. C., & Boyd, S. (2022).** *"Model-Based Deep Learning: On the Intersection of Deep Learning and Optimization."* **IEEE Access**, 10, 115384–115406. [DOI: 10.1109/ACCESS.2022.3218802](https://doi.org/10.1109/ACCESS.2022.3218802).  
  *Significance:* Establishes the formal theoretical continuum between analytical optimization/filtering and deep neural networks, laying out design principles for algorithm unfolding and neural-augmented state-space estimation.
- **Revach, G., Shlezinger, N., Ni, X., Escoriza, A. L., van Sloun, R. J. G., & Eldar, Y. C. (2022).** *"KalmanNet: Neural Network Aided Kalman Filtering for Partially Known Dynamics."* **IEEE Transactions on Signal Processing**, 70, 1532–1547. [DOI: 10.1109/TSP.2022.3158588](https://doi.org/10.1109/TSP.2022.3158588).  
  *Significance:* Introduces KalmanNet, demonstrating how an RNN can learn the optimal Kalman gain $\mathbf{K}_k$ directly from trajectory data without prior knowledge of process and measurement noise covariance matrices ($\mathbf{Q}, \mathbf{R}$).
- **Buchnik, I., Revach, G., Steger, D., van Sloun, R. J. G., Routtenberg, T., & Shlezinger, N. (2023).** *"Latent-KalmanNet: Learned Kalman Filtering for Tracking From High-Dimensional Signals."* **IEEE Transactions on Signal Processing**, 71, 4425–4440. [DOI: 10.1109/TSP.2023.3344360](https://doi.org/10.1109/TSP.2023.3344360).  
  *Significance:* Extends hybrid filtering to high-dimensional sensory and communications data by coupling an autoencoder with latent-space KalmanNet filtering.
- **Ni, X., Revach, G., & Shlezinger, N. (2024).** *"Adaptive KalmanNet: Data-Driven Kalman Filter with Fast Adaptation."* **IEEE ICASSP 2024**, 9201–9205. [DOI: 10.1109/ICASSP48485.2024.10447012](https://doi.org/10.1109/ICASSP48485.2024.10447012).  
  *Significance:* Implements hypernetwork-based weight modulation for KalmanNet, allowing instantaneous adaptation to non-stationary noise distributions without retraining.
- **Sun, Y., He, J., Lin, Z., Pu, W., Yin, F., & So, H. C. (2025).** *"Hybrid Data-Driven SSM for Interpretable and Label-Free mmWave Channel Prediction."* **IEEE Transactions on Mobile Computing**, 24(5), 3120–3135. [DOI: 10.1109/TMC.2025.3564260](https://doi.org/10.1109/TMC.2025.3564260).  
  *Significance:* Embeds neural networks inside a state-space model for millimeter-wave channel prediction, trained completely label-free in an unsupervised manner while preserving physical interpretability.
- **Piroddi, A., Kanakis, T., & Agyeman, M. O. (2026).** *"WARDEN: Wiener-Adaptive Residual Dynamic ENcoder for Channel Charting in Future Cellular Networks."* **IEEE Access**, 14, 18920–18935. [DOI: 10.1109/ACCESS.2026.3723268](https://doi.org/10.1109/ACCESS.2026.3723268).  
  *Significance:* Decomposes channel dynamics into an analytical Wiener-Hopf optimal linear transition matrix alongside a lightweight neural residual network.

### 8.2 Deep Learning Architectures for Channel Prediction
- **Ying, M., Gao, Z., Su, Y., Chen, S., & Di Renzo, M. (2024).** *"Deep Learning-Based Joint Channel Prediction and Multibeam Precoding for LEO Satellite Internet of Things."* **IEEE Transactions on Wireless Communications**, 23(10), 14205–14220. [DOI: 10.1109/TWC.2024.3406952](https://doi.org/10.1109/TWC.2024.3406952).  
  *Significance:* Demonstrates joint channel prediction and multibeam precoding for LEO satellite constellations under extreme Doppler shifts and propagation delays using spatiotemporal learning and VAE channel augmentation.
- **Jiang, Y. P., Lin, W., Zhao, W., & Wang, C. (2023).** *"AcsiNet: Attention-Based Deep Learning Network for CSI Prediction in FDD MIMO Systems."* **IEEE Wireless Communications Letters**, 12(4), 659–663. [DOI: 10.1109/LWC.2022.3230950](https://doi.org/10.1109/LWC.2022.3230950).  
  *Significance:* Validates the superiority of temporal attention over CNNs and LSTMs in massive MIMO CSI prediction, enabling direct downlink CSI forecasting from uplink compressed features.
- **Jiang, F., Pan, C., Dong, L., Wang, K., Debbah, M., Niyato, D., & Han, Z. (2026).** *"A Comprehensive Survey of Large AI Models for Future Communications: Foundations, Applications, and Challenges."* **IEEE Communications Surveys & Tutorials**, Early Access. [DOI: 10.1109/COMST.2026.3660844](https://doi.org/10.1109/COMST.2026.3660844).  
  *Significance:* Provides a comprehensive taxonomy of next-generation physical-layer AI models, covering Transformers, Diffusion, and Selective State Space Models (Mamba) for channel prediction and mobile tracking.
- **Stenhammar, O., Fodor, G., & Fischione, C. (2024).** *"A Comparison of Neural Networks for Wireless Channel Prediction."* **IEEE Wireless Communications**, 31(2), 140–147. [DOI: 10.1109/MWC.006.2300140](https://doi.org/10.1109/MWC.006.2300140).  
  *Significance:* Comprehensive comparative study assessing LSTMs, GRUs, CNNs, TCNs, and Transformers under standardized 3GPP TDL channels; provides guidelines for latency-accuracy trade-offs.
- **Jin, Y., Wu, Y., Gao, Y., Zhang, S., Xu, S., & Wang, C.-X. (2025).** *"LinFormer: A Linear-Based Lightweight Transformer Architecture for Time-Aware MIMO Channel Prediction."* **IEEE Transactions on Wireless Communications**, 24(3), 2110–2125. [DOI: 10.1109/TWC.2025.3558950](https://doi.org/10.1109/TWC.2025.3558950).  
  *Significance:* Replaces conventional attention with a time-aware MLP, achieving linear complexity $\mathcal{O}(L)$ and superior prediction accuracy in high-mobility massive MIMO systems.
- **Rizzello, V., Böck, B., Joham, M., & Utschick, W. (2023).** *"Reverse Ordering Techniques for Attention-Based Channel Prediction."* **IEEE Open Journal of Signal Processing**, 4, 520–533. [DOI: 10.1109/OJSP.2023.3344024](https://doi.org/10.1109/OJSP.2023.3344024).  
  *Significance:* Introduces reverse positional encoding to prioritize the most recent channel snapshots, delivering robustness against variable sequence lengths without increasing model complexity.
- **Liu, G., Hu, Z., Wang, L., Zhang, H., Xue, J., & Matthaiou, M. (2024).** *"A Hypernetwork Based Framework for Non-Stationary Channel Prediction."* **IEEE Transactions on Vehicular Technology**, 73(6), 8420–8434. [DOI: 10.1109/TVT.2024.3355557](https://doi.org/10.1109/TVT.2024.3355557).  
  *Significance:* Proposes `LPCNet` and `JLPCNet`, utilizing hypernetworks to dynamically update predictor weights as mobile speed variations alter the input CSI distribution.
- **Sang, Y., Ma, K., Yao, L., Wang, P., Wang, Z., Han, Z., & Chen, S. (2026).** *"Continuous-Time Transformer-Based Channel Prediction With Non-Uniform Pilot Pattern."* **IEEE Transactions on Wireless Communications**, 25(2), 1045–1060. [DOI: 10.1109/TWC.2026.3665056](https://doi.org/10.1109/TWC.2026.3665056).  
  *Significance:* Merges continuous-time Neural ODEs with Transformers over non-uniform pilot patterns, resolving Doppler aliasing under high mobility with minimal pilot overhead.
- **Cui, M., Jiang, H., Chen, Y., Du, Y., & Dai, L. (2024).** *"Continuous-Time Channel Prediction Based on Tensor Neural Ordinary Differential Equation."* **China Communications**, 21(1), 112–124. [DOI: 10.23919/JCC.fa.2022-0712.202401](https://doi.org/10.23919/JCC.fa.2022-0712.202401).  
  *Significance:* Uses Neural ODEs to realize direct continuous prediction of intra-frame channel states, bypassing conventional discrete interpolation loss.
- **Jiang, W., & Schotten, H. D. (2020).** *"Deep Learning for Fading Channel Prediction."* **IEEE Open Journal of the Communications Society**, 1, 320–332. [DOI: 10.1109/OJCOMS.2020.2982513](https://doi.org/10.1109/OJCOMS.2020.2982513).  
  *Significance:* Seminal demonstration of deep recurrent neural networks (LSTM/GRU) for multi-antenna fading channel prediction against shallow RNN baselines.
- **Yuan, J., Ngo, H. Q., & Matthaiou, M. (2020).** *"Machine Learning-Based Channel Prediction in Massive MIMO With Channel Aging."* **IEEE Transactions on Wireless Communications**, 19(9), 5878–5893. [DOI: 10.1109/TWC.2020.2969627](https://doi.org/10.1109/TWC.2020.2969627).  
  *Significance:* Derives closed-form spectral efficiency and per-user throughput expressions under ML-based CSI prediction in massive MIMO with channel aging.
- **Joo, J., Park, M. C., Han, D. S., & Pejović, V. (2019).** *"Deep Learning-Based Channel Prediction in Realistic Vehicular Communications."* **IEEE Access**, 7, 27846–27858. [DOI: 10.1109/ACCESS.2019.2901710](https://doi.org/10.1109/ACCESS.2019.2901710).  
  *Significance:* Field validation using real-world IEEE 802.11p vehicular IQ traces, proving a 15%–25% RMSE improvement in CSI forecasting over static baseline methods.

### 8.3 Classical Estimation & Bayesian Filtering Baselines
- **Das, S., & Moura, J. M. F. (2016).** *"Consensus+Innovations Distributed Kalman Filter With Optimized Gains."* **IEEE Transactions on Signal Processing**, 65(2), 415–428. [DOI: 10.1109/TSP.2016.2617827](https://doi.org/10.1109/TSP.2016.2617827).  
  *Significance:* Foundational analysis on tracking capacities and stability bounds of Kalman filtering across dynamic networked fields.
- **Jia, C., Ma, J., & Kouw, W. M. (2024).** *"Multiple Variational Kalman-GRU for Ship Trajectory Prediction With Uncertainty."* **IEEE Transactions on Aerospace and Electronic Systems**, 60(6), 8120–8135. [DOI: 10.1109/TAES.2024.3491053](https://doi.org/10.1109/TAES.2024.3491053).  
  *Significance:* Illustrates the combination of Variational Kalman Filtering with GRU networks to estimate time-varying noise covariances and multimodal kinematics with explicit uncertainty quantification.
- **Wang, N., et al. (2026).** *"Adaptive Measurement Noise Covariance Estimation Using a Linear-Attention Transformer."* **Information**, 17(3), 294. [DOI: 10.3390/info17030294](https://doi.org/10.3390/info17030294).  
  *Significance:* Explores transformer-driven adaptive estimation of the measurement covariance matrix $\mathbf{R}_k$ to maintain filter stability under non-Gaussian sensory noise.
- **Raviv, T., & Shlezinger, N. (2025).** *"Modular Hypernetworks for Scalable and Adaptive Deep MIMO Receivers."* **IEEE Open Journal of Signal Processing**, 6, 120–135. [DOI: 10.1109/OJSP.2025.3526548](https://doi.org/10.1109/OJSP.2025.3526548).  
  *Significance:* Modular hypernetworks that update receiver processing in response to instantaneous channel variations, eliminating retraining overhead.
- **Li, W., Chen, W., Ai, B., Zhang, Y., Peng, Y., & Matthaiou, M. (2026).** *"LLM–Empowered Wireless Channel Quality Prediction for Reliable Cell Handover."* **IEEE Wireless Communications**, 33(1), 88–95. [DOI: 10.1109/MWC.2026.3691074](https://doi.org/10.1109/MWC.2026.3691074).  
  *Significance:* Demonstrates large-scale foundation model adaptations (GPT-2 backbone with beam embeddings) for spatiotemporal wireless channel quality and RSRP forecasting in dense mobile networks.
