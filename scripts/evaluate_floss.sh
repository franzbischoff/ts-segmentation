#!/usr/bin/env bash
# evaluate_floss.sh
# Evaluate FLOSS detector predictions and generate comprehensive metrics
#
# This script evaluates the FLOSS (Fast Low-rank Online Subspace Tracking) detector
# predictions from the R implementation and calculates all metrics (F1/F3, NAB, temporal).
#
# Prerequisites:
# - predictions_intermediate.csv must exist in results/floss/
# - Python environment activated (.venv)
#
# Output:
# - metrics_comprehensive_with_nab.csv (detailed metrics)
# - metrics_comprehensive_with_nab.jsonl (JSONL format)
# - final_report_with_nab.json (summary report)
# - metrics_comprehensive_with_nab_summary.json (statistics)
#
# Usage: ./scripts/evaluate_floss.sh

set -e  # Exit on error

# Configuration
DETECTOR="floss"
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
CLEAN_NAME=$(echo "$DATASET_NAME" | sed -E 's/_full$//; s/_tidy.*$//')
RESULTS_DIR="results/${CLEAN_NAME}/${DETECTOR}"
if [ ! -d "$RESULTS_DIR" ]; then
    if [ -d "results/${DATASET_NAME}/${DETECTOR}" ]; then
        RESULTS_DIR="results/${DATASET_NAME}/${DETECTOR}"
        echo "Using legacy results directory (contains suffix): $RESULTS_DIR"
    fi
fi
PREDICTIONS_PATH="${RESULTS_DIR}/predictions_intermediate.csv"
METRICS_OUTPUT="${RESULTS_DIR}/metrics_comprehensive_with_nab.csv"
REPORT_OUTPUT="${RESULTS_DIR}/final_report_with_nab.json"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  FLOSS Detector - Evaluation Pipeline${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check if predictions file exists
if [ ! -f "$PREDICTIONS_PATH" ]; then
    echo -e "${YELLOW}Error: Predictions file not found: $PREDICTIONS_PATH${NC}"
    echo "Please ensure the FLOSS predictions CSV exists before running evaluation."
    exit 1
fi

# Get file info
FILE_SIZE=$(du -h "$PREDICTIONS_PATH" | cut -f1)
NUM_LINES=$(wc -l < "$PREDICTIONS_PATH")
echo -e "${GREEN}✓${NC} Found predictions file:"
echo "  Path: $PREDICTIONS_PATH"
echo "  Size: $FILE_SIZE"
echo "  Lines: $NUM_LINES"
echo ""

# Run evaluation
echo -e "${BLUE}Starting evaluation...${NC}"
echo "This will calculate comprehensive metrics (F1/F3, NAB, temporal)."
echo ""

python -m src.evaluate_predictions \
    --predictions "$PREDICTIONS_PATH" \
    --metrics-output "$METRICS_OUTPUT" \
    --report-output "$REPORT_OUTPUT"

# Check if evaluation succeeded
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  ✓ Evaluation completed successfully!${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo "Output files:"
    echo "  - Metrics CSV: $METRICS_OUTPUT"
    echo "  - Report JSON: $REPORT_OUTPUT"
    echo "  - Metrics JSONL: ${RESULTS_DIR}/metrics_comprehensive_with_nab.jsonl"
    echo "  - Summary JSON: ${RESULTS_DIR}/metrics_comprehensive_with_nab_summary.json"
    echo ""
    echo "Next step: Run visualizations with ./scripts/visualize_floss.sh"
else
    echo -e "${YELLOW}Error: Evaluation failed. Check the output above for details.${NC}"
    exit 1
fi
