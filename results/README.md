# Results

Esta pasta concentra os artefatos gerados pela pipeline de deteccao e avaliacao.

## Estrutura Atual

```text
results/
├── afib_paroxysmal/
│   └── <detector>/
├── malignantventricular/
│   └── <detector>/
├── vtachyarrhythmias/
│   └── <detector>/
├── cross_dataset_analysis/
├── comparisons/            # historico e visualizacoes comparativas legadas
└── README.md
```

Cada pasta results/<dataset>/<detector>/ contem tipicamente:

- predictions_intermediate.csv
- metrics_comprehensive_with_nab.csv
- final_report_with_nab.json
- visualizations/
- README.md

Observacao sobre snapshots Markdown:

- Ficheiros como `final_report_with_nab_<timestamp>.md` e `final_report_with_nab_twofold_seed42_<timestamp>.md` sao snapshots auxiliares gerados para preservar uma execucao especifica.
- Esses snapshots **nao** substituem os artefatos canonicos do diretorio.
- Para referencia atual do detector/dataset, use prioritariamente `README.md`, `final_report_with_nab.json`, `metrics_comprehensive_with_nab.csv` e, quando aplicavel, os CSVs/relatorios em `comparisons/<dataset>/`.

## Fluxo de Geracao

### Predicoes

```bash
python -m src.generate_predictions \
  --detector <detector> \
  --data data/<dataset>_full.csv \
  --output results/<dataset>/<detector>/predictions_intermediate.csv
```

Este comando aplica-se aos detectores Python (`adwin`, `page_hinkley`, `kswin`, `hddm_a`, `hddm_w`). FLOSS é gerado externamente pela integração R/`false.alarm` e depois avaliado pela mesma pipeline Python.

### Avaliacao

```bash
python -m src.evaluate_predictions \
  --predictions results/<dataset>/<detector>/predictions_intermediate.csv \
  --metrics-output results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv \
  --report-output results/<dataset>/<detector>/final_report_with_nab.json
```

### Visualizacoes

```bash
python -m src.visualize_results \
  --metrics results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv \
  --output-dir results/<dataset>/<detector>/visualizations
```

## Comparacoes entre Detectores

### Relatórios Comparativos (Ativo)
Os relatorios comparativos **ativos por dataset** sao escritos em:

- `comparisons/<dataset>/comparative_report.md`
- `comparisons/<dataset>/detector_rankings.csv`
- `comparisons/<dataset>/detector_summary.csv`
- `comparisons/<dataset>/constraint_tradeoffs.csv`
- `comparisons/<dataset>/robustness.csv`

**Geração**: `python -m src.compare_detectors --dataset <dataset> --detectors adwin page_hinkley kswin hddm_a hddm_w floss`

### Análise Cross-Dataset (Novo)
Para comparações **robustas entre detectores** (agregando múltiplos datasets):

- `results/cross_dataset_analysis/cross_dataset_generalization_option1.{csv,md}` — Option 1: performance ceiling
- `results/cross_dataset_analysis/parameter_portability_option2.{csv,md}` — Option 2: parameter transfer
- `results/cross_dataset_analysis/unified_robustness_option3.{csv,md}` — Option 3: robustness score
- `results/cross_dataset_analysis/option123_summary.png` — Visualização unificada

**Leitura**: Ver [`results/cross_dataset_analysis/README.md`](cross_dataset_analysis/README.md)

### Agregação de Métricas (Novo)
Para análise de parâmetros e SHAP (em R):

- `results/<dataset>/<detector>/models_aggregated.csv` — Métricas por modelo (18 ficheiros)

**Geração**: `python -m src.simplify_metrics_for_analysis --input results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv --output results/<dataset>/<detector>/models_aggregated.csv`

### Histórico
A pasta `results/comparisons/` contem visualizacoes comparativas legadas (ex: floss_vs_kswin.*).

## Fluxo de Geração Completo

### Modo 1: Geração Inicial (Do Zero)

Para detectores Python:

```bash
# 1. Gerar predições
python -m src.generate_predictions --detector <detector> --data data/<dataset>_full.csv --output results/<dataset>/<detector>/predictions_intermediate.csv

# 2. Avaliar métricas
python -m src.evaluate_predictions --predictions results/<dataset>/<detector>/predictions_intermediate.csv --metrics-output results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv --report-output results/<dataset>/<detector>/final_report_with_nab.json

# 3. Visualizar por detector
python -m src.visualize_results --metrics results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv --output-dir results/<dataset>/<detector>/visualizations
```

Para FLOSS, gerar primeiro `predictions_intermediate.csv` pela integração R/`false.alarm`; depois executar as etapas de avaliação e visualização Python.

### Modo 2: Incrementar Predições (Append Mode)
Aplicável aos detectores Python gerados por `src.generate_predictions`.

```bash
# Útil para grid search em paralelo ou incremental
python -m src.generate_predictions --detector <detector> --data data/<dataset>_full.csv --output results/<dataset>/<detector>/predictions_intermediate.csv --append --n-jobs -1

# Depois, reavalie métricas (mesmo comando da Etapa 2)
python -m src.evaluate_predictions --predictions results/<dataset>/<detector>/predictions_intermediate.csv --metrics-output results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv --report-output results/<dataset>/<detector>/final_report_with_nab.json
```

### Modo 3: Análises Cross-Dataset
```bash
# Opção 1: Performance ceiling
python -m src.aggregate_twofold_analysis

# Opção 2: Parameter portability
python -m src.test_parameter_portability

# Opção 3: Unified robustness
python -m src.unified_robustness_score

# Visualização unificada
python -m src.visualize_option123
```

### Modo 4: Agregação para SHAP
```bash
python -m src.simplify_metrics_for_analysis --input results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv --output results/<dataset>/<detector>/models_aggregated.csv --aggregation mean
```

## Notas de Consistencia

- DDM e EDDM nao fazem parte do pipeline ativo.
- min_gap_samples e aplicado como filtro de pos-processamento da pipeline.
- Manter execucao causal e idempotencia dos scripts.
- `--append` mode em generate_predictions permite incrementar grid search em paralelo.
