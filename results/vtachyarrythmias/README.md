# Resultados - vtachyarrythmias

Esta pasta está reservada para resultados do dataset `vtachyarrythmias`.
Use os scripts em `scripts/` para gerar predições, métricas e visualizações com a estrutura padrão:

```
results/<dataset>/<detector>/predictions_intermediate.csv
results/<dataset>/<detector>/metrics_comprehensive_with_nab.csv
results/<dataset>/<detector>/final_report_with_nab.json
results/<dataset>/<detector>/visualizations/
```

Exemplo rápido para gerar resultados do detector ADWIN neste dataset:

```bash
# Rodar generate para este dataset
./scripts/generate_adwin.sh data/vtachyarrythmias_full.csv

# Avaliar predições
./scripts/evaluate_adwin.sh data/vtachyarrythmias_full.csv

# Gerar visualizações
./scripts/visualize_adwin.sh data/vtachyarrythmias_full.csv
```
