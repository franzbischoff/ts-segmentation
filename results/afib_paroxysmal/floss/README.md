# Resultados do Detector FLOSS

**Status**: ✅ COMPLETO (atualizado em 14 maio 2026)

Este diretório contém os resultados completos do detector FLOSS (Fast Lowcost Online Semantic Segmentation) aplicado ao dataset completo de regimes de fibrilação atrial.

## 📊 Ficheiros Gerados

### Predições e Métricas
- **`predictions_intermediate.csv`** (5,935,680 linhas) - Predições brutas para todas combinações de parâmetros
- **`metrics_comprehensive_with_nab.csv`** (5,935,680 linhas) - Métricas detalhadas (F1/F3, NAB, temporais)
- **`final_report_with_nab.json`** (~16 KB) - Relatório consolidado com melhores configurações
- **`metrics_comprehensive_with_nab_summary.json`** (~4 KB) - Estatísticas agregadas

### Estatísticas do Dataset
- **229 ficheiros únicos** de ECG
- **25,920 combinações de parâmetros** testadas
- **5,935,680 avaliações totais** (229 × 25,920)
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
  - window_size: 75
  - regime_threshold: 0.70
  - regime_landmark: 4.0
  - min_gap_samples: 1000
```

### Métricas de Performance

| Métrica | Valor | Desvio Padrão |
|---------|-------|---------------|
| **F3 Weighted*** | **0.4798** | 0.2280 |
| **F3 Classic** | **0.5242** | 0.2378 |
| F1 Weighted* | 0.3471 | 0.2115 |
| F1 Classic | 0.3754 | 0.2227 |
| **Recall@4s** | **0.4958** | 0.2884 |
| **Recall@10s** | **0.6499** | 0.2749 |
| Precision@4s | 0.2264 | 0.1965 |
| Precision@10s | 0.3169 | 0.2386 |
| **EDD Median** | **3.28s** | - |
| **FP/min** | **1.42** | - |

### NAB Scores da configuração F3*

| Perfil | Score | Desvio Padrão |
|--------|-------|---------------|
| Standard | -1.6124 | 4.9029 |
| Low FP | -3.1104 | 7.6493 |
| Low FN | -3.5926 | 7.5980 |

## 🔍 Comparação com Outras Métricas

As diferentes métricas favorecem configurações ligeiramente diferentes:

| Métrica Objetivo | window_size | regime_threshold | regime_landmark | min_gap_samples | Score | Recall@10s | Precision@10s | FP/min | EDD(s) |
|------------------|-------------|------------------|-----------------|-----------------|-------|------------|---------------|--------|--------|
| **F3 Weighted*** | 75 | 0.70 | 4.0 | 1000 | **0.4798** | 64.99% | 31.69% | 1.42 | 3.28 |
| F1 Weighted* | 125 | 0.55 | 5.0 | 1000 | 0.3857 | 55.97% | 42.17% | 0.77 | 3.75 |
| F1 Classic | 75 | 0.65 | 8.5 | 2000 | 0.4601 | 59.02% | 45.57% | 0.63 | 6.34 |
| F3 Classic | 75 | 0.70 | 7.5 | 500 | 0.5786 | 69.09% | 39.27% | 1.12 | 5.22 |
| NAB Standard | 50 | 0.75 | 4.5 | 1000 | -1.4142 | 66.75% | 33.30% | 1.32 | 3.80 |
| NAB Low FP | 75 | 0.70 | 7.5 | 2000 | -2.4230 | 64.27% | 41.30% | 0.87 | 5.41 |
| NAB Low FN | 50 | 0.80 | 3.5 | 500 | -3.0548 | 72.03% | 24.85% | 2.25 | 3.09 |

**Observações importantes**:
- ✅ `window_size=75` domina as métricas F3 no dataset completo atualizado
- ✅ `min_gap_samples` entre 500 e 2000 controla o trade-off recall × falsos positivos; o ótimo F3* usa 1000
- ⚠️ `regime_threshold` varia entre **0.55-0.80** dependendo do trade-off recall/precision
- ⚠️ `regime_landmark` varia entre **3.5-8.5** dependendo da métrica
- 📊 Configurações com **maior recall** usam `regime_threshold=0.80` e `min_gap_samples=500`
- 📊 Configurações com **maior precision** usam landmarks mais altos (até 8.5) e gaps maiores

## 🔬 Análise Detalhada

### Características do FLOSS

O FLOSS é um detector de mudanças de regime baseado em:
- **Fast Lowcost Online Semantic Segmentation**: Segmentação semântica de baixa complexidade computacional
- **Window-based**: Utiliza janelas deslizantes para análise local
- **Regime detection**: Identifica mudanças na estrutura do sinal

### Parâmetros do Detector

1. **`window_size`**: Tamanho da janela de análise (em amostras)
   - Valor ótimo F3*: 75
   - Afeta a sensibilidade a mudanças locais

2. **`regime_threshold`**: Limiar para detecção de regime
   - Valor ótimo F3*: 0.70
   - Controla sensibilidade vs especificidade

3. **`regime_landmark`**: Parâmetro de landmark para regime
   - Valor ótimo F3*: 4.0
   - Afeta a robustez da detecção

4. **`min_gap_samples`**: Intervalo mínimo entre detecções (em amostras)
   - Valor ótimo F3*: 1000 (4.0s @ 250 Hz)

> Nota: `min_gap_samples` é um filtro aplicado pela pipeline (veja `src/streaming_detector.py`)
> e não um parâmetro intrínseco do algoritmo FLOSS. O script que gera as predições cria
> as detecções brutas, e o `min_gap_samples` é usado para suprimir detecções muito
> próximas durante a avaliação/relatório.
   - Evita detecções redundantes próximas

### Pontos Fortes

✅ **Latência baixa** (EDD median = 3.28s na melhor F3*)
✅ **Melhor F3* no dataset afib_paroxysmal** entre os detectores avaliados
✅ **Taxa moderada de falsos positivos** (1.42 FP/min - melhor que KSWIN com 9.43)
✅ **Melhor precision** (31.69% vs 10.74% do KSWIN)

### Pontos Fracos

⚠️ **Taxa de detecção moderada** (Recall@10s = 64.99% - perde ~35% dos eventos)
⚠️ **F1* ainda moderado** (0.3471 - há margem para melhoria em precisão/recall simultâneos)
⚠️ **NAB scores negativos** (indicam que o detector não supera baseline simples)
⚠️ **Alta variabilidade** (σ = 0.23 para F3*, resultados inconsistentes entre ficheiros)

### Trade-offs Identificados

📊 **Sensibilidade vs Especificidade:**
- `regime_threshold=0.55` → Favorece F1 weighted, com precision mais alta e menos FP
- `regime_threshold=0.70` → Balanceado para F3* no dataset completo atualizado
- `regime_threshold=0.80` → Favorece recall/NAB Low FN, com mais detecções e FP

📊 **Comparação com KSWIN:**
- **FLOSS**: Precision superior (31.69% vs 10.74%), menos FP (1.42 vs 9.43/min), mas recall inferior (64.99% vs 99.44%)
- **KSWIN**: Recall quase perfeito (99.44%), mas muitos FP e precision baixa (10.74%)
- **Recomendação**: KSWIN quando o critério dominante é recall; FLOSS quando o objetivo é melhor equilíbrio F3*/FP

## 📈 Como Reproduzir

### 1. Gerar Predições (R)

As predições FLOSS são geradas pela integração R/`false.alarm` e exportadas no formato CSV mínimo descrito abaixo. Não há script `generate_floss.sh` ou `scripts/export_floss_predictions.R` versionado neste repositório; para reproduzir, exportar o CSV para `results/afib_paroxysmal/floss/predictions_intermediate.csv` com as colunas especificadas.

### 2. Avaliar Métricas (Python)

```bash
python -m src.evaluate_predictions \
  --predictions results/afib_paroxysmal/floss/predictions_intermediate.csv \
  --metrics-output results/afib_paroxysmal/floss/metrics_comprehensive_with_nab.csv \
  --report-output results/afib_paroxysmal/floss/final_report_with_nab.json
