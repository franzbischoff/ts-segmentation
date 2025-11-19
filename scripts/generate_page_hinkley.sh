#!/bin/bash
# Script para gerar predições do detector Page-Hinkley
# Grid search inicial com conjunto reduzido de parâmetros

set -e

echo "========================================="
echo "Page-Hinkley Detector - Grid Search"
echo "========================================="
echo ""

# Define paths
DATA_PATH="data/afib_paroxysmal_full.csv"
if [ -n "$1" ]; then
    DATA_PATH="$1"
fi
DATASET_NAME=$(basename "$DATA_PATH" .csv | sed -E 's/_full$//; s/_tidy.*$//')
DETECTOR="page_hinkley"
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

echo "Grid Search Configuration (MODERADO):"
echo "  lambda_: [10, 30, 50, 80]  (4 values)"
echo "  delta: [0.005, 0.01, 0.02, 0.04]  (4 values)"
echo "  alpha: [0.9999, 0.99]  (2 values)"
echo "  ma_window: [10, 50, 200]  (3 values)"
echo "  min_gap: [500, 1000, 2000, 4000]  (4 values)"
echo ""
echo "Total combinations: 4 × 4 × 2 × 3 × 4 = 384"
echo "Estimated time: ~29 minutes (229 files)"
echo ""

read -p "Press Enter to start or Ctrl+C to cancel..."

# Run prediction generation
python -m src.generate_predictions \
    --detector page_hinkley \
    --data "$DATA_PATH" \
    --output "$OUTPUT_PATH" \
    --lambda 10 30 50 80 \
    --ph-delta 0.005 0.01 0.02 0.04 \
    --alpha 0.9999 0.99 \
    --ma-window 10 50 200 \
    --min-gap 500 1000 2000 4000 \
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
echo "3. Compare with ADWIN:"
echo "   python -m src.compare_detectors \\"
echo "       --detectors adwin page_hinkley \\"
echo "       --output results/comparisons/adwin_vs_page_hinkley.md"
