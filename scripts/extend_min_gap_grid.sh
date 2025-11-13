#!/bin/bash
# Script para estender o grid search com valores menores de min_gap_samples
# Baseado na análise do gráfico parameter_sensitivity.png que mostra potencial
# de melhora para valores abaixo de 1000

set -e

echo "========================================"
echo "Extending min_gap_samples grid search"
echo "========================================"
echo ""
echo "Current grid: 1000, 2000, 3000, 4000, 5000"
echo "New values to test: 100, 200, 300, 400, 500, 750"
echo ""

# Define paths
DATA_PATH="data/afib_paroxysmal_full.csv"
OUTPUT_PATH="results/adwin/predictions_intermediate.csv"

# Check if files exist
if [ ! -f "$DATA_PATH" ]; then
    echo "Error: Data file not found: $DATA_PATH"
    exit 1
fi

if [ ! -f "$OUTPUT_PATH" ]; then
    echo "Error: Existing predictions file not found: $OUTPUT_PATH"
    echo "Please run the initial grid search first."
    exit 1
fi

echo "Data file: $DATA_PATH"
echo "Output file: $OUTPUT_PATH"
echo ""

# Backup existing predictions
BACKUP_PATH="${OUTPUT_PATH}.backup_$(date +%Y%m%d_%H%M%S)"
echo "Creating backup: $BACKUP_PATH"
cp "$OUTPUT_PATH" "$BACKUP_PATH"
echo ""

# Run append mode with new min_gap values
echo "Starting prediction generation in APPEND mode..."
echo "This will only calculate predictions for new min_gap values."
echo ""

python -m src.generate_predictions \
    --data "$DATA_PATH" \
    --output "$OUTPUT_PATH" \
    --append \
    --min-gap 500 \
    --n-jobs 20

echo ""
echo "========================================"
echo "Grid extension completed!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Re-evaluate predictions:"
echo "   python -m src.evaluate_predictions \\"
echo "       --predictions $OUTPUT_PATH \\"
echo "       --metrics-output results/adwin/metrics_comprehensive_with_nab.csv \\"
echo "       --report-output results/adwin/final_report_with_nab.json"
echo ""
echo "2. Re-generate visualizations:"
echo "   python -m src.visualize_results \\"
echo "       --metrics results/adwin/metrics_comprehensive_with_nab.csv \\"
echo "       --output-dir results/adwin/visualizations"
echo ""
echo "Backup saved to: $BACKUP_PATH"
