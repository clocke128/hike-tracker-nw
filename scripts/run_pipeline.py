#!/usr/bin/env python3
"""Command-line entry point for the capstone pipeline."""

import argparse
import json
from datetime import date

from capstone.pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="mock", choices=["mock"])
    parser.add_argument("--as-of-date", type=date.fromisoformat)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-root", default="data")
    args = parser.parse_args()
    manifest = run_pipeline(
        source=args.source,
        as_of_date=args.as_of_date,
        seed=args.seed,
        output_root=args.output_root,
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
