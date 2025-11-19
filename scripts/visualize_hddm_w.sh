#!/bin/bash
# Script para gerar visualizações dos resultados do detector HDDM_W
set -e

DATA_PATH="data/afib_paroxysmal_full.csv"
if [ -n "$1" ]; then
    DATA_PATH="$1"
fi
DATASET_NAME=$(basename "$DATA_PATH" .csv | sed -E 's/_full$//; s/_tidy.*$//')
DETECTOR="hddm_w"
RESULTS_DIR="results/${DATASET_NAME}/${DETECTOR}"
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
