# Resultados de Detecção de Mudanças de Regime - ECG

Esta pasta contém os resultados organizados por detector para comparação sistemática de algoritmos de detecção de mudanças de regime (change point detection) em sinais de ECG streaming.

## Estrutura de Pastas

```
results/
├── adwin/                      # Resultados do detector ADWIN
│   ├── predictions_intermediate.csv
│   ├── metrics_comprehensive_with_nab.csv
│   ├── final_report_with_nab.json
│   ├── visualizations/
│   └── README.md
│
├── page_hinkley/              # Resultados do detector Page-Hinkley (a implementar)
│   └── README.md
│
├── ddm/                       # Resultados do detector DDM (a implementar)
│   └── README.md
│
├── comparisons/               # Comparações entre detectores
│   ├── comparative_report.md
│   ├── detector_rankings.csv
│   └── ensemble_results/
│
└── README.md                  # Este ficheiro
results/
├── afib_paroxysmal/            # Results for the `afib_paroxysmal` dataset (229 files)
│   ├── adwin/                   # Resultados do detector ADWIN
├── page_hinkley/              # Resultados do detector Page-Hinkley (a implementar)
  ├── page_hinkley/
  └── ...

├── malignantventricular/      # Results for `malignantventricular` dataset
│   ├── adwin/
│   └── ...

├── vtachyarrhythmias/          # Results for `vtachyarrhythmias` dataset
│   ├── adwin/
│   └── ...

├── page_hinkley/              # Resultados do detector Page-Hinkley (a implementar)
## Detectores Implementados
## Detectors and Dataset-aware Structure

Each dataset will have its own subfolder under `results/` to keep outputs
isolated and comparable. For example:

```
results/afib_paroxysmal/adwin/
results/malignantventricular/adwin/
results/vtachyarrhythmias/adwin/
```

This allows running the same pipeline for different datasets without
mixing predictions or metrics.
**Pasta**: `results/<dataset>/adwin/`
**Dataset**: afib_paroxysmal (229 ficheiros) — you may also run this on other datasets by passing a different path to the scripts.
    --data data/afib_paroxysmal_tidy.csv \
**Dataset**: afib_paroxysmal (229 ficheiros)
    --output results/<dataset>/<DETECTOR_NAME>/predictions_intermediate.csv \
python -m src.compare_detectors \
    --detectors <detector1> <detector2> <detector3> \
    --results-dir results/<dataset> \
    --output results/comparisons/<nome_comparacao>.md
**Recall@10s**: 97.77%
**FP/min**: 10.00

[Ver detalhes completos →](adwin/README.md)

### 🔄 Page-Hinkley
**Status**: A implementar
**Pasta**: `results/page_hinkley/`
**Princípio**: Teste sequencial de mudança de média
**Vantagens**: Rápido, baixa memória
**Parâmetros**: lambda, delta, alpha

<!-- DDM/EDDM removidos do pipeline: não são usados para detecção de mudanças em séries temporais contínuas. -->

### 🔄 HDDM (Hoeffding's Bound Drift Detection)
**Status**: Planejado
**Pasta**: `results/hddm/`
**Princípio**: Usa bound de Hoeffding
**Vantagens**: Garantias teóricas

### 🔄 KSWIN (Kolmogorov-Smirnov Windowing)
**Status**: Planejado
**Pasta**: `results/kswin/`
**Princípio**: Teste estatístico KS entre janelas
**Vantagens**: Não paramétrico, detecta qualquer tipo de mudança

## Pipeline de Avaliação

Cada detector segue o mesmo pipeline padronizado:

### 1️⃣ Geração de Predições
```bash
python -m src.generate_predictions \
    --data data/afib_paroxysmal_tidy.csv \
    --detector <DETECTOR_NAME> \
    --output results/<dataset>/<DETECTOR_NAME>/predictions_intermediate.csv \
    --delta <VALUES> \
    --ma-window <VALUES> \
    --min-gap <VALUES>
```

**Output**: `predictions_intermediate.csv` com todas as detecções brutas

> Nota: `min_gap_samples` é um filtro aplicado pela pipeline após as detecções serem
> geradas; não faz parte dos detectores subjacentes. O `predictions_intermediate.csv`
> contém as detecções "brutas" para cada combinação de parâmetros — o gap é depois
> usado para suprimir eventos redundantes durante a avaliação.

### 2️⃣ Avaliação de Métricas
```bash
python -m src.evaluate_predictions \
    --predictions results/<dataset>/<DETECTOR_NAME>/predictions_intermediate.csv \
    --metrics-output results/<dataset>/<DETECTOR_NAME>/metrics_comprehensive_with_nab.csv \
    --report-output results/<dataset>/<DETECTOR_NAME>/final_report_with_nab.json
```

**Output**:
- `metrics_comprehensive_with_nab.csv` - Métricas detalhadas
- `final_report_with_nab.json` - Sumário executivo

> Novo (robustez 2-fold): acrescente `--two-fold-analysis` para dividir os ficheiros do dataset
> em duas metades reprodutíveis e comparar a generalização dos melhores parâmetros entre elas.
> Opcionalmente ajuste `--two-fold-seed` (default 42), `--two-fold-primary-metric` (ex.: `nab_score_standard`)
> e `--two-fold-suffix` para personalizar o nome dos artefactos.
>
> Outputs extras gerados por este modo:
> - `results/<dataset>/fold_assignments_seed<seed>.json` – lista fixa dos ficheiros em cada metade
> - `results/<dataset>/<DETECTOR_NAME>/final_report_with_nab_twofold_seed<seed>.json` – resumo das métricas intra-fold e cruzadas

### 3️⃣ Visualizações
```bash
python -m src.visualize_results \
    --metrics results/<dataset>/<DETECTOR_NAME>/metrics_comprehensive_with_nab.csv \
    --output-dir results/<dataset>/<DETECTOR_NAME>/visualizations
