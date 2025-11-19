#!/bin/bash
# Script para gerar predições do detector HDDM_A (Hoeffding Drift Detection - Average)
# Grid search completo com parâmetros de confiança

set -e

echo "========================================="
echo "HDDM_A Detector - Grid Search"
echo "========================================="
echo ""

# Define paths
DATA_PATH="data/afib_paroxysmal_full.csv"
if [ -n "$1" ]; then
    ARG="$1"
    if [[ "$ARG" == *.csv ]] || [[ "$ARG" == */* ]]; then
        DATA_PATH="$ARG"
        DATASET_NAME=$(basename "$DATA_PATH" .csv)
    else
        DATASET_NAME="$ARG"
        DATA_PATH="data/${DATASET_NAME}.csv"
    fi
else
    DATASET_NAME=$(basename "$DATA_PATH" .csv)
fi
DETECTOR="hddm_a"
CLEAN_NAME=$(echo "$DATASET_NAME" | sed -E 's/_full$//; s/_tidy.*$//')
OUTPUT_DIR="results/${CLEAN_NAME}/${DETECTOR}"
OUTPUT_PATH="${OUTPUT_DIR}/predictions_intermediate.csv"

# Check if data file exists
if [ ! -f "$DATA_PATH" ]; then
    echo "Error: Data file not found: $DATA_PATH"
    exit 1
fi

echo "Data file: $DATA_PATH"
echo "Dataset name: $DATASET_NAME (clean: $CLEAN_NAME)"
echo "Output file: $OUTPUT_PATH"
echo ""

# Create output directory
mkdir -p "${OUTPUT_DIR}"

# Extra args (forward to python script: --max-files, --max-samples)
EXTRA_ARGS="${@:2}"

echo "Grid Search Configuration:"
echo "  drift_confidence: [0.0001, 0.0005, 0.001, 0.005]  (4 values)"
echo "  warning_confidence: [0.001, 0.005, 0.01, 0.05]  (4 values)"
echo "  two_side_option: [True, False]  (2 values - bi/unilateral test)"
echo "  ma_window: [1, 10, 50, 100]  (4 values - 1 = no smoothing)"
echo "  min_gap: [500, 1000, 2000, 3000, 5000]  (5 values)"
echo ""
echo "Total combinations: 4 × 4 × 2 × 4 × 5 = 640"
echo "Estimated time: ~60 minutes (229 files)"
echo ""
echo "Note: HDDM_A uses Hoeffding bounds for drift detection"
echo "      Based on average values"
echo ""

read -p "Press Enter to start or Ctrl+C to cancel..."

# Run prediction generation (use default grid - no custom params needed)
python -m src.generate_predictions \
    --detector hddm_a \
    --data "$DATA_PATH" \
    --output "$OUTPUT_PATH" \
    --n-jobs 20
    $EXTRA_ARGS

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
echo "3. Compare with HDDM_W:"
echo "   python -m src.compare_detectors \\"
echo "       --detectors hddm_a hddm_w \\"
echo "       --output results/comparisons/hddm_comparison.md"
