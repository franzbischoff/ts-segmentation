#!/bin/bash
# Script para gerar predições do detector HDDM_W (Hoeffding Drift Detection - Weighted)
# Grid search completo com parâmetros de confiança e ponderação

set -e

echo "========================================="
echo "HDDM_W Detector - Grid Search"
echo "========================================="
echo ""

# Define paths
DATA_PATH="data/afib_paroxysmal_full.csv"
if [ -n "$1" ]; then
    DATA_PATH="$1"
fi
DATASET_NAME=$(basename "$DATA_PATH" .csv | sed -E 's/_full$//; s/_tidy.*$//')
DETECTOR="hddm_w"
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
echo "  drift_confidence: [0.0001, 0.0005, 0.001, 0.005]  (4 values)"
echo "  warning_confidence: [0.001, 0.005, 0.01, 0.05]  (4 values)"
echo "  lambda_option: [0.01, 0.05, 0.1, 0.2]  (4 values - weighting factor)"
echo "  two_side_option: [True, False]  (2 values - bi/unilateral test)"
echo "  ma_window: [1, 10, 50, 100]  (4 values - 1 = no smoothing)"
echo "  min_gap: [500, 1000, 2000, 3000, 5000]  (5 values)"
echo ""
echo "Total combinations: 4 × 4 × 4 × 2 × 4 × 5 = 2,560"
echo "Estimated time: ~180 minutes / 3 hours (229 files)"
echo ""
echo "Note: HDDM_W uses Hoeffding bounds with weighted moving average"
echo "      Better for non-stationary streams"
echo "      Second best F3 performance in validation (0.5342)"
echo ""

read -p "Press Enter to start or Ctrl+C to cancel..."

# Run prediction generation (use default grid - no custom params needed)
python -m src.generate_predictions \
    --detector hddm_w \
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
echo "3. Compare with other top detectors:"
echo "   python -m src.compare_detectors \\"
echo "       --detectors hddm_w kswin adwin page_hinkley hddm_a \\"
echo "       --output results/comparisons/top_detectors.md"
