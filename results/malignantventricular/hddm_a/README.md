# Resultados do Detector HDDM-A

**Status**: ✅ COMPLETO (Novembro 2025)

Este diretório contém os resultados da análise do detector **HDDM-A** aplicado ao dataset de arritmias ventriculares malignas.

## 📊 Detector: HDDM-A

**Algoritmo**: HDDM-A (Hoeffding's Adaptive Tree Drift Detection Method - Adelson)
**Biblioteca**: scikit-multiflow
**Princípio**: Detecta mudanças de conceito monitorando estatísticas de árvores de Hoeffding adaptativas

**Parâmetros principais**:
- `delta`: Nível de confiança para detecção
- `lambda_`: Taxa de aprendizagem
- `ma_window`: Janela de média móvel (filtro da pipeline)
- `min_gap_samples`: Espaçamento mínimo entre detecções (filtro de pós-processamento)

## 📁 Ficheiros Principais

### Predições e Métricas
- **`predictions_intermediate.csv`** - Predições brutas
- **`metrics_comprehensive_with_nab.csv`** - Métricas detalhadas
- **`final_report_with_nab.json`** - Relatório consolidado

### Visualizações (PNG)
Disponíveis em `visualizations/` com análise de sensibilidade paramétrica

## 🔍 Análise Detalhada

Para análise quantitativa, consultar:
- [`comparisons/malignantventricular/comparative_report.md`](../../../../comparisons/malignantventricular/comparative_report.md)
- [`comparisons/malignantventricular/detector_rankings.csv`](../../../../comparisons/malignantventricular/detector_rankings.csv)

---

**Dataset**: malignantventricular (22 ficheiros, 592 eventos) | **Data**: Novembro 2025 | **Status**: Análise integrada na pipeline
