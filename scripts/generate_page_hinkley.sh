#!/bin/bash
# Script para gerar predições do detector Page-Hinkley
# Grid search inicial com conjunto reduzido de parâmetros

set -e

echo "========================================="
echo "Page-Hinkley Detector - Grid Search"
echo "========================================="
echo ""

# Define paths
DATA_PATH="data/afib_paroxysmal_tidy.csv"
OUTPUT_PATH="results/page_hinkley/predictions_intermediate.csv"

# Check if data file exists
if [ ! -f "$DATA_PATH" ]; then
    echo "Error: Data file not found: $DATA_PATH"
    exit 1
fi

echo "Data file: $DATA_PATH"
echo "Output file: $OUTPUT_PATH"
echo ""

# Create output directory
mkdir -p results/page_hinkley

echo "Grid Search Configuration:"
echo "  lambda_: [20, 30, 40, 50, 60, 80]  (6 values)"
echo "  delta: [0.005, 0.01, 0.02, 0.03]  (4 values)"
echo "  alpha: [0.9999, 0.999, 0.99]  (3 values)"
echo "  ma_window: [10, 30, 50, 100, 200, 300]  (6 values)"
echo "  min_gap: [500, 1000, 1500, 2000, 3000, 4000, 5000]  (7 values)"
echo ""
echo "Total combinations: 6 × 4 × 3 × 6 × 7 = 3,024"
echo "Estimated time: ~2-3 hours (229 files)"
echo ""

read -p "Press Enter to start or Ctrl+C to cancel..."

# Run prediction generation
python -m src.generate_predictions \
    --detector page_hinkley \
    --data "$DATA_PATH" \
    --output "$OUTPUT_PATH" \
    --lambda 20 30 40 50 60 80 \
    --ph-delta 0.005 0.01 0.02 0.03 \
    --alpha 0.9999 0.999 0.99 \
    --ma-window 10 30 50 100 200 300 \
    --min-gap 500 1000 1500 2000 3000 4000 5000 \
    --n-jobs -1

echo ""
echo "========================================="
echo "Prediction generation completed!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Evaluate predictions:"
echo "   python -m src.evaluate_predictions \\"
echo "       --predictions $OUTPUT_PATH \\"
echo "       --metrics-output results/page_hinkley/metrics_comprehensive_with_nab.csv \\"
echo "       --report-output results/page_hinkley/final_report_with_nab.json"
echo ""
echo "2. Generate visualizations:"
echo "   python -m src.visualize_results \\"
echo "       --metrics results/page_hinkley/metrics_comprehensive_with_nab.csv \\"
echo "       --output-dir results/page_hinkley/visualizations"
echo ""
echo "3. Compare with ADWIN:"
echo "   python -m src.compare_detectors \\"
echo "       --detectors adwin page_hinkley \\"
echo "       --output results/comparisons/adwin_vs_page_hinkley.md"
