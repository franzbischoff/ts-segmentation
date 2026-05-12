# Scripts

Scripts auxiliares para execucao da pipeline por detector.

## Scripts Disponiveis

### Geracao de Predicoes

- generate_adwin.sh
- generate_page_hinkley.sh
- generate_kswin.sh
- generate_hddm_a.sh
- generate_hddm_w.sh

Observacao: nao ha generate_floss.sh neste diretorio. Para FLOSS, usar chamada direta do modulo Python.

### Avaliacao

- evaluate_adwin.sh
- evaluate_page_hinkley.sh
- evaluate_kswin.sh
- evaluate_hddm_a.sh
- evaluate_hddm_w.sh
- evaluate_floss.sh

### Visualizacao

- visualize_adwin.sh
- visualize_page_hinkley.sh
- visualize_kswin.sh
- visualize_hddm_a.sh
- visualize_hddm_w.sh
- visualize_floss.sh

## Uso Recomendado

Ativar o ambiente virtual antes de executar qualquer script:

```bash
source .venv/bin/activate
```

Exemplo de fluxo para um detector:

```bash
./scripts/generate_adwin.sh
./scripts/evaluate_adwin.sh
./scripts/visualize_adwin.sh
```

## Comparacao Entre Detectores

Para comparacoes por dataset, usar o modulo Python (saida em comparisons/<dataset>/):

```bash
python -m src.compare_detectors \
  --dataset <dataset> \
  --detectors adwin page_hinkley kswin hddm_a hddm_w floss \
  --output comparisons/<dataset>/comparative_report.md \
  --csv-output comparisons/<dataset>/detector_rankings.csv
```

## Notas

- min_gap_samples e um filtro de pos-processamento da pipeline (nao e parametro intrinseco dos detectores).
- DDM e EDDM estao excluidos do fluxo ativo para series temporais continuas.
