from __future__ import annotations

import argparse
import sys

from data_dictionary_agent.agent_runner import run_agent
from data_dictionary_agent.config import load_config
from data_dictionary_agent.dictionary_builder import build_data_dictionary
from data_dictionary_agent.intake import load_dataset
from data_dictionary_agent.llm_descriptions import generate_llm_description_suggestions
from data_dictionary_agent.output_writers import write_dictionary_outputs, write_suggested_overrides_yaml, write_llm_safe_summary, write_llm_description_suggestions_json, write_llm_description_suggestions_markdown
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
    parser.add_argument("--mode", choices=["deterministic", "agent"], default="deterministic")
    parser.add_argument("--llm-descriptions", action="store_true", default=False)
    parser.add_argument("--llm-model", default=None)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.mode == "agent":
            result = run_agent(args.input, args.output_dir, sheet=args.sheet, config_path=args.config, sample_size=args.sample_size, top_values_limit=args.top_values_limit, llm_descriptions=args.llm_descriptions, llm_model=args.llm_model)
            profile = result["profile"]
            output_paths = result["output_paths"]
            print("profiling completed")
            print(f"rows: {profile['row_count']}")
            print(f"columns: {profile['column_count']}")
            print("mode: agent")
            for key in output_paths:
                print(f"{key}: {output_paths[key]}")
            return 0

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
        print("mode: deterministic")
        print(f"profiling_trace: {output_path}")
        print(f"data_dictionary_md: {dictionary_paths['data_dictionary_md']}")
        print(f"data_dictionary_csv: {dictionary_paths['data_dictionary_csv']}")
        print(f"data_dictionary_json: {dictionary_paths['data_dictionary_json']}")
        print(f"suggested_overrides_yaml: {suggested_overrides_path}")
        if args.llm_descriptions:
            safe_summary, suggestions = generate_llm_description_suggestions(dictionary, model=args.llm_model)
            safe_path = write_llm_safe_summary(safe_summary, args.output_dir)
            sugg_json_path = write_llm_description_suggestions_json(suggestions, args.output_dir)
            sugg_md_path = write_llm_description_suggestions_markdown(suggestions, metadata.get("source_file", "unknown"), args.output_dir)
            print(f"llm_safe_summary: {safe_path}")
            print(f"llm_description_suggestions_json: {sugg_json_path}")
            print(f"llm_description_suggestions_md: {sugg_md_path}")

        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
