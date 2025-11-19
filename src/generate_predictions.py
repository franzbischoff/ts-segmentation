#!/usr/bin/env python3
"""
Generate intermediate predictions dataset.
Creates a dataset with all parameter combinations and their detections for each file.
This allows reusing predictions when expanding parameter grids.

Note:
- `min_gap_samples` is a post-processing filter applied by the pipeline (see
    `src/streaming_detector.py`) and **is not** a parameter of the underlying
    scikit-multiflow detectors. The grids below only enumerate values to test the
    post-processing supression of close detections during evaluation.
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


def create_param_grid_adwin(custom_params: Dict[str, List[Any]] = None) -> Dict[str, List[Any]]:
    """Create parameter grid for ADWIN detector."""
    if custom_params:
        return custom_params

    return {
        'delta': [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1],
        'ma_window': [10, 25, 50, 75, 100, 150, 200, 250, 300],
        # NOTE: this is a post-processing filter (see src/streaming_detector.py)
        # The detectors themselves do not support min_gap_samples — we use it to
        # suppress consecutive detections within the given number of samples.
        'min_gap_samples': list(range(1000, 6000, 1000)),
    }
    # Total: 11 × 9 × 5 = 495 combinations


def create_param_grid_page_hinkley(custom_params: Dict[str, List[Any]] = None) -> Dict[str, List[Any]]:
    """Create parameter grid for Page-Hinkley detector."""
    if custom_params:
        return custom_params

    return {
        'lambda_': [10, 30, 50, 80],  # Threshold (4 valores)
        'delta': [0.005, 0.01, 0.02, 0.04],  # Permissiveness (4 valores)
        'alpha': [0.9999, 0.99],  # Forgetting factor (2 valores - 0.9999 melhor na validação)
        'ma_window': [10, 50, 200],  # Moving average (3 valores)
        # NOTE: `min_gap_samples` is applied in the pipeline's post-processing
        # step. It is not an intrinsic detector parameter — we include it so we
        # can evaluate how different temporal suppression windows affect metrics.
        'min_gap_samples': [500, 1000, 2000, 4000],  # Gap samples (4 valores)
    }
    # Total: 4 × 4 × 2 × 3 × 4 = 384 combinations (moderado - reduzido de 9,408)


def create_param_grid_kswin(custom_params: Dict[str, List[Any]] = None) -> Dict[str, List[Any]]:
    """Create parameter grid for KSWIN detector."""
    if custom_params:
        return custom_params

    return {
        'alpha': [0.001, 0.005, 0.01, 0.05],  # Significance level
        'window_size': [50, 100, 200, 500],  # Reference window size
        'stat_size': [20, 30, 50, 100],  # Statistical window size
        'ma_window': [1, 10, 50, 100],  # Moving average (1 = no smoothing)
        # NOTE: `min_gap_samples` is a pipeline post-processing option used
        # to reduce multiple detections that occur in quick succession.
        'min_gap_samples': [500, 1000, 2000, 3000, 5000],
    }
    # Total: 4 × 4 × 4 × 4 × 5 = 1,280 combinations


def create_param_grid_hddm_a(custom_params: Dict[str, List[Any]] = None) -> Dict[str, List[Any]]:
    """Create parameter grid for HDDM_A detector."""
    if custom_params:
        return custom_params

    return {
        'drift_confidence': [0.0001, 0.0005, 0.001, 0.005],  # Drift confidence level
        'warning_confidence': [0.001, 0.005, 0.01, 0.05],  # Warning confidence level
        'two_side_option': [True, False],  # Two-sided or one-sided test
        'ma_window': [1, 10, 50, 100],  # Moving average (1 = no smoothing)
        # NOTE: `min_gap_samples` is a pipeline post-processing option used
        # to reduce multiple detections that occur in quick succession.
        'min_gap_samples': [500, 1000, 2000, 3000, 5000],
    }
    # Total: 4 × 4 × 2 × 4 × 5 = 640 combinations


def create_param_grid_hddm_w(custom_params: Dict[str, List[Any]] = None) -> Dict[str, List[Any]]:
    """Create parameter grid for HDDM_W detector."""
    if custom_params:
        return custom_params

    return {
        'drift_confidence': [0.0001, 0.0005, 0.001, 0.005],  # Drift confidence level
        'warning_confidence': [0.001, 0.005, 0.01, 0.05],  # Warning confidence level
        'lambda_option': [0.01, 0.05, 0.1, 0.2],  # Weighting factor
        'two_side_option': [True, False],  # Two-sided or one-sided test
        'ma_window': [1, 10, 50, 100],  # Moving average (1 = no smoothing)
        # NOTE: `min_gap_samples` is a pipeline post-processing option used
        # to reduce multiple detections that occur in quick succession.
        'min_gap_samples': [500, 1000, 2000, 3000, 5000],
    }
    # Total: 4 × 4 × 4 × 2 × 4 × 5 = 2,560 combinations


def create_param_grid(detector_name: str, custom_params: Dict[str, List[Any]] = None) -> Dict[str, List[Any]]:
    """Create parameter grid based on detector type."""
    detector_lower = detector_name.lower()

    if detector_lower == 'adwin':
        return create_param_grid_adwin(custom_params)
    elif detector_lower in ['page_hinkley', 'ph']:
        return create_param_grid_page_hinkley(custom_params)
    elif detector_lower == 'kswin':
        return create_param_grid_kswin(custom_params)
    elif detector_lower in ['hddm_a', 'hddm-a']:
        return create_param_grid_hddm_a(custom_params)
    elif detector_lower in ['hddm_w', 'hddm-w']:
        return create_param_grid_hddm_w(custom_params)
    else:
        raise ValueError(f"Unknown detector: {detector_name}")


def extract_detector_params(detector_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Extract detector-specific parameters from combined params dict."""
    detector_lower = detector_name.lower()

    if detector_lower == 'adwin':
        return {'delta': params['delta']}
    elif detector_lower in ['page_hinkley', 'ph']:
        return {
            'lambda_': params['lambda_'],
            'delta': params['delta'],
            'alpha': params['alpha']
        }
    elif detector_lower == 'kswin':
        return {
            'alpha': params['alpha'],
            'window_size': params['window_size'],
            'stat_size': params['stat_size']
        }
    elif detector_lower in ['hddm_a', 'hddm-a']:
        return {
            'drift_confidence': params['drift_confidence'],
            'warning_confidence': params['warning_confidence'],
            'two_side_option': params['two_side_option']
        }
    elif detector_lower in ['hddm_w', 'hddm-w']:
        return {
            'drift_confidence': params['drift_confidence'],
            'warning_confidence': params['warning_confidence'],
            'lambda_option': params['lambda_option'],
            'two_side_option': params['two_side_option']
        }
    else:
        raise ValueError(f"Unknown detector: {detector_name}")


