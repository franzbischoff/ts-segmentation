#!/bin/bash
# Script para gerar predições do detector KSWIN (Kolmogorov-Smirnov Windowing)
# Grid search completo com parâmetros estatísticos

set -e

echo "========================================="
echo "KSWIN Detector - Grid Search"
echo "========================================="
echo ""

# Define paths
DATA_PATH="data/afib_paroxysmal_full.csv"
# Allow passing a custom data file as first argument
if [ -n "$1" ]; then
    DATA_PATH="$1"
fi

# Derive a short dataset name from the file (strip _full / _tidy suffixes)
DATASET_NAME=$(basename "$DATA_PATH" .csv | sed -E 's/_full$//; s/_tidy.*$//')
DETECTOR="kswin"

# Output paths are now dataset-aware: results/<dataset>/<detector>/...
OUTPUT_DIR="results/${DATASET_NAME}/${DETECTOR}"
OUTPUT_PATH="${OUTPUT_DIR}/predictions_intermediate.csv"

# Check if data file exists
if [ ! -f "$DATA_PATH" ]; then
    echo "Error: Data file not found: $DATA_PATH"
    exit 1
fi

echo "Data file: $DATA_PATH"
echo "Dataset name: $DATASET_NAME"
echo "Output file: $OUTPUT_PATH"
echo ""

# Create output directory
mkdir -p "${OUTPUT_DIR}"

echo "Grid Search Configuration:"
echo "  alpha: [0.001, 0.005, 0.01, 0.05]  (4 values - significance level)"
echo "  window_size: [50, 100, 200, 500]  (4 values - reference window)"
echo "  stat_size: [20, 30, 50, 100]  (4 values - statistical window)"
echo "  ma_window: [1, 10, 50, 100]  (4 values - 1 = no smoothing)"
echo "  min_gap: [500, 1000, 2000, 3000, 5000]  (5 values)"
echo ""
echo "Total combinations: 4 × 4 × 4 × 4 × 5 = 1,280"
echo "Estimated time: ~90 minutes (229 files)"
echo ""
echo "Note: KSWIN uses Kolmogorov-Smirnov statistical test"
echo "      Works with continuous values (no binary conversion)"
echo ""

read -p "Press Enter to start or Ctrl+C to cancel..."

# Run prediction generation (use default grid - no custom params needed)
python -m src.generate_predictions \
    --detector kswin \
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
echo "   python -m src.evaluate_predictions \\
    --predictions $OUTPUT_PATH \\
    --metrics-output ${OUTPUT_DIR}/metrics_comprehensive_with_nab.csv \\
    --report-output ${OUTPUT_DIR}/final_report_with_nab.json"
echo ""
echo "2. Generate visualizations:"
echo "   python -m src.visualize_results \\
    --metrics ${OUTPUT_DIR}/metrics_comprehensive_with_nab.csv \\
    --output-dir ${OUTPUT_DIR}/visualizations"
echo ""
echo "3. Compare with other detectors:"
echo "   python -m src.compare_detectors \\"
echo "       --detectors kswin adwin \\"
echo "       --output results/comparisons/kswin_comparison.md"