```

**Output**: 9 gráficos PNG para análise visual

## Estrutura de Pastas

```
results/
├── <dataset>/                   # Results for each dataset (e.g. afib_paroxysmal)
│   ├── adwin/
│   ├── page_hinkley/
│   ├── kswin/
│   └── ...
├── comparisons/                 # Comparações entre detectors (aggregate across datasets)
└── README.md
fp_per_min,page_hinkley,adwin,kswin,hddm_w,...
```

### Ensemble Analysis
Combinar detectores via:
- Votação majoritária
- Weighted voting por confiança
- Cascata (detector rápido → detector preciso)

## Workflow para Adicionar Novo Detector

1. **Criar pasta dedicada**:
   ```bash
    mkdir -p results/<dataset>/<detector_name>
   ```

2. **Executar pipeline completo**:
   ```bash
   # Gerar predições
   python -m src.generate_predictions --detector <detector_name> \
    --output results/<dataset>/<detector_name>/predictions_intermediate.csv ...

   # Avaliar métricas
   python -m src.evaluate_predictions \
    --predictions results/<dataset>/<detector_name>/predictions_intermediate.csv \
    --metrics-output results/<dataset>/<detector_name>/metrics_comprehensive_with_nab.csv \
    --report-output results/<dataset>/<detector_name>/final_report_with_nab.json

   # Gerar visualizações
   python -m src.visualize_results \
    --metrics results/<dataset>/<detector_name>/metrics_comprehensive_with_nab.csv \
    --output-dir results/<dataset>/<detector_name>/visualizations
   ```

3. **Criar README específico** (template em `results/adwin/README.md`)

4. **Atualizar comparações**:
   ```bash
   python -m src.compare_detectors \
       --detectors adwin page_hinkley <detector_name> \
       --output results/comparisons/comparative_report.md
   ```

## Grid Search Padrão

Para comparação justa, usar o mesmo grid para todos os detectores:

```python
DELTA_VALUES = [0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
MA_WINDOW_VALUES = [10, 30, 50, 100, 200, 300, 500]
MIN_GAP_VALUES = [500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 7500, 10000]
```

**Total**: 12 × 7 × 10 = 840 combinações por detector

## Recursos Computacionais

### ADWIN (referência)
- Tempo geração predições: ~45 minutos (229 ficheiros × 495 combinações)
- Tempo avaliação: ~84 segundos (113,355 avaliações)
- Tempo visualizações: ~30 segundos
- **Total**: ~50 minutos por detector

### Estimativas para 5 detectores
- Tempo total: ~4 horas
- Espaço em disco: ~1 GB (predições + métricas + visualizações)
- RAM necessária: ~2 GB

## Análise Estatística

Para cada detector, calcular:

### Robustez
- Coeficiente de variação (CV) das métricas entre ficheiros
- Identificar outliers (ficheiros muito difíceis/fáceis)

### Estabilidade Paramétrica
- Sensibilidade a cada parâmetro (gradiente médio)
- Tamanho da região Pareto-ótima

### Generalização
- Performance em diferentes classes (paroxysmal vs persistent vs non-afib)
- Validação cruzada por paciente

## Formato de Ficheiros

### predictions_intermediate.csv
```csv
record_id,detector,delta,ma_window,min_gap_samples,detection_samples,detection_time_s,ground_truth_samples,ground_truth_time_s
data_101_1.par,adwin,0.005,300,1000,12500,50.0,12480,49.92
...
```

### metrics_comprehensive_with_nab.csv
```csv
record_id,detector,delta,ma_window,min_gap_samples,f1_classic,f1_weighted,f3_classic,f3_weighted,recall_4s,recall_10s,precision_4s,precision_10s,edd_median_s,fp_per_min,nab_score_standard,nab_score_low_fp,nab_score_low_fn,...
data_101_1.par,adwin,0.005,300,1000,0.1689,0.1603,0.4188,0.3994,0.7863,0.9777,0.0714,0.1020,2.64,10.00,-8.8409,-20.1729,-4.4326,...
...
```

### final_report_with_nab.json
```json
{
  "detector": "adwin",
  "dataset": "afib_paroxysmal",
  "evaluation_summary": {...},
  "best_parameters": {
    "f3_weighted": {...},
    "nab_standard": {...},
    ...
  },
  "top_10_f3_weighted": [...],
  "parameter_grid_coverage": {...}
}
```

## Citações

Ao usar estes resultados, citar:

**Dataset**:
```
Moody GB, Mark RG. The impact of the MIT-BIH Arrhythmia Database.
IEEE Eng in Med and Biol 20(3):45-50 (May-June 2001).
```

**NAB Benchmark**:
```
Ahmad S, Lavin A, Purdy S, Agha Z. Unsupervised real-time anomaly detection
for streaming data. Neurocomputing, 2017.
```

**ADWIN**:
```
Bifet A, Gavaldà R. Learning from time-changing data with adaptive windowing.
SIAM International Conference on Data Mining, 2007.
```

## Contato

Para dúvidas sobre a estrutura de resultados ou adicionar novos detectores, consultar:
- Documentação principal: `../README.md`
- Guia de métricas: `../docs/evaluation_metrics_v1.md`
- Guia de visualizações: `../docs/visualizations_guide.md`

---

**Última atualização**: 2025-11-13
**Versão**: 1.0
