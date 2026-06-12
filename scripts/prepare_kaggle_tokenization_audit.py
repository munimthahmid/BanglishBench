#!/usr/bin/env python3
"""Prepare a Kaggle CPU kernel for HuggingFace tokenizer audits."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from kaggle_with_account import credential_path, load_credentials


ROOT = Path(__file__).resolve().parents[1]
JOBS = ROOT / "kaggle_jobs"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-+", "-", slug)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_kernel_script(path: Path, dataset_slug: str, output_prefix: str, tokenizers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tokenizer_args = []
    for tokenizer in tokenizers:
        tokenizer_args.extend(["--hf-tokenizer", tokenizer])
    path.write_text(
        f'''#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


INPUT_BASE = Path("/kaggle/input")
WORKING = Path("/kaggle/working/script-matters-tokenization")
WORKING.mkdir(parents=True, exist_ok=True)
EXTRACTED = WORKING / "_extracted_inputs"
OUTPUT_PREFIX = {json.dumps(output_prefix)}
TOKENIZER_ARGS = {json.dumps(tokenizer_args)}


def show_inputs() -> None:
    print("Kaggle input tree preview:")
    for idx, path in enumerate(sorted(INPUT_BASE.rglob("*"))):
        if idx >= 120:
            print("... truncated input tree preview ...")
            break
        print(path)


def find_input_file(name: str) -> Path:
    direct_matches = [path for path in INPUT_BASE.rglob(name) if path.is_file()]
    if direct_matches:
        return direct_matches[0]

    EXTRACTED.mkdir(parents=True, exist_ok=True)
    for zip_path in INPUT_BASE.rglob("*.zip"):
        target_dir = EXTRACTED / zip_path.stem
        if not target_dir.exists():
            print(f"Extracting {{zip_path}}")
            with zipfile.ZipFile(zip_path) as archive:
                archive.extractall(target_dir)
        extracted_matches = [path for path in target_dir.rglob(name) if path.is_file()]
        if extracted_matches:
            return extracted_matches[0]

    raise FileNotFoundError(f"Could not find {{name}} under {{INPUT_BASE}}")


show_inputs()

(WORKING / "scripts").mkdir(parents=True, exist_ok=True)
(WORKING / "data").mkdir(parents=True, exist_ok=True)
shutil.copy2(find_input_file("tokenization_audit.py"), WORKING / "scripts/tokenization_audit.py")
shutil.copy2(find_input_file("items.jsonl"), WORKING / "data/items.jsonl")
shutil.copy2(find_input_file("requirements-kaggle.txt"), WORKING / "requirements-kaggle.txt")

subprocess.run(
    [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        "-r",
        str(WORKING / "requirements-kaggle.txt"),
    ],
    check=True,
)

subprocess.run(
    [
        sys.executable,
        str(WORKING / "scripts/tokenization_audit.py"),
        "--input",
        str(WORKING / "data/items.jsonl"),
        "--out",
        f"/kaggle/working/{{OUTPUT_PREFIX}}.csv",
        "--summary-out",
        f"/kaggle/working/{{OUTPUT_PREFIX}}_summary.csv",
        *TOKENIZER_ARGS,
    ],
    check=True,
)
''',
        encoding="utf-8",
    )


def prepare(args: argparse.Namespace, username: str) -> None:
    items_path = args.items_path
    if not items_path.is_absolute():
        items_path = ROOT / items_path

    dataset_ref = f"{username}/{args.dataset_slug}"
    kernel_ref = f"{username}/{args.kernel_slug}"
    assets_dir = JOBS / args.assets_job_name
    kernel_dir = JOBS / args.job_name

    if assets_dir.exists():
        shutil.rmtree(assets_dir)
    if kernel_dir.exists():
        shutil.rmtree(kernel_dir)

    copy_file(items_path, assets_dir / "items.jsonl")
    copy_file(ROOT / "requirements-kaggle.txt", assets_dir / "requirements-kaggle.txt")
    copy_file(ROOT / "scripts/tokenization_audit.py", assets_dir / "tokenization_audit.py")
    write_json(
        assets_dir / "dataset-metadata.json",
        {
            "id": dataset_ref,
            "licenses": [{"name": "unknown"}],
            "title": args.dataset_title,
        },
    )

    code_file = f"{args.job_name}.py"
    write_kernel_script(kernel_dir / code_file, args.dataset_slug, args.output_prefix, args.tokenizers)
    write_json(
        kernel_dir / "kernel-metadata.json",
        {
            "code_file": code_file,
            "dataset_sources": [dataset_ref],
            "enable_gpu": False,
            "enable_internet": True,
            "id": kernel_ref,
            "is_private": True,
            "kernel_type": "script",
            "language": "python",
            "title": args.title,
        },
    )

    print(f"Prepared dataset folder: {assets_dir}")
    print(f"Prepared kernel folder: {kernel_dir}")
    print(f"Dataset ref: {dataset_ref}")
    print(f"Kernel ref: {kernel_ref}")
    print(f"Items path: {items_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=int, default=1)
    parser.add_argument("--credential-file", type=Path)
    parser.add_argument("--items-path", type=Path, required=True)
    parser.add_argument("--dataset-slug", required=True)
    parser.add_argument("--dataset-title", default="Script Matters Tokenization Assets")
    parser.add_argument("--assets-job-name", required=True)
    parser.add_argument("--job-name", required=True)
    parser.add_argument("--kernel-slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--output-prefix", required=True)
    parser.add_argument("--tokenizers", nargs="+", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    creds = credential_path(args.account, args.credential_file)
    username, _ = load_credentials(creds)
    prepare(args, username)


if __name__ == "__main__":
    main()
