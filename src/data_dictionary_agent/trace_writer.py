"""Writer for deterministic profiling trace evidence."""

from __future__ import annotations
import json
from pathlib import Path


def write_profiling_trace(profile: dict, output_dir: str | Path) -> Path:
    """Persist profiling evidence to profiling_trace.json."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    output_path = out_dir / "profiling_trace.json"
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, sort_keys=True)
        f.write("\n")

    return output_path
