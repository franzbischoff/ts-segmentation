# Resultados - vtachyarrhythmias

Esta pasta contém os resultados completos do dataset `vtachyarrhythmias` para os 6 detectores ativos.
Use os scripts em `scripts/` para regenerar predições, métricas e visualizações dos detectores Python. FLOSS é a exceção: a geração de predições é feita pela integração R/`false.alarm`, e neste repositório há scripts apenas para avaliação e visualização de FLOSS.

```
results/<dataset>/<detector>/predictions_intermediate.csv
results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv
results/<dataset>/<detector>/final_report_with_nab.json
results/<dataset>/<detector>/models_aggregated.csv
results/<dataset>/<detector>/visualizations/
results/<dataset>/<detector>/visualizations/metrics_aggregated.csv
```

Exemplo rápido para gerar resultados do detector ADWIN neste dataset:

```bash
# Rodar generate para este dataset
./scripts/generate_adwin.sh data/vtachyarrhythmias_full.csv

# Avaliar predições
./scripts/evaluate_adwin.sh data/vtachyarrhythmias_full.csv

# Gerar visualizações
./scripts/visualize_adwin.sh data/vtachyarrhythmias_full.csv
```
