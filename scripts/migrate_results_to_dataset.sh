#!/bin/bash
# Migrate existing detector results (results/<detector>) to dataset-aware structure
# Usage: ./scripts/migrate_results_to_dataset.sh afib_paroxysmal

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <dataset_name>\nExample: $0 afib_paroxysmal"
    exit 1
fi

DATASET=$1

# Detectors to migrate (exist in results/)
DETECTORS=(adwin kswin page_hinkley hddm_a hddm_w floss)

for DET in "${DETECTORS[@]}"; do
    SRC=results/${DET}
    DST=results/${DATASET}/${DET}

    if [ ! -d "$SRC" ]; then
        echo "Skipping $SRC (not found)"
        continue
    fi

    echo "Migrating $SRC -> $DST"
    mkdir -p "$DST"

    # Move files (preserve existing)
    shopt -s dotglob
    mv $SRC/* "$DST/" || true

    # Remove old directory if empty
    rmdir "$SRC" 2>/dev/null || true
done

echo "Migration complete for dataset: $DATASET"
