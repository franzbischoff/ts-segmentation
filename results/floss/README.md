# Resultados do Detector FLOSS

**Status**: ✅ COMPLETO (17 novembro 2025)

Este diretório contém os resultados completos do detector FLOSS (Fast Low-rank Online Subspace Tracking) aplicado ao dataset completo de regimes de fibrilação atrial.

## 📊 Ficheiros Gerados

### Predições e Métricas
- **`predictions_intermediate.csv`** (989,280 linhas) - Predições brutas para todas combinações de parâmetros
- **`metrics_comprehensive_with_nab.csv`** (989,280 linhas) - Métricas detalhadas (F1/F3, NAB, temporais)
- **`metrics_comprehensive_with_nab.jsonl`** (989,280 linhas) - Formato alternativo JSONL
- **`final_report_with_nab.json`** (~50 KB) - Relatório consolidado com melhores configurações
- **`metrics_comprehensive_with_nab_summary.json`** (~5 KB) - Estatísticas agregadas

### Estatísticas do Dataset
- **229 ficheiros únicos** de ECG
- **4,320 combinações de parâmetros** testadas
- **989,280 avaliações totais** (229 × 4,320)
- **1,301 eventos ground truth** (média de 5.68 por ficheiro)

### Visualizações (PNG)
- `pr_scatter_plots.png` - Gráficos de dispersão Precision-Recall
- `pareto_front.png` - Frente de Pareto (soluções não-dominadas)
- `heatmap_f3-weighted.png` - Sensibilidade de parâmetros para F3*
- `heatmap_nab-score-standard.png` - Sensibilidade para NAB Standard
- `heatmap_recall-10s.png` - Sensibilidade para Recall@10s
- `heatmap_fp-per-min.png` - Sensibilidade para taxa de falsos positivos
- `score_distributions.png` - Distribuições das métricas
- `3d_tradeoff.png` - Superfície 3D de trade-offs
- `parameter_sensitivity.png` - Efeito de parâmetros nas métricas

## 🎯 Melhores Resultados

### Configuração Ótima (F3 Weighted - Métrica Primária)

```
Detector: FLOSS
Parâmetros:
  - window_size: 25
  - regime_threshold: 0.85
  - regime_landmark: 3.0
  - min_gap_samples: 200
```

### Métricas de Performance

| Métrica | Valor | Desvio Padrão |
|---------|-------|---------------|
| **F3 Weighted*** | **0.3582** | 0.2276 |
| **F3 Classic** | **0.4205** | 0.2381 |
| F1 Weighted* | 0.2240 | 0.1893 |
| F1 Classic | 0.2658 | 0.2098 |
| **Recall@4s** | **0.4404** | 0.2957 |
| **Recall@10s** | **0.5921** | 0.3037 |
| Precision@4s | 0.1437 | 0.1600 |
| Precision@10s | 0.2098 | 0.2119 |
| **EDD Median** | **2.66s** | - |
| **FP/min** | **2.32** | - |

### NAB Scores

| Perfil | Score | Desvio Padrão |
|--------|-------|---------------|
| Standard | -3.11 | 6.11 |
| Low FP | -5.56 | 11.05 |
| Low FN | -4.85 | 7.43 |

## 🔍 Comparação com Outras Métricas

As diferentes métricas favorecem configurações ligeiramente diferentes:

| Métrica Objetivo | window_size | regime_threshold | regime_landmark | min_gap_samples | Score | Recall@10s | Precision@10s | FP/min | EDD(s) |
|------------------|-------------|------------------|-----------------|-----------------|-------|------------|---------------|--------|--------|
| **F3 Weighted*** | 25 | 0.85 | 3.0 | 200 | **0.3582** | 59.21% | 20.98% | 2.32 | 2.66 |
| F1 Weighted* | 25 | 0.80 | 3.5 | 200 | 0.2410 | 46.34% | 25.57% | 1.42 | 2.61 |
| F1 Classic | 25 | 0.80 | 5.0 | 200 | 0.2830 | 44.79% | 25.85% | 1.22 | 2.60 |
| F3 Classic | 25 | 0.90 | 2.5 | 200 | 0.4299 | 68.28% | 16.81% | 3.66 | 3.01 |
| NAB Standard | 25 | 0.80 | 3.0 | 200 | -3.07 | 50.61% | 24.39% | 1.67 | 2.73 |
| NAB Low FP | 25 | 0.80 | 4.5 | 200 | -4.31 | 43.35% | 25.11% | 1.26 | 2.76 |
| NAB Low FN | 25 | 0.90 | 3.0 | 200 | -4.63 | 65.84% | 17.72% | 3.22 | 2.80 |

**Observações importantes**:
- ✅ `window_size=25` é **consistentemente ótimo** em todas as métricas
- ✅ `min_gap_samples=200` (0.8s @ 250Hz) é **consistentemente ótimo** em todas as métricas
- ⚠️ `regime_threshold` varia entre **0.80-0.90** dependendo do trade-off recall/precision
- ⚠️ `regime_landmark` varia entre **2.5-5.0** dependendo da métrica
- 📊 Configurações com **maior recall** (F3 Classic, NAB Low FN) usam `regime_threshold=0.90`
- 📊 Configurações com **maior precision** (F1 Weighted, NAB Low FP) usam `regime_landmark` mais alto (≥3.5)

## 🔬 Análise Detalhada

### Características do FLOSS

O FLOSS é um detector de mudanças de regime baseado em:
- **Fast Low-rank Online Subspace Tracking**: Tracking de subespaços de baixa dimensão
- **Window-based**: Utiliza janelas deslizantes para análise local
- **Regime detection**: Identifica mudanças na estrutura do sinal

### Parâmetros do Detector

