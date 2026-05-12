# Time Series Regime Change Detection Baseline

Baseline de deteccao de mudancas de regime em sinais ECG streaming (250 Hz), com execucao estritamente causal (sem lookahead) e avaliacao temporal orientada a latencia.

## Escopo Atual

- Detectores ativos: adwin, page_hinkley, kswin, hddm_a, hddm_w, floss
- Detectores removidos do pipeline ativo: DDM e EDDM

### Sobre FLOSS

FLOSS (Fast Lowcost Online Semantic Segmentation) é implementado em R (projeto `false.alarm`) e integrado externamente na pipeline de avaliação. Para detalhes técnicos e resultados, consultar:
- [`results/afib_paroxysmal/floss/README.md`](results/afib_paroxysmal/floss/README.md) — Resultados e análise FLOSS
- [`results/cross_dataset_analysis/floss/`](results/cross_dataset_analysis/floss/) — Análise cross-dataset

### Pipeline Padrão
1. Geracao de predicoes por detector
2. Avaliacao de metricas (F1/F3 classico, F1/F3 ponderado, Recall/Precision temporais, EDD, FP/min, NAB)
3. Visualizacoes por detector
4. Comparacao entre detectores por dataset

## Estrutura de Pastas

```text
.
├── data/
├── src/
├── results/
│   ├── afib_paroxysmal/
│   ├── malignantventricular/
│   ├── vtachyarrhythmias/
│   ├── cross_dataset_analysis/
│   ├── comparisons/              # historico/visualizacoes legadas
│   └── README.md
├── comparisons/
│   ├── afib_paroxysmal/
│   ├── malignantventricular/
│   └── vtachyarrhythmias/
├── docs/
├── scripts/
└── README.md
```

## Pipeline Operacional

Ativar ambiente virtual antes de executar:

```bash
source .venv/bin/activate
```

### 1) Gerar Predicoes

```bash
python -m src.generate_predictions \
  --detector <nome_detector> \
  --data data/<dataset>_full.csv \
  --output results/<dataset>/<detector>/predictions_intermediate.csv \
  --n-jobs -1
```

### 2) Avaliar Predicoes

```bash
python -m src.evaluate_predictions \
  --predictions results/<dataset>/<detector>/predictions_intermediate.csv \
  --metrics-output results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv \
  --report-output results/<dataset>/<detector>/final_report_with_nab.json
```

### 3) Gerar Visualizacoes

```bash
python -m src.visualize_results \
  --metrics results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv \
  --output-dir results/<dataset>/<detector>/visualizations
```

### 4) Agregar Metricas para Analise (Opcional)

Para análise de importância de parâmetros ou ML externo em R:

```bash
python -m src.simplify_metrics_for_analysis \
  --input results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv \
  --output results/<dataset>/<detector>/models_aggregated.csv \
  --aggregation mean
```

Saída: `models_aggregated.csv` com 1 linha por combinação de parâmetros (agregado sobre todos os ficheiros).

### 5) Comparar Detectores (por dataset)

```bash
python -m src.compare_detectors \
  --dataset <dataset> \
  --detectors adwin page_hinkley kswin hddm_a hddm_w floss \
  --output comparisons/<dataset>/comparative_report.md \
  --csv-output comparisons/<dataset>/detector_rankings.csv
```

## Regras Importantes

- Streaming estrito: sem uso de amostras futuras.
- min_gap_samples e filtro de pos-processamento da pipeline; nao e parametro intrinseco dos detectores.
- Dependencias devem permanecer pinadas em requirements.txt.
- Datasets grandes devem permanecer apenas em data/.

## Onde Consultar Resultados

### Por Detector e Dataset

- **Predições**: `results/<dataset>/<detector>/predictions_intermediate.csv`
- **Métricas**: `results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv`
- **Relatório JSON**: `results/<dataset>/<detector>/final_report_with_nab.json`
- **Dados agregados** (para análise SHAP/ML): `results/<dataset>/<detector>/models_aggregated.csv`
- **Visualizações**: `results/<dataset>/<detector>/visualizations/` (9 PNGs)
- **Documentação**: `results/<dataset>/<detector>/README.md`

### Comparação Entre Detectores (por dataset)

- **Relatório comparativo**: `comparisons/<dataset>/comparative_report.md`
- **Ranking de detectores**: `comparisons/<dataset>/detector_rankings.csv`
- **Métricas agregadas**: `comparisons/<dataset>/detector_summary.csv`

### Análise Cross-Dataset (Macro-Averages)

- **Sumário geral**: `results/cross_dataset_analysis/README.md`
- **Por detector**: `results/cross_dataset_analysis/<detector>/README.md`

## Documentacao Tecnica

Referência rigorosa de métricas e formatos:

- [docs/evaluation_metrics.md](docs/evaluation_metrics.md) — Definições rigorosas de todas as métricas, fórmulas matemáticas
- [docs/visualizations_guide.md](docs/visualizations_guide.md) — Guia das visualizações de grid search
- [docs/predictions_csv_format_specification.md](docs/predictions_csv_format_specification.md) — Especificação de formato de CSVs (`predictions_intermediate.csv` e `models_aggregated.csv`)
