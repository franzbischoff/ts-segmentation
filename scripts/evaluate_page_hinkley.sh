#!/bin/bash
# Script para avaliar as métricas do detector Page-Hinkley
set -e

PRED_PATH="results/page_hinkley/predictions_intermediate.csv"
METRICS_PATH="results/page_hinkley/metrics_comprehensive_with_nab.csv"
REPORT_PATH="results/page_hinkley/final_report_with_nab.json"

if [ ! -f "$PRED_PATH" ]; then
    echo "Arquivo de predições não encontrado: $PRED_PATH"
    exit 1
fi

python -m src.evaluate_predictions \
    --predictions "$PRED_PATH" \
    --metrics-output "$METRICS_PATH" \
    --report-output "$REPORT_PATH"
