#!/usr/bin/env python3
"""Fetch the pinned BnSentMix CSV used by the real-code-mixed evaluation layer."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import tempfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "literature/data/bnsentmix/dataset.csv"
SOURCE_URL = (
    "https://huggingface.co/datasets/aplycaebous/BnSentMix/"
    "resolve/main/dataset.csv?download=true"
)
EXPECTED_SHA256 = "148f23eb3dc40c1012a973efec920eaccc39700a74e5bcfb56806b0bf389029d"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = args.output
    if output.exists() and not args.force:
        actual = sha256_file(output)
        if actual != EXPECTED_SHA256:
            raise SystemExit(
                f"Existing BnSentMix CSV hash mismatch: expected {EXPECTED_SHA256}, got {actual}"
            )
        print(f"already_present={output}")
        print(f"sha256={actual}")
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix="bnsentmix-", suffix=".csv", delete=False, dir=output.parent
    ) as temporary:
        temporary_path = Path(temporary.name)
        with urllib.request.urlopen(SOURCE_URL) as response:
            shutil.copyfileobj(response, temporary)

    try:
        actual = sha256_file(temporary_path)
        if actual != EXPECTED_SHA256:
            raise SystemExit(
                f"Downloaded BnSentMix CSV hash mismatch: expected {EXPECTED_SHA256}, got {actual}"
            )
        temporary_path.replace(output)
    finally:
        temporary_path.unlink(missing_ok=True)

    print(f"downloaded={output}")
    print(f"sha256={actual}")


if __name__ == "__main__":
    main()