def get_result_columns(detector_name: str) -> List[str]:
    """Get parameter column names for a specific detector."""
    detector_lower = detector_name.lower()

    if detector_lower == 'adwin':
        return ['delta', 'ma_window', 'min_gap_samples']
    elif detector_lower in ['page_hinkley', 'ph']:
        return ['lambda_', 'delta', 'alpha', 'ma_window', 'min_gap_samples']
    elif detector_lower == 'kswin':
        return ['alpha', 'window_size', 'stat_size', 'ma_window', 'min_gap_samples']
    elif detector_lower in ['hddm_a', 'hddm-a']:
        return ['drift_confidence', 'warning_confidence', 'two_side_option', 'ma_window', 'min_gap_samples']
    elif detector_lower in ['hddm_w', 'hddm-w']:
        return ['drift_confidence', 'warning_confidence', 'lambda_option', 'two_side_option', 'ma_window', 'min_gap_samples']
    else:
        raise ValueError(f"Unknown detector: {detector_name}")


def process_single_file_predictions(record_id: str, record_data: pd.DataFrame,
                                  param_combinations: List[Dict[str, Any]],
                                  detector_name: str = 'adwin',
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
            detector_params = extract_detector_params(detector_name, params)

            # Run detection
            events, metrics, actual_detector_name = run_stream_on_dataframe(
                df=record_data,
                detector_name=detector_name,
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
                'detector': actual_detector_name,
                **params,  # Include all parameters
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
                'detector': detector_name,
                **params,  # Include all parameters
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


def load_existing_predictions(file_path: str) -> pd.DataFrame:
    """Load existing predictions CSV if it exists."""
    path = Path(file_path)
    if path.exists():
        print(f"Loading existing predictions from {file_path}")
        df = pd.read_csv(file_path)
        print(f"Found {len(df)} existing predictions")
        return df
    return pd.DataFrame()


def filter_new_combinations(param_combinations: List[Dict[str, Any]],
                           existing_df: pd.DataFrame,
                           detector_name: str,
                           record_ids: List[str]) -> List[Dict[str, Any]]:
    """Filter out parameter combinations that already exist in the dataset."""
    if existing_df.empty:
        return param_combinations

    # Get parameter column names for this detector
    param_cols = get_result_columns(detector_name)

    # Get unique combinations from existing data
    existing_combos = existing_df[param_cols].drop_duplicates()

    # Create set of existing tuples for fast lookup
    existing_set = set()
    for _, row in existing_combos.iterrows():
        combo_tuple = tuple(row[col] for col in param_cols)
        existing_set.add(combo_tuple)

    # Filter out existing combinations
    new_combinations = []
    for params in param_combinations:
        combo_tuple = tuple(params[col] for col in param_cols)
        if combo_tuple not in existing_set:
            new_combinations.append(params)

    skipped = len(param_combinations) - len(new_combinations)
    print(f"Skipping {skipped} existing combinations, {len(new_combinations)} new combinations to process")

    return new_combinations


def generate_predictions_dataset(data_path: str, output_path: str,
                               detector_name: str = 'adwin',
                               sample_rate: int = 250,
                               n_jobs: int = -1, max_files: int = None, max_samples: int = None,
                               custom_param_grid: Dict[str, List[Any]] = None,
                               append_mode: bool = False) -> None:
    """Generate intermediate predictions dataset.

    Args:
        data_path: Path to tidy CSV with id column
        output_path: Output CSV path for predictions
        detector_name: Name of detector ('adwin', 'page_hinkley', 'kswin', 'hddm_a', 'hddm_w')
        sample_rate: Sampling rate
        n_jobs: Number of parallel jobs (-1 for all cores)
        max_files: Limit number of files (for testing)
        max_samples: Limit samples per file (for testing)
        custom_param_grid: Custom parameter grid (if None, use default)
        append_mode: If True, load existing predictions and only generate new combinations
    """

    # Load existing predictions if in append mode
    existing_df = pd.DataFrame()
    if append_mode:
        existing_df = load_existing_predictions(output_path)

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
    print(f"Using detector: {detector_name}")

    # Create parameter combinations
    param_grid = create_param_grid(detector_name, custom_param_grid)
    param_names = list(param_grid.keys())
    param_combinations = [
        dict(zip(param_names, values))
        for values in itertools.product(*param_grid.values())
    ]

    # Filter out existing combinations if in append mode
    if append_mode:
        param_combinations = filter_new_combinations(param_combinations, existing_df, detector_name, unique_ids.tolist())

        if len(param_combinations) == 0:
            print("No new combinations to process. All requested parameters already exist.")
            return

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
                record_id, record_data, param_combinations, detector_name, sample_rate, max_samples
            )
            all_results.extend(results)
    else:
        # Parallel processing
        print("Starting parallel prediction generation...")

        def process_record(record_id):
            record_data = df[df['id'] == record_id].copy()
            record_data = record_data.reset_index(drop=True)
            return process_single_file_predictions(
                record_id, record_data, param_combinations, detector_name, sample_rate, max_samples
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
    print(f"Generated {len(all_results):,} new predictions")

    # Convert to DataFrame
    new_results_df = pd.DataFrame(all_results)

    # Merge with existing data if in append mode
    if append_mode and not existing_df.empty:
        print(f"Merging {len(new_results_df)} new predictions with {len(existing_df)} existing predictions")
        results_df = pd.concat([existing_df, new_results_df], ignore_index=True)
        print(f"Total predictions after merge: {len(results_df)}")
    else:
        results_df = new_results_df

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
    # Derive dataset name for metadata
    try:
        dataset_name = Path(data_path).stem
    except Exception:
        dataset_name = data_path

    summary = {
        'dataset': dataset_name,
        'total_files': len(unique_ids),
        'new_param_combinations': len(param_combinations),
        'new_predictions': len(all_results),
        'total_predictions_in_file': len(results_df),
        'processing_time_seconds': elapsed_time,
        'param_grid': param_grid,
        'sample_rate': sample_rate,
        'append_mode': append_mode,
        'error_count': sum(1 for r in all_results if 'error' in r),
        'avg_processing_time_per_prediction': elapsed_time / len(all_results) if all_results else 0
    }

    summary_path = output_path.replace('.csv', '_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to: {summary_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate intermediate predictions dataset',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate with default grid for ADWIN (dataset-aware results directory)
    python -m src.generate_predictions --detector adwin --data data.csv --output results/<dataset>/adwin/predictions.csv

    # Generate for Page-Hinkley
    python -m src.generate_predictions --detector page_hinkley --data data.csv --output results/<dataset>/page_hinkley/predictions.csv

  # Append new min_gap values to existing predictions
  python -m src.generate_predictions --detector adwin --data data.csv --output results/adwin/predictions.csv \\
      --append --min-gap 100 200 300 400 500 750

  # Custom full grid for Page-Hinkley
  python -m src.generate_predictions --detector page_hinkley --data data.csv --output results/page_hinkley/predictions.csv \\
      --lambda 10 20 30 --delta 0.01 0.02 --alpha 0.9999 0.999 --ma-window 10 50 100 --min-gap 500 1000 1500
        """
    )
    parser.add_argument('--detector', required=True,
                       choices=['adwin', 'page_hinkley', 'kswin', 'hddm_a', 'hddm_w'],
                       help='Detector type to use')
    parser.add_argument('--data', required=True, help='Path to tidy CSV with id column')
    parser.add_argument('--output', required=True, help='Output CSV path for predictions')
    parser.add_argument('--sample-rate', type=int, default=250, help='Sampling rate')
    parser.add_argument('--n-jobs', type=int, default=-1, help='Number of parallel jobs')
    parser.add_argument('--max-files', type=int, default=None, help='Limit number of files (for testing)')
    parser.add_argument('--max-samples', type=int, default=None, help='Limit samples per file (for testing)')

    # Append mode
    parser.add_argument('--append', action='store_true',
                       help='Append mode: load existing predictions and only generate new combinations')

    # Custom parameter grid - Common parameters
    parser.add_argument('--ma-window', type=int, nargs='+', default=None,
                       help='MA window values to test (overrides default)')
    parser.add_argument('--min-gap', type=int, nargs='+', default=None,
                       help='Min gap samples to test (overrides default)')

    # ADWIN specific
    parser.add_argument('--delta', type=float, nargs='+', default=None,
                       help='Delta values to test (ADWIN) (overrides default)')

    # Page-Hinkley specific
    parser.add_argument('--lambda', '--lambda_', dest='lambda_', type=float, nargs='+', default=None,
                       help='Lambda (threshold) values to test (Page-Hinkley) (overrides default)')
    parser.add_argument('--ph-delta', type=float, nargs='+', default=None,
                       help='Delta (permissiveness) values for Page-Hinkley (overrides default)')
    parser.add_argument('--alpha', type=float, nargs='+', default=None,
                       help='Alpha (forgetting factor) values to test (Page-Hinkley/KSWIN) (overrides default)')

    # KSWIN specific
    parser.add_argument('--ks-alpha', type=float, nargs='+', default=None,
                       help='Alpha (significance level) values for KSWIN (overrides default)')
    parser.add_argument('--window-size', type=int, nargs='+', default=None,
                       help='Window size values for KSWIN (overrides default)')
    parser.add_argument('--stat-size', type=int, nargs='+', default=None,
                       help='Statistical window size values for KSWIN (overrides default)')

    # HDDM specific
    parser.add_argument('--drift-confidence', type=float, nargs='+', default=None,
                       help='Drift confidence values for HDDM (overrides default)')
    parser.add_argument('--warning-confidence', type=float, nargs='+', default=None,
                       help='Warning confidence values for HDDM (overrides default)')
    parser.add_argument('--lambda-option', type=float, nargs='+', default=None,
                       help='Lambda (weighting) values for HDDM_W (overrides default)')
    parser.add_argument('--two-side', action='store_true',
                       help='Use two-sided test for HDDM (overrides default)')

    args = parser.parse_args()

    # Build custom parameter grid if specified
    custom_param_grid = None
    detector_lower = args.detector.lower()

    # Check if any custom params specified
    has_custom = (args.ma_window or args.min_gap or args.delta or
                  args.lambda_ or args.ph_delta or args.alpha)

    if has_custom:
        # Load defaults for this detector
        default_grid = create_param_grid(detector_lower)

        if detector_lower == 'adwin':
            custom_param_grid = {
                'delta': args.delta if args.delta else default_grid['delta'],
                'ma_window': args.ma_window if args.ma_window else default_grid['ma_window'],
                'min_gap_samples': args.min_gap if args.min_gap else default_grid['min_gap_samples']
            }
        elif detector_lower in ['page_hinkley', 'ph']:
            custom_param_grid = {
                'lambda_': args.lambda_ if args.lambda_ else default_grid['lambda_'],
                'delta': args.ph_delta if args.ph_delta else default_grid['delta'],
                'alpha': args.alpha if args.alpha else default_grid['alpha'],
                'ma_window': args.ma_window if args.ma_window else default_grid['ma_window'],
                'min_gap_samples': args.min_gap if args.min_gap else default_grid['min_gap_samples']
            }
        elif detector_lower == 'kswin':
            custom_param_grid = {
                'alpha': args.ks_alpha if args.ks_alpha else default_grid['alpha'],
                'window_size': args.window_size if args.window_size else default_grid['window_size'],
                'stat_size': args.stat_size if args.stat_size else default_grid['stat_size'],
                'ma_window': args.ma_window if args.ma_window else default_grid['ma_window'],
                'min_gap_samples': args.min_gap if args.min_gap else default_grid['min_gap_samples']
            }
        elif detector_lower in ['hddm_a', 'hddm-a']:
            two_side_values = [True, False] if args.two_side else default_grid['two_side_option']
            custom_param_grid = {
                'drift_confidence': args.drift_confidence if args.drift_confidence else default_grid['drift_confidence'],
                'warning_confidence': args.warning_confidence if args.warning_confidence else default_grid['warning_confidence'],
                'two_side_option': two_side_values,
                'ma_window': args.ma_window if args.ma_window else default_grid['ma_window'],
                'min_gap_samples': args.min_gap if args.min_gap else default_grid['min_gap_samples']
            }
        elif detector_lower in ['hddm_w', 'hddm-w']:
            two_side_values = [True, False] if args.two_side else default_grid['two_side_option']
            custom_param_grid = {
                'drift_confidence': args.drift_confidence if args.drift_confidence else default_grid['drift_confidence'],
                'warning_confidence': args.warning_confidence if args.warning_confidence else default_grid['warning_confidence'],
                'lambda_option': args.lambda_option if args.lambda_option else default_grid['lambda_option'],
                'two_side_option': two_side_values,
                'ma_window': args.ma_window if args.ma_window else default_grid['ma_window'],
                'min_gap_samples': args.min_gap if args.min_gap else default_grid['min_gap_samples']
            }

        print("Using custom parameter grid:")
        for param, values in custom_param_grid.items():
            print(f"  {param}: {values}")

    generate_predictions_dataset(
        data_path=args.data,
        output_path=args.output,
        detector_name=args.detector,
        sample_rate=args.sample_rate,
        n_jobs=args.n_jobs,
        max_files=args.max_files,
        max_samples=args.max_samples,
        custom_param_grid=custom_param_grid,
        append_mode=args.append
    )


if __name__ == '__main__':
    main()
