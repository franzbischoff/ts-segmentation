# Resultados do Detector HDDM-W

**Status**: ✅ COMPLETO (Novembro 2025)

Este diretório contém os resultados da análise do detector **HDDM-W** aplicado ao dataset de arritmias ventriculares malignas.

## 📊 Detector: HDDM-W

**Algoritmo**: HDDM-W (Hoeffding Drift Detection Method - weighted moving average test)
**Biblioteca**: scikit-multiflow
**Princípio**: Detecta mudanças em streams usando limites de Hoeffding sobre uma média móvel ponderada

**Parâmetros principais**:
- `drift_confidence`: Nível de confiança para detecção de drift
- `warning_confidence`: Nível de confiança para aviso
- `lambda_option`: Fator de ponderação da média móvel
- `two_side_option`: Teste unilateral ou bilateral
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
- [`comparisons/malignantventricular/comparative_report.md`](../../../comparisons/malignantventricular/comparative_report.md)
- [`comparisons/malignantventricular/detector_rankings.csv`](../../../comparisons/malignantventricular/detector_rankings.csv)

---

**Dataset**: malignantventricular (22 ficheiros, 592 eventos) | **Data**: Novembro 2025 | **Status**: Análise integrada na pipeline
