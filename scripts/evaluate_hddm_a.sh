#!/bin/bash
# Script para avaliar as métricas do detector HDDM_A
set -e

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
RESULTS_DIR="results/${CLEAN_NAME}/${DETECTOR}"
if [ ! -d "$RESULTS_DIR" ]; then
    if [ -d "results/${DATASET_NAME}/${DETECTOR}" ]; then
        RESULTS_DIR="results/${DATASET_NAME}/${DETECTOR}"
        echo "Using legacy results directory (contains suffix): $RESULTS_DIR"
    fi
fi
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
    --report-output "$REPORT_PATH" \
    --two-fold-analysis \
    --two-fold-seed 42 \
    --two-fold-primary-metric f3_weighted \
    --two-fold-suffix _twofold
