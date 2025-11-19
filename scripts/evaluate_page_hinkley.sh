#!/bin/bash
# Script para avaliar as métricas do detector Page-Hinkley
set -e

DATA_PATH="data/afib_paroxysmal_full.csv"
if [ -n "$1" ]; then
    DATA_PATH="$1"
fi
DATASET_NAME=$(basename "$DATA_PATH" .csv | sed -E 's/_full$//; s/_tidy.*$//')
DETECTOR="page_hinkley"
RESULTS_DIR="results/${DATASET_NAME}/${DETECTOR}"
PRED_PATH="${RESULTS_DIR}/predictions_intermediate.csv"
METRICS_PATH="${RESULTS_DIR}/metrics_comprehensive_with_nab.csv"
REPORT_PATH="${RESULTS_DIR}/final_report_with_nab.json"

if [ ! -f "$PRED_PATH" ]; then
    echo "Arquivo de predições não encontrado: $PRED_PATH"
    exit 1
fi

python -m src.evaluate_predictions \
    --predictions "$PRED_PATH" \
    --metrics-output "$METRICS_PATH" \
    --report-output "$REPORT_PATH"
