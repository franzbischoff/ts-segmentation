#!/bin/bash
# Script para gerar visualizações dos resultados do detector HDDM_W
set -e

METRICS_PATH="results/hddm_w/metrics_comprehensive_with_nab.csv"
OUTDIR="results/hddm_w/visualizations"

if [ ! -f "$METRICS_PATH" ]; then
    echo "Arquivo de métricas não encontrado: $METRICS_PATH"
    exit 1
fi

mkdir -p "$OUTDIR"

python -m src.visualize_results \
    --metrics "$METRICS_PATH" \
    --output-dir "$OUTDIR"
