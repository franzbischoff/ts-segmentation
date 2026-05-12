# Cross-Dataset Analysis (Current Baseline)

Este diretorio concentra os artefatos ativos para comparacao robusta entre detectores em multiplos datasets.

## Objetivo

Avaliar robustez dos detectores em tres perspectivas complementares:
1. Option 1: ceiling de performance com tuning local
2. Option 2: portabilidade de parametros entre datasets
3. Option 3: score unificado de robustez

Importante:
- Este README e operacional. Ele descreve metodo, comandos e artefatos.
- Rankings numericos podem mudar quando a pipeline e reexecutada (ex.: correcao de formulas, novo grid, novos dados).

## Artefatos Ativos

### Option 1 (Ceiling Performance)
- `cross_dataset_generalization_option1.csv`
- `cross_dataset_generalization_option1.md`

### Option 2 (Parameter Portability)
- `parameter_portability_option2.csv`
- `parameter_portability_option2.md`

### Option 3 (Unified Robustness)
- `unified_robustness_option3.csv`
- `unified_robustness_option3.md`

### Visualizacao Integrada
- `option123_summary.png`

### Two-Fold Support
- `twofold_robustness_afib_paroxysmal.csv`
- `twofold_robustness_malignantventricular.csv`
- `twofold_robustness_vtachyarrhythmias.csv`
- `twofold_analysis_summary.md`
- `TWOFOLD_ROBUSTNESS_README.md`

## Execucao

Ativar ambiente virtual:

```bash
source .venv/bin/activate
```

Gerar Option 1:

```bash
python -m src.aggregate_twofold_analysis
```

Gerar Option 2:

```bash
python -m src.test_parameter_portability
```

Gerar Option 3:

```bash
python -m src.unified_robustness_score
```

Gerar visualizacao integrada:

```bash
python -m src.visualize_option123
```

## Como Interpretar (Sem Fixar Ranking)

- Option 1 responde: "qual o melhor teto de performance com tuning por dataset?"
- Option 2 responde: "quanto da performance se mantem ao transferir parametros?"
- Option 3 responde: "qual detector e mais robusto ao combinar consistencia intra e inter-dataset?"

Recomendacao para publicacao:
1. Regerar os 3 blocos no estado atual da formula.
2. Usar os CSVs resultantes como fonte canonica para tabelas/rankings.
3. Tratar os markdowns gerados como interpretacao da rodada atual.

## Arquivo Historico

Documentos potencialmente desatualizados (anteriores a revisoes de formula) foram movidos para:

- `archive_pre_formula_fix/AGGREGATION_METHODS_COMPARISON.md`
- `archive_pre_formula_fix/ANALYSIS_RANKING_DISCREPANCIES.md`
- `archive_pre_formula_fix/CROSS_DATASET_ANALYSIS_SUMMARY.md`
- `archive_pre_formula_fix/OPTION3_COMPLETION_SUMMARY.txt`

Esses ficheiros foram preservados para auditoria historica e revisao manual posterior.

## Estrutura Atual

```text
results/cross_dataset_analysis/
├── README.md
├── cross_dataset_generalization_option1.csv
├── cross_dataset_generalization_option1.md
├── parameter_portability_option2.csv
├── parameter_portability_option2.md
├── unified_robustness_option3.csv
├── unified_robustness_option3.md
├── option123_summary.png
├── twofold_analysis_summary.md
├── twofold_robustness_afib_paroxysmal.csv
├── twofold_robustness_malignantventricular.csv
├── twofold_robustness_vtachyarrhythmias.csv
├── TWOFOLD_ROBUSTNESS_README.md
├── archive_pre_formula_fix/
└── <detector>/
```
