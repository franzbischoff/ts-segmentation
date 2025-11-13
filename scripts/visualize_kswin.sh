#!/bin/bash
# Script para gerar visualizações dos resultados do detector KSWIN
set -e

METRICS_PATH="results/kswin/metrics_comprehensive_with_nab.csv"
OUTDIR="results/kswin/visualizations"

if [ ! -f "$METRICS_PATH" ]; then
    echo "Arquivo de métricas não encontrado: $METRICS_PATH"
    exit 1
fi

mkdir -p "$OUTDIR"

python -m src.visualize_results \
    --metrics "$METRICS_PATH" \
    --output-dir "$OUTDIR"
