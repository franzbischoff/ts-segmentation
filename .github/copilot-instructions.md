Este repositório mantém um baseline de deteção de mudanças de regime em sinais de ECG streaming (250 Hz). A pipeline cobre preprocessamento (`ecg_preprocess.py`), geração de predições, avaliação temporal (F3-weighted/NAB) e visualizações estruturadas. **DDM/EDDM permanecem excluídos** (inadequados para séries temporais contínuas). Manter execução estritamente streaming (sem lookahead), dependências pinadas, modularidade e verificações rápidas antes de ampliar escopo.

## Estado Atual
- **Datasets completos**: `afib_paroxysmal` (229 ficheiros), `malignantventricular` (22) e `vtachyarrhythmias` (34). Cada dataset possui outputs para **6 detectores** (`adwin`, `page_hinkley`, `kswin`, `hddm_a`, `hddm_w`, `floss`) em `results/<dataset>/<detector>/` (CSV de predições, métricas, relatórios JSON/JSONL, sumários e `visualizations/` com 9 PNGs).
- **Comparações**: arquivos legados vivem em `results/comparisons/` (ex.: `floss_vs_kswin.*`), mas a ferramenta atual escreve em `comparisons/<dataset>/` (`comparative_report.md`, `detector_rankings.csv`, `detector_summary.csv`, `constraint_tradeoffs.csv`, `robustness.csv`). Use `python -m src.compare_detectors --dataset <dataset> --detectors ...` para atualizar esses artefactos.
- **Macro/micro averages**: `python -m src.cross_dataset_analysis --detector <detector> --output results/cross_dataset_analysis/<detector>/` calcula rankings robustos e README específicos (um por detector).
- **Scripts auxiliares**: `scripts/generate_*.sh`, `scripts/evaluate_*.sh` e `scripts/visualize_*.sh` já aceitam `--max-files/--max-samples` e encaminham argumentos adicionais.

## Pipeline Padronizado
1. **Predições** – `python -m src.generate_predictions --detector <nome> --data data/<dataset>_*.csv --output results/<dataset>/<detector>/predictions_intermediate.csv [--append ... --n-jobs -1]`
2. **Avaliação** – `python -m src.evaluate_predictions --predictions results/<dataset>/<detector>/predictions_intermediate.csv --metrics-output results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv --report-output results/<dataset>/<detector>/final_report_with_nab.json`
3. **Visualizações** – `python -m src.visualize_results --metrics results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv --output-dir results/<dataset>/<detector>/visualizations`
4. **Comparação** – `python -m src.compare_detectors --dataset <dataset> --detectors adwin page_hinkley kswin hddm_a hddm_w floss --output comparisons/<dataset>/comparative_report.md --csv-output comparisons/<dataset>/detector_rankings.csv`

Notas:
- `min_gap_samples` é filtro **aplicado pela pipeline** (não faz parte dos detectores).
- Guardar ficheiros grandes apenas em `data/` (já ignorado). Não versionar novos datasets volumosos.

## Documentação Essencial
- `README.md` (raiz): visão geral da pipeline e comandos principais.
- `results/<dataset>/<detector>/README.md`: resultados e melhores configurações por dataset/detector; preferir estes ficheiros em vez do README genérico.
- `docs/evaluation_metrics_v1.md`, `docs/visualizations_guide.md`, `docs/predictions_csv_format_specification.md`: métricas, interpretação das figuras e formato de CSVs.
- `results/cross_dataset_analysis/README.md` + READMEs específicos (um por detector) descrevem macro/micro averages e regras de robustez.

## Diretrizes Fixas
- Não criar novos ficheiros Markdown sem validação do utilizador; atualizar documentação existente relevante.
- Documentar qualquer novo parâmetro ou mudança operacional no README correspondente.
- Priorizar clareza/modularidade, manter scripts idempotentes e alinhados com o workflow streaming.
- Respeitar as dependências pinadas, evitar side-effects fora de `results/`/`data/`.
- Antes de executar o python, confirme se está no ambiente virtual correto (`source .venv/bin/activate`).

## Memória Persistente
Ler `.github/copilot-memory.md` sempre que o utilizador anunciar início do dia. Ao encerrar a sessão (quando solicitado), atualizar esse ficheiro com o estado mais recente.
