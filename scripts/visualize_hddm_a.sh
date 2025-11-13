#!/bin/bash
# Script para gerar visualizações dos resultados do detector HDDM_A
set -e

METRICS_PATH="results/hddm_a/metrics_comprehensive_with_nab.csv"
OUTDIR="results/hddm_a/visualizations"

if [ ! -f "$METRICS_PATH" ]; then
    echo "Arquivo de métricas não encontrado: $METRICS_PATH"
    exit 1
fi

mkdir -p "$OUTDIR"

python -m src.visualize_results \
    --metrics "$METRICS_PATH" \
    --output-dir "$OUTDIR"
