#!/usr/bin/env python3
"""
Generate intermediate predictions dataset.
Creates a dataset with all parameter combinations and their detections for each file.
This allows reusing predictions when expanding parameter grids.
"""

import argparse
import itertools
import json
import time
import random
from pathlib import Path
from typing import Dict, List, Any

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

# Set seeds for reproducibility
random.seed(42)
np.random.seed(42)

from src.streaming_detector import run_stream_on_dataframe
from src.data_loader import load_dataset


def create_param_grid() -> Dict[str, List[Any]]:
    """Create exhaustive parameter grid."""
    return {
        'delta': [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1],  # 11 values
        'ma_window': [10, 25, 50, 75, 100, 150, 200, 250, 300],                          # 9 specific values
        'min_gap_samples': list(range(1000, 6000, 1000)),                               # 5 values (1000,2000,3000,4000,5000)
    }
    # Total: 11 × 9 × 5 = 495 combinations

def process_single_file_predictions(record_id: str, record_data: pd.DataFrame,
                                  param_combinations: List[Dict[str, Any]],
                                  sample_rate: int = 250, max_samples: int = None) -> List[Dict[str, Any]]:
    """Process a single file and generate predictions for all parameter combinations."""

    # Limit samples for testing
    if max_samples and len(record_data) > max_samples:
        record_data = record_data.head(max_samples).copy()
        print(f"  {record_id}: Limited to {max_samples} samples for testing")

    print(f"Processing {record_id}: {len(record_data)} samples, {len(param_combinations)} param combinations")

    # Extract ground truth
    gt_indices = record_data.index[record_data['regime_change'] == 1].tolist()
    gt_times = [idx / sample_rate for idx in gt_indices]

    results = []

    for i, params in enumerate(param_combinations):
        if (i + 1) % 50 == 0:
            print(f"  {record_id}: {i+1}/{len(param_combinations)} combinations")

        start_time = time.time()

        try:
            # Configure detector parameters
            detector_params = {'delta': params['delta']}

            # Run detection
            events, metrics, detector_name = run_stream_on_dataframe(
                df=record_data,
                detector_name='adwin',
                sample_rate=sample_rate,
                tolerance=500,  # Not used for evaluation here, just for compatibility
                detector_params=detector_params,
                ma_window=params['ma_window'],
                use_derivative=False,
                min_gap_samples=params['min_gap_samples']
            )

            # Extract detection times
            det_times = [event.time_seconds for event in events]
            det_indices = [event.sample_index for event in events]

            result = {
                'record_id': record_id,
                'detector': detector_name,
                'delta': params['delta'],
                'ma_window': params['ma_window'],
                'min_gap_samples': params['min_gap_samples'],
                'duration_samples': len(record_data),
                'duration_seconds': len(record_data) / sample_rate,
                'gt_indices': gt_indices,
                'gt_times': gt_times,
                'det_indices': det_indices,
                'det_times': det_times,
                'n_detections': len(events),
                'n_ground_truth': len(gt_times),
                'processing_time': time.time() - start_time
            }

            results.append(result)

        except Exception as e:
            result = {
                'record_id': record_id,
                'detector': 'adwin',
                'delta': params['delta'],
                'ma_window': params['ma_window'],
                'min_gap_samples': params['min_gap_samples'],
                'duration_samples': len(record_data),
                'duration_seconds': len(record_data) / sample_rate,
                'gt_indices': gt_indices,
                'gt_times': gt_times,
                'det_indices': [],
                'det_times': [],
                'n_detections': 0,
                'n_ground_truth': len(gt_times),
                'processing_time': time.time() - start_time,
                'error': str(e)
            }
            results.append(result)

    return results


