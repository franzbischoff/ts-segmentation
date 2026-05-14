# Resultados do Detector ADWIN

Esta pasta contém todos os resultados da avaliação do detector **ADWIN** (Adaptive Windowing) no dataset afib_paroxysmal.

## Detector: ADWIN

**Algoritmo**: ADWIN (Adaptive Windowing)
**Biblioteca**: scikit-multiflow
**Princípio**: Detecta mudanças monitorando média de janelas adaptativas

**Parâmetros principais**:
- `delta`: Threshold de confiança para detectar mudança (menor = mais sensível)
- `ma_window`: Janela de média móvel para pré-processamento
- `min_gap_samples`: Espaçamento mínimo entre detecções consecutivas

> Nota: `min_gap_samples` é um filtro de pós-processamento aplicado pela pipeline
> (em `src/streaming_detector.py`), não um parâmetro do detector ADWIN. As detecções
> geradas por ADWIN são "brutas" e o `min_gap_samples` suprime detecções redundantes
> depois de serem emitidas.

> Organização atual: os resultados do detector são agora armazenados em
> `results/<dataset>/adwin/` — por exemplo, `results/afib_paroxysmal/adwin/`.
> Isto mantém os resultados separados por dataset quando você rodar a mesma
> pipeline para os outros conjuntos de dados.

## Ficheiros Principais

### 1. Predições Brutas
- **`predictions_intermediate.csv`** (195 MB)
  - 136,026 linhas de predições individuais
  - Colunas: record_id, detector, delta, ma_window, min_gap_samples, duration_samples, duration_seconds, gt_indices, gt_times, det_indices, det_times, n_detections, n_ground_truth, processing_time
  - Gerado por: `src/generate_predictions.py`

- **`predictions_intermediate_summary.json`**
  - Metadados da geração: total de ficheiros, combinações de parâmetros, timestamp

### 2. Métricas Agregadas
- **`metrics_comprehensive_with_nab.csv`** (39 MB)
  - 136,026 avaliações (uma por ficheiro × combinação de parâmetros)
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

Score: 0.4004 ± 0.2165
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

Score: -7.0183 ± 9.9636
Recall@10s: 35.29%
FP/min: 2.01
```

## Grid Search Coverage

**Dataset**: 229 ficheiros (classe: paroxysmal_afib)
**Combinações de parâmetros**: 594
**Total de avaliações**: 136,026
**Eventos ground-truth únicos por avaliação**: 1,301
**Soma de eventos ground-truth nas avaliações**: 772,794
**Detecções totais nas avaliações**: 10,967,500

**Ranges de parâmetros**:
- `delta`: [0.005, 0.010, 0.015, 0.020, 0.025, 0.030, 0.040, 0.050, 0.060, 0.080, 0.100]
- `ma_window`: [10, 25, 50, 75, 100, 150, 200, 250, 300]
- `min_gap_samples`: [500, 1000, 2000, 3000, 4000, 5000]

## Reproduzir Resultados

### 1. Gerar Predições
```bash
python -m src.generate_predictions \
    --data data/afib_paroxysmal_full.csv \
    --detector adwin \
    --output results/afib_paroxysmal/adwin/predictions_intermediate.csv \
    --delta 0.005 0.01 0.015 0.02 0.025 0.03 0.04 0.05 0.06 0.08 0.1 \
    --ma-window 10 25 50 75 100 150 200 250 300 \
    --min-gap 500 1000 2000 3000 4000 5000
```

### 2. Avaliar Métricas
```bash
python -m src.evaluate_predictions \
    --predictions results/afib_paroxysmal/adwin/predictions_intermediate.csv \
    --metrics-output results/afib_paroxysmal/adwin/metrics_comprehensive_with_nab.csv \
    --report-output results/afib_paroxysmal/adwin/final_report_with_nab.json
```

### 3. Gerar Visualizações
```bash
python -m src.visualize_results \
    --metrics results/afib_paroxysmal/adwin/metrics_comprehensive_with_nab.csv \
    --output-dir results/afib_paroxysmal/adwin/visualizations
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

## Estado de Execução

- ✅ Comparação com Page-Hinkley disponível em `comparisons/afib_paroxysmal/`
- ✅ Comparação com outros detectores concluída (adwin, page_hinkley, kswin, hddm_a, hddm_w, floss)
- ✅ Artefatos completos em `results/afib_paroxysmal/adwin/`
- ✅ Pronto para análises complementares (ensemble, failure cases e validação por paciente)

## Referências

- ADWIN: Bifet & Gavaldà (2007) "Learning from Time-Changing Data with Adaptive Windowing"
- NAB: Ahmad et al. (2017) "Unsupervised real-time anomaly detection for streaming data"
- Dataset: Moody & Mark (2001) "The impact of the MIT-BIH Arrhythmia Database"

## 📝 Notas Técnicas

- **Dataset**: 229 ficheiros paroxysmal afib (classe paroxysmal_afib)
- **Lead/Derivação**: Lead II (derivação II padrão para análise de ritmo cardíaco)
- **Grid search**: 594 combinações de parâmetros
- **Taxa de amostragem**: 250 Hz (constante)
- **Todas as métricas** calculadas em **segundos** (não em amostras)

---

**Última atualização**: 2026-05-14
**Versão**: 1.1