```

### 3. Gerar Visualizações (Python)

```bash
python -m src.visualize_results \
  --metrics results/afib_paroxysmal/floss/metrics_comprehensive_with_nab.csv \
  --output-dir results/afib_paroxysmal/floss/visualizations
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

- **Métricas**: [`docs/evaluation_metrics.md`](../../../docs/evaluation_metrics.md)
- **Visualizações**: [`docs/visualizations_guide.md`](../../../docs/visualizations_guide.md)
- **Formato CSV**: [`docs/predictions_csv_format_specification.md`](../../../docs/predictions_csv_format_specification.md)
- **Organização Geral**: [`results/README.md`](../../README.md)

## 📝 Notas Técnicas

- **Dataset completo**: 229 ficheiros de ECG com regimes de fibrilação atrial (classe paroxysmal_afib)
- **Lead/Derivação**: Lead II (derivação II padrão para análise de ritmo cardíaco)
- **Grid search**: 25,920 combinações de parâmetros testadas (16 window_size × 18 regime_threshold × 15 regime_landmark × 6 min_gap)
- **Total de avaliações**: 5,935,680 (229 ficheiros × 25,920 configs)
- **Taxa de amostragem**: 250 Hz (constante)
- **Ground truth**: 1,301 eventos totais (média de 5.68 eventos por ficheiro)
- **Detecções totais**: 4,244 na config ótima F3* (3.3× mais que ground truth)
- **Formato de integração**: CSV mínimo (R→Python), seguindo `docs/predictions_csv_format_specification.md`
- **Todas as métricas** calculadas em **segundos** (não em amostras)
- **Data de geração dos artefatos atuais**: 12 maio 2026

## 🔗 Comparações com Outros Detectores

Para comparações detalhadas com outros detectores, veja:
- [`tmp/results_comparisons_legacy/floss_vs_kswin.md`](../../../tmp/results_comparisons_legacy/floss_vs_kswin.md) - Comparação histórica FLOSS vs KSWIN (arquivo local, não versionado)
- [`tmp/results_comparisons_legacy/floss_vs_kswin_radar.png`](../../../tmp/results_comparisons_legacy/floss_vs_kswin_radar.png) - Gráfico radar histórico (arquivo local, não versionado)
- [`comparisons/afib_paroxysmal/detector_rankings.csv`](../../../comparisons/afib_paroxysmal/detector_rankings.csv) - Rankings canônicos atuais por dataset