def generate_predictions_dataset(data_path: str, output_path: str, sample_rate: int = 250,
                               n_jobs: int = -1, max_files: int = None, max_samples: int = None) -> None:
    """Generate intermediate predictions dataset."""

    # Load data
    print(f"Loading data from {data_path}")
    df, _ = load_dataset(data_path, sample_rate=sample_rate)

    if 'id' not in df.columns:
        raise ValueError("Dataset must contain 'id' column for per-file processing")

    # Group by ID
    unique_ids = df['id'].unique()
    if max_files:
        unique_ids = unique_ids[:max_files]
        print(f"Limited to {max_files} files for testing")

    print(f"Found {len(unique_ids)} unique record IDs")

    # Create parameter combinations
    param_grid = create_param_grid()
    param_names = list(param_grid.keys())
    param_combinations = [
        dict(zip(param_names, values))
        for values in itertools.product(*param_grid.values())
    ]

    print(f"Testing {len(param_combinations)} parameter combinations per file")
    print(f"Total predictions to generate: {len(unique_ids)} files × {len(param_combinations)} params = {len(unique_ids) * len(param_combinations):,}")

    start_time = time.time()

    # Process files in parallel
    if n_jobs == 1:
        # Sequential processing
        all_results = []
        for record_id in unique_ids:
            record_data = df[df['id'] == record_id].copy()
            record_data = record_data.reset_index(drop=True)
            results = process_single_file_predictions(
                record_id, record_data, param_combinations, sample_rate, max_samples
            )
            all_results.extend(results)
    else:
        # Parallel processing
        print("Starting parallel prediction generation...")

        def process_record(record_id):
            record_data = df[df['id'] == record_id].copy()
            record_data = record_data.reset_index(drop=True)
            return process_single_file_predictions(
                record_id, record_data, param_combinations, sample_rate, max_samples
            )

        parallel_results = Parallel(n_jobs=n_jobs)(
            delayed(process_record)(record_id) for record_id in unique_ids
        )

        # Flatten results
        all_results = []
        for results in parallel_results:
            all_results.extend(results)

    elapsed_time = time.time() - start_time
    print(f"\nPrediction generation completed in {elapsed_time:.1f}s")
    print(f"Generated {len(all_results):,} total predictions")

    # Convert to DataFrame and save
    results_df = pd.DataFrame(all_results)

    # Save as CSV
    csv_path = output_path
    results_df.to_csv(csv_path, index=False)
    print(f"\nResults saved to: {csv_path}")

    # Also save as JSON Lines for easier inspection
    jsonl_path = output_path.replace('.csv', '.jsonl')
    with open(jsonl_path, 'w') as f:
        for result in all_results:
            f.write(json.dumps(result) + '\n')
    print(f"JSONL format saved to: {jsonl_path}")

    # Save summary statistics
    summary = {
        'total_files': len(unique_ids),
        'total_param_combinations': len(param_combinations),
        'total_predictions': len(all_results),
        'processing_time_seconds': elapsed_time,
        'param_grid': param_grid,
        'sample_rate': sample_rate,
        'error_count': sum(1 for r in all_results if 'error' in r),
        'avg_processing_time_per_prediction': elapsed_time / len(all_results)
    }

    summary_path = output_path.replace('.csv', '_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to: {summary_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate intermediate predictions dataset')
    parser.add_argument('--data', required=True, help='Path to tidy CSV with id column')
    parser.add_argument('--output', required=True, help='Output CSV path for predictions')
    parser.add_argument('--sample-rate', type=int, default=250, help='Sampling rate')
    parser.add_argument('--n-jobs', type=int, default=-1, help='Number of parallel jobs')
    parser.add_argument('--max-files', type=int, default=None, help='Limit number of files (for testing)')
    parser.add_argument('--max-samples', type=int, default=None, help='Limit samples per file (for testing)')

    args = parser.parse_args()

    generate_predictions_dataset(
        data_path=args.data,
        output_path=args.output,
        sample_rate=args.sample_rate,
        n_jobs=args.n_jobs,
        max_files=args.max_files,
        max_samples=args.max_samples
    )


if __name__ == '__main__':
    main()
