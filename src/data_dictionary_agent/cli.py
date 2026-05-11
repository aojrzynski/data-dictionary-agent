from __future__ import annotations

import argparse
import sys

from data_dictionary_agent.config import load_config
from data_dictionary_agent.dictionary_builder import build_data_dictionary
from data_dictionary_agent.intake import load_dataset
from data_dictionary_agent.output_writers import write_dictionary_outputs, write_suggested_overrides_yaml
from data_dictionary_agent.profiling import build_profile
from data_dictionary_agent.suggested_overrides import build_suggested_overrides
from data_dictionary_agent.trace_writer import write_profiling_trace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic dataset profiling tool")
    parser.add_argument("--input", required=True, help="Path to CSV/XLSX/XLSM input file")
    parser.add_argument("--sheet", help="Sheet name for Excel files", default=None)
    parser.add_argument("--output-dir", default="outputs", help="Output directory")
    parser.add_argument("--sample-size", type=int, default=5)
    parser.add_argument("--top-values-limit", type=int, default=5)
    parser.add_argument("--config", help="Optional YAML config overrides", default=None)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        df, metadata = load_dataset(args.input, sheet=args.sheet)
        profile = build_profile(df, metadata, sample_size=args.sample_size, top_values_limit=args.top_values_limit)
        config = load_config(args.config)
        output_path = write_profiling_trace(profile, args.output_dir)
        dictionary = build_data_dictionary(profile, config=config)
        dictionary_paths = write_dictionary_outputs(dictionary, args.output_dir)
        suggested_overrides_path = write_suggested_overrides_yaml(build_suggested_overrides(dictionary), args.output_dir)
        print("profiling completed")
        print(f"rows: {profile['row_count']}")
        print(f"columns: {profile['column_count']}")
        print(f"profiling_trace: {output_path}")
        print(f"data_dictionary_md: {dictionary_paths['data_dictionary_md']}")
        print(f"data_dictionary_csv: {dictionary_paths['data_dictionary_csv']}")
        print(f"data_dictionary_json: {dictionary_paths['data_dictionary_json']}")
        print(f"suggested_overrides_yaml: {suggested_overrides_path}")
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
