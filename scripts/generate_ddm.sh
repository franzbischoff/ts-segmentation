#!/bin/bash
# Script para gerar predições do detector DDM (Drift Detection Method)
# Grid search completo com parâmetros de pré-processamento

set -e

echo "========================================="
echo "DDM Detector - Grid Search"
echo "========================================="
echo ""
echo "AVISO: O detector DDM NÃO é apropriado para sinais contínuos de ECG streaming."
echo "Ele foi projetado para dados binários (acertos/erros de classificação)."
echo "A execução irá converter o sinal em erros binários (z-score > 2.0), o que pode perder nuances importantes."
echo "Não recomendamos o uso de DDM para comparativos finais em ECG."
echo "Deseja realmente continuar? (s/N)"
read -r CONTINUE
if [[ ! "$CONTINUE" =~ ^[sS]$ ]]; then
    echo "Execução abortada pelo usuário."
    exit 1
fi

# Define paths
DATA_PATH="data/afib_paroxysmal_full.csv"
OUTPUT_PATH="results/ddm/predictions_intermediate.csv"

# Check if data file exists
if [ ! -f "$DATA_PATH" ]; then
    echo "Error: Data file not found: $DATA_PATH"
    exit 1
fi

echo "Data file: $DATA_PATH"
echo "Output file: $OUTPUT_PATH"
echo ""

# Create output directory
mkdir -p results/ddm

echo "Grid Search Configuration:"
echo "  ma_window: [10, 30, 50, 100, 200, 300]  (6 values)"
echo "  min_gap: [500, 1000, 1500, 2000, 3000, 4000, 5000]  (7 values)"
echo "  use_derivative: [True, False]  (2 values - via grid default)"
echo ""
echo "Total combinations: 6 × 7 × 2 = 84"
echo "Estimated time: ~15 minutes (229 files)"
echo ""
echo "Note: DDM uses binary error conversion (z-score > 2.0)"
echo "      No tunable detector parameters (uses internal defaults)"
echo ""

read -p "Press Enter to start or Ctrl+C to cancel..."

# Run prediction generation (use default grid - no custom params needed)
python -m src.generate_predictions \
    --detector ddm \
    --data "$DATA_PATH" \
    --output "$OUTPUT_PATH" \
    --n-jobs 20

echo ""
echo "========================================="
echo "Prediction generation completed!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Evaluate predictions:"
echo "   python -m src.evaluate_predictions \\"
echo "       --predictions $OUTPUT_PATH \\"
echo "       --metrics-output results/ddm/metrics_comprehensive_with_nab.csv \\"
echo "       --report-output results/ddm/final_report_with_nab.json"
echo ""
echo "2. Generate visualizations:"
echo "   python -m src.visualize_results \\"
echo "       --metrics results/ddm/metrics_comprehensive_with_nab.csv \\"
echo "       --output-dir results/ddm/visualizations"
echo ""
echo "3. Compare with other detectors:"
echo "   python -m src.compare_detectors \\"
echo "       --detectors ddm eddm adwin \\"
echo "       --output results/comparisons/ddm_comparison.md"
