# Resultados do Detector FLOSS — Ventricular Tachyarrhythmias

**Status**: ✅ COMPLETO (22 novembro 2025)

Este diretório contém os resultados da análise do detector FLOSS (Fast Lowcost Online Semantic Segmentation) aplicado ao dataset de taquiarritmias ventriculares.

## 📊 Ficheiros Gerados

### Predições e Métricas
- **`predictions_intermediate.csv`** - Predições brutas para todas combinações de parâmetros
- **`metrics_comprehensive_with_nab.csv`** - Métricas detalhadas (F1/F3, NAB, temporais)
- **`final_report_with_nab.json`** - Relatório consolidado com melhores configurações
- **`final_report_with_nab_twofold_seed42.json`** - Análise two-fold cross-validation

### Estatísticas do Dataset
- **34 ficheiros únicos** de ECG
- **Eventos de regime**: 97 no total
- **Frequência de amostragem**: 250 Hz
- **Lead**: II (padrão para análise de ritmo)

### Visualizações (PNG)
- `visualizations/` — Gráficos de análise de sensibilidade paramétrica

## 🔍 Análise Detalhada

Para análise quantitativa detalhada e rankings comparativos, consultar os ficheiros canônicos:
- [`comparisons/vtachyarrhythmias/comparative_report.md`](../../../comparisons/vtachyarrhythmias/comparative_report.md)
- [`comparisons/vtachyarrhythmias/detector_rankings.csv`](../../../comparisons/vtachyarrhythmias/detector_rankings.csv)

## 📚 Ver Também

- **Resultados AFib Paroxysmal (referência)**: [`../../afib_paroxysmal/floss/README.md`](../../afib_paroxysmal/floss/README.md)
- **Análise Cross-Dataset**: [`../../cross_dataset_analysis/floss/`](../../cross_dataset_analysis/floss/)
- **Documentação de FLOSS**: [README principal — Sobre FLOSS](../../../README.md#sobre-floss)

---

**Implementação**: R (projeto `false.alarm`) | **Data**: 2025-11-22 | **Status**: Análise integrada na pipeline