1. **`window_size`**: Tamanho da janela de análise (em amostras)
   - Valor ótimo: 25
   - Afeta a sensibilidade a mudanças locais

2. **`regime_threshold`**: Limiar para detecção de regime
   - Valor ótimo: 0.8 (F3*) ou 0.9 (NAB)
   - Controla sensibilidade vs especificidade

3. **`regime_landmark`**: Parâmetro de landmark para regime
   - Valor ótimo: 2.5 (F3*) ou 3.0 (NAB)
   - Afeta a robustez da detecção

4. **`min_gap_samples`**: Intervalo mínimo entre detecções (em amostras)
   - Valor ótimo: 200 (0.8s @ 250 Hz)
   - Evita detecções redundantes próximas

### Pontos Fortes

✅ **Latência muito baixa** (EDD median = 2.66s - detecção rápida)
✅ **Parâmetros estáveis** (window_size=25, min_gap=200 ótimos em todas as métricas)
✅ **Taxa moderada de falsos positivos** (2.32 FP/min - melhor que KSWIN com 9.43)
✅ **Melhor precision** (20.98% vs 10.74% do KSWIN)

### Pontos Fracos

⚠️ **Taxa de detecção moderada** (Recall@10s = 59.21% - perde ~41% dos eventos)
⚠️ **F-scores moderados** (F3* = 0.36, F1* = 0.22 - há margem para melhoria)
⚠️ **NAB scores negativos** (indicam que o detector não supera baseline simples)
⚠️ **Alta variabilidade** (σ = 0.23 para F3*, resultados inconsistentes entre ficheiros)

### Trade-offs Identificados

📊 **Sensibilidade vs Especificidade:**
- `regime_threshold=0.80` → Mais detecções, mais FP (precision ~25%, FP/min ~1.4)
- `regime_threshold=0.85` → Balanceado (precision ~21%, FP/min ~2.3) ← **Ótimo F3***
- `regime_threshold=0.90` → Menos FP, menos TP (precision ~17%, FP/min ~3.7)

📊 **Comparação com KSWIN:**
- **FLOSS**: Precision superior (21% vs 11%), menos FP (2.3 vs 9.4/min), mas recall inferior (59% vs 99%)
- **KSWIN**: Recall quase perfeito (99%), mas muitos FP e precision baixa (11%)
- **Recomendação**: KSWIN para aplicações clínicas (não pode perder eventos), FLOSS para alertas automáticos

## 📈 Como Reproduzir

### 1. Gerar Predições (R)

```r
# No ambiente R com pacote false.alarm
source("scripts/export_floss_predictions.R")
```

### 2. Avaliar Métricas (Python)

```bash
python -m src.evaluate_predictions \
  --predictions results/floss/predictions_intermediate.csv \
  --metrics-output results/floss/metrics_comprehensive_with_nab.csv \
  --report-output results/floss/final_report_with_nab.json
```

### 3. Gerar Visualizações (Python)

```bash
python -m src.visualize_results \
  --metrics results/floss/metrics_comprehensive_with_nab.csv \
  --output-dir results/floss/visualizations
```

## 🔗 Integração R-Python

Este detector foi implementado em R e integrado com o pipeline de avaliação Python seguindo a especificação documentada em `docs/predictions_csv_format_specification.md`.

### Formato CSV Mínimo Utilizado

```csv
record_id,detector,window_size,regime_threshold,regime_landmark,min_gap_samples,duration_seconds,gt_times,det_times,n_detections,n_ground_truth
```

**Colunas obrigatórias** (✅ presentes):
- `record_id`, `detector`, parâmetros específicos, `duration_seconds`
- `gt_times`, `det_times`, `n_detections`, `n_ground_truth`

**Colunas opcionais** (⚠️ omitidas):
- `duration_samples`, `processing_time`, `error`

**Colunas redundantes** (❌ omitidas corretamente):
- `gt_indices`, `det_indices` (calculadas automaticamente: `times * 250`)

## 📚 Documentação Relacionada

- **Métricas**: [`docs/evaluation_metrics_v1.md`](../../docs/evaluation_metrics_v1.md)
- **Visualizações**: [`docs/visualizations_guide.md`](../../docs/visualizations_guide.md)
- **Formato CSV**: [`docs/predictions_csv_format_specification.md`](../../docs/predictions_csv_format_specification.md)
- **Organização Geral**: [`results/README.md`](../README.md)

## 📝 Notas Técnicas

- **Dataset completo**: 229 ficheiros de ECG com regimes de fibrilação atrial
- **Grid search**: 4,320 combinações de parâmetros testadas (16 window_size × 18 regime_threshold × 15 regime_landmark × 1 min_gap)
- **Total de avaliações**: 989,280 (229 ficheiros × 4,320 configs)
- **Taxa de amostragem**: 250 Hz (constante)
- **Ground truth**: 1,301 eventos totais (média de 5.68 eventos por ficheiro)
- **Detecções totais**: 6,638 na config ótima (5.1× mais que ground truth)
- **Formato de integração**: CSV mínimo (R→Python), seguindo `docs/predictions_csv_format_specification.md`
- **Todas as métricas** calculadas em **segundos** (não em amostras)
- **Data de geração**: 17 novembro 2025

## 🔗 Comparações com Outros Detectores

Para comparações detalhadas com outros detectores, veja:
- [`results/comparisons/floss_vs_kswin.md`](../comparisons/floss_vs_kswin.md) - Comparação completa FLOSS vs KSWIN
- [`results/comparisons/floss_vs_kswin_radar.png`](../comparisons/floss_vs_kswin_radar.png) - Gráfico radar comparativo
- [`results/comparisons/detector_rankings.csv`](../comparisons/detector_rankings.csv) - Rankings de todos os detectores
