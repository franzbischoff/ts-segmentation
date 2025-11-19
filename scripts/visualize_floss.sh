#!/usr/bin/env bash
# visualize_floss.sh
# Generate comprehensive visualizations for FLOSS detector results
#
# This script creates 9 visualization plots analyzing the FLOSS detector performance:
# - Precision-Recall scatter plots
# - Pareto front analysis
# - Parameter sensitivity heatmaps
# - Score distributions
# - 3D trade-off surfaces
# - Parameter sensitivity analysis
#
# Prerequisites:
# - metrics_comprehensive_with_nab.csv must exist in results/floss/
# - Python environment activated (.venv)
#
# Output:
# - 9 PNG files in results/floss/visualizations/
#
# Usage: ./scripts/visualize_floss.sh

set -e  # Exit on error

# Configuration
DETECTOR="floss"
DATA_PATH="data/afib_paroxysmal_full.csv"
if [ -n "$1" ]; then
    DATA_PATH="$1"
fi
DATASET_NAME=$(basename "$DATA_PATH" .csv | sed -E 's/_full$//; s/_tidy.*$//')
RESULTS_DIR="results/${DATASET_NAME}/${DETECTOR}"
METRICS_PATH="${RESULTS_DIR}/metrics_comprehensive_with_nab.csv"
OUTPUT_DIR="${RESULTS_DIR}/visualizations"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  FLOSS Detector - Visualization Pipeline${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check if metrics file exists
if [ ! -f "$METRICS_PATH" ]; then
    echo -e "${YELLOW}Error: Metrics file not found: $METRICS_PATH${NC}"
    echo "Please run ./scripts/evaluate_floss.sh first to generate metrics."
    exit 1
fi

# Get file info
FILE_SIZE=$(du -h "$METRICS_PATH" | cut -f1)
NUM_LINES=$(wc -l < "$METRICS_PATH")
echo -e "${GREEN}✓${NC} Found metrics file:"
echo "  Path: $METRICS_PATH"
echo "  Size: $FILE_SIZE"
echo "  Lines: $NUM_LINES"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"
echo -e "${GREEN}✓${NC} Output directory: $OUTPUT_DIR"
echo ""

# Run visualization
echo -e "${BLUE}Generating visualizations...${NC}"
echo "This will create 9 plots analyzing FLOSS performance."
echo ""

python -m src.visualize_results \
    --metrics "$METRICS_PATH" \
    --output-dir "$OUTPUT_DIR"

# Check if visualization succeeded
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  ✓ Visualizations completed successfully!${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo "Generated plots in $OUTPUT_DIR:"

    # List generated files
    if [ -d "$OUTPUT_DIR" ]; then
        for file in "$OUTPUT_DIR"/*.png; do
            if [ -f "$file" ]; then
                FILE_SIZE=$(du -h "$file" | cut -f1)
                echo "  - $(basename "$file") ($FILE_SIZE)"
            fi
        done
    fi

    echo ""
    echo "You can view the plots with:"
    echo "  xdg-open $OUTPUT_DIR/pareto_front.png"
    echo ""
    echo "Or browse all visualizations:"
    echo "  ls -lh $OUTPUT_DIR/"
else
    echo -e "${YELLOW}Error: Visualization failed. Check the output above for details.${NC}"
    exit 1
fi
