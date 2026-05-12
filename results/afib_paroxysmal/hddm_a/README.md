# Resultados do Detector HDDM-A

**Status**: ✅ COMPLETO (Novembro 2025)

Este diretório contém os resultados da análise do detector **HDDM-A** (Hoeffding's Adaptive Tree Drift Detection Method - Adelson) aplicado ao dataset de fibrilação atrial paroxística.

## 📊 Detector: HDDM-A

**Algoritmo**: HDDM-A (Hoeffding's Adaptive Tree Drift Detection Method - Adelson)
**Biblioteca**: scikit-multiflow
**Princípio**: Detecta mudanças de conceito em streams monitorando estatísticas de árvores de Hoeffding adaptativas

**Parâmetros principais**:
- `delta`: Nível de confiança para detecção (menor = mais sensível)
- `lambda_`: Taxa de aprendizagem (forgetting factor)
- `ma_window`: Janela de média móvel para pré-processamento (filtro da pipeline)
- `min_gap_samples`: Espaçamento mínimo entre detecções (filtro de pós-processamento)

> Nota: `min_gap_samples` é um filtro de pós-processamento aplicado pela pipeline
> (em `src/streaming_detector.py`), não um parâmetro do detector. As detecções
> brutas são processadas e detecções redundantes são suprimidas.

## 📁 Ficheiros Principais

### Predições e Métricas
- **`predictions_intermediate.csv`** - Predições brutas para todas combinações de parâmetros
- **`metrics_comprehensive_with_nab.csv`** - Métricas detalhadas (F1/F3, NAB, temporais)
- **`metrics_comprehensive_with_nab.jsonl`** - Formato alternativo JSONL
- **`final_report_with_nab.json`** - Relatório consolidado com melhores configurações
- **`final_report_with_nab_twofold_seed42.json`** - Análise two-fold cross-validation
- **`metrics_aggregated.csv`** - Agregação de métricas por parâmetro

### Visualizações (PNG)
- `visualizations/pr_scatter_plots.png` - Gráficos de dispersão Precision-Recall
- `visualizations/pareto_front.png` - Frente de Pareto
- `visualizations/heatmap_f3-weighted.png` - Sensibilidade de parâmetros para F3*
- `visualizations/heatmap_nab-score-standard.png` - Sensibilidade para NAB
- `visualizations/heatmap_recall-10s.png` - Sensibilidade para Recall@10s
- `visualizations/heatmap_fp-per-min.png` - Sensibilidade para falsos alarmes
- `visualizations/score_distributions.png` - Distribuições de métricas
- `visualizations/3d_tradeoff.png` - Superfície 3D de trade-offs
- `visualizations/parameter_sensitivity.png` - Efeito de parâmetros

## 🔍 Análise Detalhada

Para análise quantitativa detalhada e rankings comparativos, consultar:
- [`comparisons/afib_paroxysmal/comparative_report.md`](../../../../comparisons/afib_paroxysmal/comparative_report.md)
- [`comparisons/afib_paroxysmal/detector_rankings.csv`](../../../../comparisons/afib_paroxysmal/detector_rankings.csv)

## 📚 Ver Também

- **Comparação entre detectores**: [`comparisons/afib_paroxysmal/`](../../../../comparisons/afib_paroxysmal/)
- **Análise cross-dataset**: [`../../cross_dataset_analysis/hddm_a/`](../../cross_dataset_analysis/hddm_a/)
- **Documentação de métricas**: [`docs/evaluation_metrics_v1.md`](../../../../docs/evaluation_metrics_v1.md)

---

**Dataset**: afib_paroxysmal (229 ficheiros, 1,301 eventos) | **Data**: Novembro 2025 | **Status**: Análise completa integrada na pipeline
