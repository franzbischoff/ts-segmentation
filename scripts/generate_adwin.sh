#!/bin/bash
# Script para gerar predições do detector ADWIN (Adaptive Windowing)
# Grid search completo com parâmetros de pré-processamento

set -e

echo "========================================="
echo "ADWIN Detector - Grid Search"
echo "========================================="
echo ""

DATA_PATH="data/afib_paroxysmal_full.csv"
if [ -n "$1" ]; then
    # Accept either dataset name (afib_paroxysmal_full) or full csv path
    if [[ "$1" == *.csv ]] || [[ "$1" == */* ]]; then
        DATA_PATH="$1"
        DATASET_NAME=$(basename "$DATA_PATH" .csv)
    else
        DATASET_NAME="$1"
        DATA_PATH="data/${DATASET_NAME}.csv"
    fi
else
    DATASET_NAME=$(basename "$DATA_PATH" .csv)
fi
DETECTOR="adwin"
# Use a 'clean' dataset name for output paths (strip suffixes like _full/_tidy)
CLEAN_NAME=$(echo "$DATASET_NAME" | sed -E 's/_full$//; s/_tidy.*$//')
OUTPUT_DIR="results/${CLEAN_NAME}/${DETECTOR}"
OUTPUT_PATH="${OUTPUT_DIR}/predictions_intermediate.csv"

if [ ! -f "$DATA_PATH" ]; then
    echo "Error: Data file not found: $DATA_PATH"
    exit 1
fi

echo "Data file: $DATA_PATH"
echo "Dataset name: $DATASET_NAME (clean: $CLEAN_NAME)"
echo "Output file: $OUTPUT_PATH"
echo ""

mkdir -p "${OUTPUT_DIR}"

# Extra args passed to script are forwarded to python (e.g., --max-files 1)
EXTRA_ARGS="${@:2}"

echo "Grid Search Configuration:"
echo "  delta: [0.005, 0.01, 0.02, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15]  (11 values)"
echo "  ma_window: [10, 30, 50, 100, 200, 300, 500, 750, 1000]  (9 values)"
echo "  min_gap: [1000, 2000, 3000, 4000, 5000]  (5 values)"
echo ""
echo "Total combinations: 11 × 9 × 5 = 495"
echo "Estimated time: ~45 minutes (229 files)"
echo ""

python -m src.generate_predictions \
    --detector adwin \
    --data "$DATA_PATH" \
    --output "$OUTPUT_PATH" \
    --n-jobs 20
    $EXTRA_ARGS
