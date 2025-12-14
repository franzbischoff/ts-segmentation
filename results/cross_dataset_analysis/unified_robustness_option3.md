# Unified Robustness Score (Option 3)

Generated: 2025-12-14T21:48:59.082908

## Executive Summary

This analysis combines both dimensions from Options 1 and 2 into a single **unified robustness metric**:

$$\text{Robustness Score} = 0.6 \times (1 - \text{2-fold gap}) + 0.4 \times (1 - \text{transfer variance})$$

**Score Range**: 0 to 1 (higher = more robust)

### Final Ranking

| Rank | Detector | Unified Score | Intra-Consistency | Inter-Generalization | Ceiling F3 | Transfer CV |
|------|----------|---------------|-------------------|----------------------|------------|------------|
| 1 | **floss** | 0.9763 | 0.9789 | 0.9723 | 0.4285 | 21.9% |
| 2 | **adwin** | 0.9713 | 0.9576 | 0.9919 | 0.2879 | 9.5% |
| 3 | **kswin** | 0.9690 | 0.9558 | 0.9887 | 0.3176 | 12.1% |
| 4 | **hddm_a** | 0.9509 | 0.9540 | 0.9463 | 0.2997 | 35.5% |
| 5 | **hddm_w** | 0.9426 | 0.9788 | 0.8882 | 0.1527 | 73.2% |
| 6 | **page_hinkley** | 0.9049 | 0.9484 | 0.8396 | 0.3132 | 73.7% |

---

## Detailed Analysis

### Top 3 Recommendations


**🥇 #1: floss**
- **Unified Score**: 0.9763
- **Intra-Dataset Consistency**: 0.9789 (stable across folds)
- **Inter-Dataset Generalization**: 0.9723 (stable across datasets)
- **Ceiling Performance (F3)**: 0.4285
- **Transfer Variability**: 21.9% (CV across transfers)


**🥈 #2: adwin**
- **Unified Score**: 0.9713
- **Intra-Dataset Consistency**: 0.9576 (stable across folds)
- **Inter-Dataset Generalization**: 0.9919 (stable across datasets)
- **Ceiling Performance (F3)**: 0.2879
- **Transfer Variability**: 9.5% (CV across transfers)


**🥉 #3: kswin**
- **Unified Score**: 0.9690
- **Intra-Dataset Consistency**: 0.9558 (stable across folds)
- **Inter-Dataset Generalization**: 0.9887 (stable across datasets)
- **Ceiling Performance (F3)**: 0.3176
- **Transfer Variability**: 12.1% (CV across transfers)


---

## Interpretation Guide

### What Each Component Measures

**Intra-Dataset Consistency** (Weight 0.6):
- Measures stability between folds within the same dataset
- High value (≥0.95) = detector parameters are stable across data splits
- Low value (<0.70) = detector highly sensitive to training data distribution
- **Interpretation**: How much can you trust parameters to generalize to new data from same source?

**Inter-Dataset Generalization** (Weight 0.4):
- Measures stability of parameter transfers across different datasets
- High value (≥0.80) = detector works reliably across dataset types
- Low value (<0.50) = detector requires re-tuning for new datasets
- **Interpretation**: How portable are the parameters to new domains?

### Why These Weights?

- **0.6 for Intra**: Dominant weight because consistent parameters within domain are foundational
- **0.4 for Inter**: Secondary weight because transfer is less critical than baseline reliability

### Rationale for the Unified Formula

- **Multiobjective weighted-sum**: Combinar objetivos normalizados via pesos explícitos é o método clássico em otimização multiobjetivo; aqui, consolidamos performance intra (1−gap) e estabilidade inter (1−variance) num único escalar comparável.
- **Generalização = estabilidade + variância**: A robustez prática depende de consistência no domínio (pouca sensibilidade a splits) e baixa variância ao transferir para novos domínios; a fórmula captura exatamente essas duas dimensões.
- **Pesos transparentes e ajustáveis**: 0.6/0.4 refletem prioridade prática (confiabilidade interna ligeiramente mais importante que portabilidade), mas podem ser recalibrados conforme a tolerância a risco de transferência.
- **Fontes literárias**:
	- Deb, K. *Multi-Objective Optimization Using Evolutionary Algorithms*. Wiley, 2001. (weighted-sum como método base de agregação multiobjetivo)
	- Quiñonero-Candela et al. *Dataset Shift in Machine Learning*. MIT Press, 2009. (robustez vs. variância sob mudança de domínio)
	- Keeney, R., Raiffa, H. *Decisions with Multiple Objectives*. Cambridge Univ. Press, 1993. (pesos explícitos e preferências em decisão multicritério)

---

## Production Guidance by Score Range

- **🟢 Excellent** (0.85 - 1.0): Production-ready, minimal validation needed
- **🟡 Good** (0.75 - 0.84): Production-viable with standard validation
- **🟠 Acceptable** (0.60 - 0.74): Production-viable with enhanced monitoring
- **🔴 Poor** (0.0 - 0.59): Research use only, re-tuning required

---

## Comparison with Option 1 and Option 2

| Metric | Option 1 | Option 2 | Option 3 |
|--------|----------|----------|----------|
| **Focus** | Ceiling performance with local tuning | Parameter transfer across datasets | Combined robustness |
| **Best For** | Research, max performance | Production deployment | Holistic detector selection |
| **Questions Answered** | What's the best we can do if we retune? | Can we use params without retuning? | Which detector is most reliable overall? |
| **Winner Typically** | FLOSS (performance focused) | ADWIN (robustness focused) | KSWIN (balanced) |

---

## Dataset-Level Summary

This unified score is computed from macro-averages across all three datasets:
- **afib_paroxysmal**: Largest dataset (229 files)
- **malignantventricular**: Medium dataset (22 files)
- **vtachyarrhythmias**: Smallest dataset (34 files)

Detectors performing well on small datasets (vtachy) and hard datasets (malign) get higher robustness scores because they demonstrate consistency despite domain challenges.

---

## Recommendations

### For Research/Benchmarking
- **Use FLOSS** (Option 1: F3=0.4285 ceiling)
- Accept the tuning cost, get maximum performance

### For Production Deployment
- **Use detector ranked #1 in Option 3** (unified score)
- Provides best balance of ceiling + portability + stability

### For Heterogeneous Data
- **Ensemble approach**: Top 2 detectors from Option 3
- Voting or weighted combination improves overall reliability

### For Extreme Resource Constraints
- **Use ADWIN** (excellent portability, zero re-tuning cost)
- Accept lower ceiling for maximum convenience

---

## Technical Notes

- Variance normalization uses min-max scaling to 0-1 range
- Weights (0.6 / 0.4) are tunable but balanced towards practical deployment
- All metrics computed from aggregated results (no per-file recomputation)
- Score is deterministic and reproducible
