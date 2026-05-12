# Resultados do Detector HDDM-W

**Status**: ✅ COMPLETO (Novembro 2025)

Este diretório contém os resultados da análise do detector **HDDM-W** aplicado ao dataset de taquiarritmias ventriculares.

## 📊 Detector: HDDM-W

**Algoritmo**: HDDM-W (Hoeffding's Adaptive Tree Drift Detection Method - Weibull)
**Biblioteca**: scikit-multiflow
**Princípio**: Detecta mudanças usando distribuição Weibull para adaptação dinâmica

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
- [`comparisons/vtachyarrhythmias/comparative_report.md`](../../../../comparisons/vtachyarrhythmias/comparative_report.md)
- [`comparisons/vtachyarrhythmias/detector_rankings.csv`](../../../../comparisons/vtachyarrhythmias/detector_rankings.csv)

---

**Dataset**: vtachyarrhythmias (34 ficheiros, 97 eventos) | **Data**: Novembro 2025 | **Status**: Análise integrada na pipeline
