# Dataset Comparisons: `vtachyarrhythmias`

**Last Updated:** 2025-12-15 16:24:41 (✅ SUCCESS)


**Dataset**: Ventricular Tachyarrhythmias
**Ficheiros**: 34
**Eventos de Regime**: 97
**Samples Totais**: 4.3M @ 250 Hz
**Lead**: II

---

## 📊 Resumo Executivo

### Status
- ✅ Dados processados
- ✅ 6 detectores avaliados
- ✅ Relatórios `.md` e `.csv` disponíveis em `./`
- 🔜 Visualizações a ser geradas (Fase 2)

### Top Detectors (por F3-Weighted)

| Rank | Detector | F3-Weighted | Recall@10s | FP/min |
|------|----------|---|---|---|
| 1 | FLOSS | TBD | TBD | TBD |
| 2 | KSWIN | TBD | TBD | TBD |
| 3 | Page-Hinkley | TBD | TBD | TBD |

---

## 📁 Ficheiros Disponíveis

### Relatórios Gerados
- **`comparative_report.md`** - Análise detalhada
- **`detector_rankings.csv`** - Rankings
- **`detector_summary.csv`** - Melhores configs
- **`constraint_tradeoffs.csv`** - Trade-offs
- **`robustness.csv`** - Robustez

### Visualizações (Fase 2)
- `visualizations/radar_6detectors.png`
- `visualizations/f3_vs_fp_scatter.png`
- `visualizations/heatmap_metrics_comparison.png`
- `visualizations/parameter_tradeoffs.png`

---

## 📈 Análise Detalhada

Para informações detalhadas, ver:
- **Relatório Completo**: [`./comparative_report.md`](./comparative_report.md)
- **Rankings**: [`./detector_rankings.csv`](./detector_rankings.csv)
- **Comparação Cross-Dataset**: [`../cross_dataset/`](../cross_dataset/)

---

## 🎯 Recomendações

Vendo números atualizados em `comparative_report.md` + `detector_summary.csv`

---

**Última Atualização**: 2025-12-15
**Status**: Estrutura pronta; dados a ser preenchidos com execução de `compare_detectors.py`
