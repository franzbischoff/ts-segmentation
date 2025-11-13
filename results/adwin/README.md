# Resultados do Detector ADWIN

Esta pasta contém todos os resultados da avaliação do detector **ADWIN** (Adaptive Windowing) no dataset afib_regimes.

## Detector: ADWIN

**Algoritmo**: ADWIN (Adaptive Windowing)
**Biblioteca**: scikit-multiflow
**Princípio**: Detecta mudanças monitorando média de janelas adaptativas

**Parâmetros principais**:
- `delta`: Threshold de confiança para detectar mudança (menor = mais sensível)
- `ma_window`: Janela de média móvel para pré-processamento
- `min_gap_samples`: Espaçamento mínimo entre detecções consecutivas

## Ficheiros Principais

### 1. Predições Brutas
- **`predictions_intermediate.csv`** (126 MB)
  - 113,355 linhas de predições individuais
  - Colunas: record_id, detector, delta, ma_window, min_gap_samples, detection_samples, detection_time_s, ground_truth_samples, ground_truth_time_s
  - Gerado por: `src/generate_predictions.py`

- **`predictions_intermediate_summary.json`**
  - Metadados da geração: total de ficheiros, combinações de parâmetros, timestamp

### 2. Métricas Agregadas
- **`metrics_comprehensive_with_nab.csv`** (33 MB)
  - 113,355 avaliações (uma por ficheiro × combinação de parâmetros)
  - Todas as métricas: F1/F3 classic/weighted, Recall@4s/10s, Precision@4s/10s, EDD, FP/min, NAB scores
  - Gerado por: `src/evaluate_predictions.py`

- **`metrics_comprehensive_with_nab_summary.json`**
  - Estatísticas agregadas das métricas

### 3. Relatório Final
- **`final_report_with_nab.json`** (12 KB)
  - Sumário executivo com melhores configurações
  - Top 10 rankings por métrica
  - Coverage do grid search
  - Gerado por: `src/evaluate_predictions.py`

### 4. Visualizações
- **`visualizations/`** (9 gráficos, 4.3 MB total)
  - `pr_scatter_plots.png` - Precision-Recall trade-offs
  - `pareto_front.png` - Soluções não-dominadas
  - `heatmap_*.png` - Sensibilidade de parâmetros
  - `score_distributions.png` - Distribuições de métricas
  - `3d_tradeoff.png` - Trade-off 3D
  - `parameter_sensitivity.png` - Análise de sensibilidade
  - Gerado por: `src/visualize_results.py`

## Melhores Configurações

### Métrica Primária: F3-weighted
```
delta: 0.005
ma_window: 300
min_gap_samples: 1000

Score: 0.3994 ± 0.2159
Recall@10s: 97.77%
Precision@10s: 10.20%
FP/min: 10.00
EDD median: 2.64s
```

### NAB Standard (comparação com benchmarks)
```
delta: 0.050
ma_window: 10
min_gap_samples: 2000

Score: -4.2820 ± 8.5400
Recall@10s: 74.01%
FP/min: 4.33
```

### NAB Low FN (aplicações críticas)
```
delta: 0.080
ma_window: 100
min_gap_samples: 2000

Score: -3.3841 ± 8.4849
Recall@10s: 91.19%
FP/min: 5.78
EDD median: 4.66s
```

### NAB Low FP (minimizar alarmes falsos)
```
delta: 0.005
ma_window: 10
min_gap_samples: 5000

Score: -7.0183 ± 6.9898
Recall@10s: 34.98%
FP/min: 1.53
```

## Grid Search Coverage

**Dataset**: 229 ficheiros (classe: paroxysmal_afib)
**Combinações de parâmetros**: 495
**Total de avaliações**: 113,355
**Eventos ground-truth**: 643,995
**Detecções totais**: 6,752,494

**Ranges de parâmetros**:
- `delta`: [0.005, 0.010, 0.015, 0.020, 0.030, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090, 0.100]
- `ma_window`: [10, 30, 50, 100, 200, 300, 500]
- `min_gap_samples`: [500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 7500, 10000]

## Reproduzir Resultados

### 1. Gerar Predições
```bash
python -m src.generate_predictions \
    --data data/afib_paroxysmal_tidy.csv \
    --detector adwin \
    --output results/adwin/predictions_intermediate.csv \
    --delta 0.005 0.01 0.015 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 \
    --ma-window 10 30 50 100 200 300 500 \
    --min-gap 500 1000 1500 2000 2500 3000 4000 5000 7500 10000
```

### 2. Avaliar Métricas
```bash
python -m src.evaluate_predictions \
    --predictions results/adwin/predictions_intermediate.csv \
    --metrics-output results/adwin/metrics_comprehensive_with_nab.csv \
    --report-output results/adwin/final_report_with_nab.json
```

### 3. Gerar Visualizações
```bash
python -m src.visualize_results \
    --metrics results/adwin/metrics_comprehensive_with_nab.csv \
    --output-dir results/adwin/visualizations
```

## Insights Principais

### Strengths do ADWIN
✅ Alta recall (97.77% @ 10s com configuração ótima)
✅ Detecção rápida (EDD median: 2.64s)
✅ Auto-adaptativo (não requer parâmetros de janela fixa)
✅ Robusto a diferentes configurações de ma_window

### Weaknesses do ADWIN
❌ Alta taxa de falsos positivos (10 FP/min na melhor F3)
❌ Sensível a mudanças graduais de baseline
❌ Performance varia significativamente entre pacientes (std alto)
❌ NAB scores negativos indicam penalização por FPs

### Recomendações
1. **Para recall máximo**: usar `delta=0.005, ma_window=300, min_gap=1000`
2. **Para balancear FP/FN**: usar `delta=0.08, ma_window=100, min_gap=2000`
3. **Para minimizar FP**: usar `delta=0.005, ma_window=10, min_gap=5000` (compromete recall)
4. **Para comparação justa**: reportar sempre NAB Standard score

## Próximos Passos

- [ ] Comparar com Page-Hinkley (`results/page_hinkley/`)
- [ ] Comparar com DDM (`results/ddm/`)
- [ ] Análise de ensemble (votação entre detectores)
- [ ] Análise de failure cases (ficheiros com pior performance)
- [ ] Validação cruzada por paciente

## Referências

- ADWIN: Bifet & Gavaldà (2007) "Learning from Time-Changing Data with Adaptive Windowing"
- NAB: Ahmad et al. (2017) "Unsupervised real-time anomaly detection for streaming data"
- Dataset: Moody & Mark (2001) "The impact of the MIT-BIH Arrhythmia Database"

---

**Última atualização**: 2025-11-13
**Versão**: 1.0
