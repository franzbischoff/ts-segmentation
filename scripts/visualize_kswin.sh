#!/bin/bash
# Script para gerar visualizações dos resultados do detector KSWIN
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
DETECTOR="kswin"
CLEAN_NAME=$(echo "$DATASET_NAME" | sed -E 's/_full$//; s/_tidy.*$//')
RESULTS_DIR="results/${CLEAN_NAME}/${DETECTOR}"
if [ ! -d "$RESULTS_DIR" ]; then
    if [ -d "results/${DATASET_NAME}/${DETECTOR}" ]; then
        RESULTS_DIR="results/${DATASET_NAME}/${DETECTOR}"
        echo "Using legacy results directory (contains suffix): $RESULTS_DIR"
    fi
fi
METRICS_PATH="${RESULTS_DIR}/metrics_comprehensive_with_nab.csv"
OUTDIR="${RESULTS_DIR}/visualizations"

if [ ! -f "$METRICS_PATH" ]; then
    echo "Arquivo de métricas não encontrado: $METRICS_PATH"
    exit 1
fi

mkdir -p "$OUTDIR"

python -m src.visualize_results \
    --metrics "$METRICS_PATH" \
    --output-dir "$OUTDIR"
