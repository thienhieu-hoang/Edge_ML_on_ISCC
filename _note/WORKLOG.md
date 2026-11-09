# Project Worklog

<!-- NOTE: Latest dates and newest entries are placed at the top -->

## 07/10/2026

<div style="display: flex; gap: 24px; margin: 12px 0 24px 0;">
  <div style="flex: 1; float: left; width: 48%;">

### 🛠️ Action (What I do)
- Evaluated UDA transfer learning performance using CORAL and FDA on LEO satellite-to-ground channel dataset.
- Ran validation inference scripts in `Hest_NTN_UDA_clean/eval_uda.py` across SNR range `[-5dB, 20dB]`.

  </div>
  <div style="flex: 1; float: right; width: 48%;">

### 📊 Results
- **NMSE Improvement:** FDA achieved a **2.8 dB gain** in normalized MSE over baseline non-adapted model at low SNR.
- Generated comparison convergence plots in `z_Simulation notes/results_report/`.

<img src="attachements/Pasted image 20260918163611.png" alt="NMSE vs SNR Comparison" style="max-width: 100%; height: auto; border-radius: 6px; border: 1px solid #d0d7de; margin-top: 8px;" />

*Figure 1: NMSE vs. SNR performance across UDA methods.*

  </div>
  <div style="clear: both;"></div>
</div>

$$
\text{NMSE} = 10 \log_{10} \left( \frac{\|\mathbf{H} - \hat{\mathbf{H}}\|_F^2}{\|\mathbf{H}\|_F^2} \right)
$$

<hr/>

<div style="display: flex; gap: 24px; margin: 12px 0 24px 0;">
  <div style="flex: 1; float: left; width: 48%;">

### 🛠️ Action (What I do)
- Updated project guidelines and `.agent/rules/main.md` logging schema to adopt floating two-column layout.
- Initialized clean worklog structure in `WORKLOG.md`.

  </div>
  <div style="flex: 1; float: right; width: 48%;">

### 📊 Results
- Rules modernized to eliminate markdown tables and present actions and results side-by-side with reverse-chronological ordering.

  </div>
  <div style="clear: both;"></div>
</div>
<hr/>

## 06/10/2026

<div style="display: flex; gap: 24px; margin: 12px 0 24px 0;">
  <div style="flex: 1; float: left; width: 48%;">

### 🛠️ Action (What I do)
- Generated high-mobility NTN channel realization matrices using Sionna simulator in `Gene_NTN_Data`.
- Configured 3GPP TR 38.811 NTN parameters: orbit altitude 600 km, S-band carrier frequency 2 GHz.

  </div>
  <div style="flex: 1; float: right; width: 48%;">

### 📊 Results
- Successfully exported `ntn_channel_h_samples_50k.h5` dataset (50,000 CIR realizations).
- Doppler shift profile validated against theoretical maximum trajectory angles.

  </div>
  <div style="clear: both;"></div>
</div>
<hr/>
