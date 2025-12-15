# Dataset Comparisons: `afib_paroxysmal`

**Last Updated:** 2025-12-15 16:24:34 (✅ SUCCESS)


**Dataset**: Paroxysmal Atrial Fibrillation
**Ficheiros**: 229
**Eventos de Regime**: 1,301
**Samples Totais**: 41.3M @ 250 Hz
**Lead**: II (padrão para análise de ritmo)

---

## 📊 Resumo Executivo

### Top Detectors por Métrica (melhor configuração)

| Métrica | Top Detector | Score | Config |
|---------|---|---|---|
| **F3-Weighted** ⭐ | FLOSS | 0.3397 | window_size=75, regime_threshold=0.7 |
| **F3-Classic** | KSWIN | 0.4948 | ma=10, gap=2000 |
| **Recall@10s** | KSWIN | 99.44% | ma=50, gap=1000 |
| **Precision@10s** | FLOSS | 20.98% | gap=200 |
| **FP/min** | FLOSS | 2.32 | gap=200 |
| **NAB Standard** | FLOSS | -3.07 | gap=200 |
| **EDD Median** | FLOSS | 2.66s | gap=200 |

### 🎯 Recomendações por Cenário

| Cenário | Detector | Razão |
|---------|----------|-------|
| **Máxima Performance** | FLOSS | F3=0.3397 (melhor em dataset) |
| **Recall (não perder eventos)** | KSWIN | 99.44% detecção em 10s |
| **Mínimos Alarmes Falsos** | FLOSS | 2.32 FP/min (vs 9.43 KSWIN) |
| **Balanced (production)** | KSWIN | Bom trade-off recall/precision |
| **Rápida detecção** | FLOSS | EDD=2.66s (vs 2.89s KSWIN) |

---

## 📁 Ficheiros Disponíveis

### Relatórios Gerados (via `compare_detectors.py`)
- **`comparative_report.md`** - Análise detalhada de trade-offs
- **`detector_rankings.csv`** - Rankings numéricos
- **`detector_summary.csv`** - Resumo de melhores configs
- **`constraint_tradeoffs.csv`** - Análise de trade-offs
- **`robustness.csv`** - Análise de robustez paramétrica

### Visualizações (Fase 2 - em preparação)
- **`visualizations/radar_6detectors.png`** - Radar chart (6 detectores × 6 métricas)
- **`visualizations/f3_vs_fp_scatter.png`** - Scatter plot trade-off
- **`visualizations/heatmap_metrics_comparison.png`** - Heatmap de performance
- **`visualizations/parameter_tradeoffs.png`** - 3D/parallel coordinates

---

## 🔍 Análise Detalhada por Detector

### 1. **FLOSS** 🥇 (F3-Weighted)
**Melhor Configuração**: window_size=75, regime_threshold=0.7, regime_landmark=4.0, min_gap=1000
- F3-weighted: **0.3397** ⭐
- Precision@10s: **20.98%** (melhor em precision)
- FP/min: **2.32** (menos alarmes falsos)
- EDD: **2.66s** (detecção rápida)
- Vantagem: Excelente em reduzir falsos positivos
- Desvantagem: Recall=59.21% (perde eventos)

### 2. **KSWIN** 🥈 (F3-Classic)
**Melhor Configuração**: alpha=0.005, window_size=500, ma_window=50, min_gap=1000
- F3-weighted: 0.2435
- Recall@10s: **99.44%** (quase não perde eventos)
- FP/min: 9.43 (muitos alarmes falsos)
- EDD: 2.89s
- Vantagem: Máximo recall (captura quase tudo)
- Desvantagem: Muitos falsos positivos

### 3. **Page-Hinkley** 🥉
**Melhor Configuração**: lambda=1.0, delta=0.04, alpha=0.9999, ma_window=50, min_gap=1000
- F3-weighted: 0.1551
- Recall@10s: 39.88%
- FP/min: 3.08 (segundo melhor)
- Vantagem: Bom trade-off após FLOSS
- Desvantagem: Recall moderado

### 4. **ADWIN**
**Melhor Configuração**: delta=0.005, ma_window=300, min_gap=1000
- F3-weighted: 0.1603
- Recall@10s: 60.53%
- FP/min: 10.00
- Vantagem: Recall decente
- Desvantagem: Mais alarmes que FLOSS

### 5. **HDDM_A**
**Melhor Configuração**: drift_confidence=0.005, warning_confidence=0.001, two_side=true, ma_window=1, min_gap=1000
- F3-weighted: 0.1547
- Recall@10s: 47.35%
- FP/min: 3.75
- Vantagem: Moderado trade-off
- Desvantagem: Recall e precision baixos

### 6. **HDDM_W**
**Melhor Configuração**: drift_confidence=0.005, warning_confidence=0.001, lambda=0.2, two_side=false, ma_window=1, min_gap=1000
- F3-weighted: 0.1489
- Recall@10s: 46.45%
- FP/min: 3.84
- Vantagem: Estável
- Desvantagem: Performance baixa em todas as métricas

---

## ⚖️ Trade-Offs Principales

### F3-Weighted vs Recall@10s
```
         99.44% Recall ← KSWIN (mas 9.43 FP/min)
         │
         │ Trade-off: High Recall, High FP
         │
   ADWIN │ 60% Recall, 10 FP/min
         │
   FLOSS │ 59% Recall, 2.32 FP/min ← Low FP, Acceptable Recall
         │
    Page │ 40% Recall, 3.08 FP/min
         │
         ↓
       Low Recall, Low FP
```

### Decisão Prática
- **Clínica**: KSWIN (não pode perder eventos, acepita mais alarmes)
- **Alertas Automatizados**: FLOSS (minimizar alarmes falsos)
- **Research**: KSWIN (F3=0.2435 melhor que FLOSS=0.1129 em configs médias)

---

## 📈 Variabilidade Paramétrica

### FLOSS: Estável (baixa variabilidade)
- Mean F3: 0.112 ± 0.176
- Configs boas: window_size < 100, regime_threshold ∈ [0.6, 0.8]

### KSWIN: Média variabilidade
- Mean F3: 0.251 ± 0.215
- Configs boas: window_size ∈ [200, 750], alpha pequeno

### ADWIN: Média variabilidade
- Mean F3: 0.160 ± 0.150
- Configs boas: delta pequeno, ma_window > 100

### Page-Hinkley: Estável
- Mean F3: 0.105 ± 0.080

### HDDM_A/W: Baixa variabilidade
- Configs mais homogêneas, menos sensíveis a parâmetros

---

## 🔧 Como Usar Este Dataset

### Para Otimização
1. Usar FLOSS com `window_size` no range [50, 100]
2. Variar `regime_threshold` ∈ [0.6, 0.85]
3. Manter `min_gap` em 1000 (evita clustering)

### Para Produção Imediata (sem tuning)
- Usar FLOSS configs default: window_size=75, regime_threshold=0.7, min_gap=1000
- Performance esperada: F3≈0.34

### Para Alta Recall (clínica)
- Usar KSWIN: ma_window=50, min_gap=1000
- Performance esperada: Recall=99.44%, mas FP/min=9.43

---

## 📚 Ver Também

- **Comparação Cross-Dataset**: [`../cross_dataset/`](../cross_dataset/)
- **Análise Two-Fold**: [`../../cross_dataset_analysis/`](../../cross_dataset_analysis/)
- **Resultados por Detector**: [`../../<detector>/`](../../)
- **Relatório Completo**: [`./comparative_report.md`](./comparative_report.md)

---

**Última Atualização**: 2025-12-15
**Status**: Estrutura pronta; visualizações a ser geradas na Fase 2
