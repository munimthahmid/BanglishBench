#!/usr/bin/env python3
"""Prepare Kaggle dataset and kernel folders for one model evaluation run."""

from __future__ import annotations

import argparse
import json
import re
import shutil
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


def write_kernel_script(
    path: Path,
    dataset_slug: str,
    model: str,
    output_name: str,
    limit: int,
    variants: list[str],
    max_new_tokens: int,
    temperature: float,
    prompt_mode: str,
    load_in_4bit: bool,
    load_in_8bit: bool,
    disable_thinking: bool,
    prompt_wrapper: str,
    bitsandbytes_requirement: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'''#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


INPUT_ROOT = Path("/kaggle/input/{dataset_slug}")
INPUT_BASE = Path("/kaggle/input")
WORKING = Path("/kaggle/working/script-matters")
WORKING.mkdir(parents=True, exist_ok=True)
EXTRACTED = WORKING / "_extracted_inputs"

MODEL = {json.dumps(model)}
OUTPUT_NAME = {json.dumps(output_name)}
LIMIT = {limit}
VARIANTS = {json.dumps(variants)}
MAX_NEW_TOKENS = {max_new_tokens}
TEMPERATURE = {temperature}
PROMPT_MODE = {json.dumps(prompt_mode)}
LOAD_IN_4BIT = {load_in_4bit}
LOAD_IN_8BIT = {load_in_8bit}
DISABLE_THINKING = {disable_thinking}
PROMPT_WRAPPER = {json.dumps(prompt_wrapper)}
BITSANDBYTES_REQUIREMENT = {json.dumps(bitsandbytes_requirement)}


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

gpu_info = subprocess.run(
    ["nvidia-smi", "--query-gpu=name,compute_cap", "--format=csv,noheader"],
    check=False,
    capture_output=True,
    text=True,
)
gpu_text = gpu_info.stdout or gpu_info.stderr
print("GPU info:")
print(gpu_text)

if LOAD_IN_4BIT and ("P100" in gpu_text or "6.0" in gpu_text):
    raise RuntimeError("4-bit bitsandbytes run requested on P100/sm_60. Use T4/L4 or a non-4-bit smoke run.")

if LOAD_IN_4BIT and LOAD_IN_8BIT:
    raise RuntimeError("Use only one quantization mode: 4-bit or 8-bit.")

if "P100" in gpu_text or "6.0" in gpu_text:
    print("Detected P100/sm_60 GPU. Installing a PyTorch build compatible with this smoke test.")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "--force-reinstall",
            "torch==2.4.1",
            "--index-url",
            "https://download.pytorch.org/whl/cu121",
        ],
        check=True,
    )
    subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", "torchvision", "torchaudio"],
        check=False,
    )

if LOAD_IN_4BIT or LOAD_IN_8BIT:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", BITSANDBYTES_REQUIREMENT],
        check=True,
    )

if (WORKING / "scripts").exists():
    shutil.rmtree(WORKING / "scripts")
(WORKING / "scripts").mkdir(parents=True, exist_ok=True)
(WORKING / "data/pilot").mkdir(parents=True, exist_ok=True)

shutil.copy2(find_input_file("run_eval_kaggle.py"), WORKING / "scripts/run_eval_kaggle.py")
shutil.copy2(find_input_file("items.jsonl"), WORKING / "data/pilot/items.jsonl")
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

os.chdir(WORKING)
run_cmd = [
    sys.executable,
    "scripts/run_eval_kaggle.py",
    "--input",
    "data/pilot/items.jsonl",
    "--output",
    f"/kaggle/working/results/runs/{{OUTPUT_NAME}}.jsonl",
    "--model",
    MODEL,
    "--limit",
    str(LIMIT),
    "--max-new-tokens",
    str(MAX_NEW_TOKENS),
    "--temperature",
    str(TEMPERATURE),
    "--prompt-mode",
    PROMPT_MODE,
    "--prompt-wrapper",
    PROMPT_WRAPPER,
    "--variants",
    *VARIANTS,
]
if LOAD_IN_4BIT:
    run_cmd.append("--load-in-4bit")
if LOAD_IN_8BIT:
    run_cmd.append("--load-in-8bit")
if DISABLE_THINKING:
    run_cmd.append("--disable-thinking")

print("Running:", " ".join(run_cmd))
subprocess.run(run_cmd, check=True)
''',
        encoding="utf-8",
    )


def prepare(args: argparse.Namespace, username: str) -> None:
    model_slug = slugify(args.model)
    kernel_slug = args.kernel_slug or f"script-matters-{model_slug}-{args.limit}-pilot"
    kernel_ref = f"{username}/{kernel_slug}"
    dataset_ref = f"{username}/{args.dataset_slug}"
    output_name = args.output_name or f"{model_slug.replace('-', '_')}_pilot{args.limit}"
    job_name = args.job_name or f"pilot_{slugify(kernel_slug).replace('-', '_')}"
    title = args.title or f"Script Matters {args.model} {args.limit} Pilot"

    assets_dir = JOBS / args.assets_job_name
    kernel_dir = JOBS / job_name

    if assets_dir.exists():
        shutil.rmtree(assets_dir)
    if kernel_dir.exists():
        shutil.rmtree(kernel_dir)

    items_path = args.items_path
    if not items_path.is_absolute():
        items_path = ROOT / items_path

    copy_file(items_path, assets_dir / "items.jsonl")
    requirements_path = args.requirements_path
    if not requirements_path.is_absolute():
        requirements_path = ROOT / requirements_path
    copy_file(requirements_path, assets_dir / "requirements-kaggle.txt")
    copy_file(ROOT / "scripts/run_eval_kaggle.py", assets_dir / "run_eval_kaggle.py")

    write_json(
        assets_dir / "dataset-metadata.json",
        {
            "id": dataset_ref,
            "licenses": [{"name": "unknown"}],
            "title": args.dataset_title,
        },
    )

    code_file = f"{job_name}.py"
    write_kernel_script(
        kernel_dir / code_file,
        args.dataset_slug,
        args.model,
        output_name,
        args.limit,
        args.variants,
        args.max_new_tokens,
        args.temperature,
        args.prompt_mode,
        args.load_in_4bit,
        args.load_in_8bit,
        args.disable_thinking,
        args.prompt_wrapper,
        args.bitsandbytes_requirement,
    )
    write_json(
        kernel_dir / "kernel-metadata.json",
        {
            "code_file": code_file,
            "dataset_sources": [dataset_ref],
            "enable_gpu": True,
            "enable_internet": True,
            "id": kernel_ref,
            "is_private": True,
            "kernel_type": "script",
            "language": "python",
            "title": title,
        },
    )

    print(f"Prepared dataset folder: {assets_dir}")
    print(f"Prepared kernel folder: {kernel_dir}")
    print(f"Dataset ref: {dataset_ref}")
    print(f"Kernel ref: {kernel_ref}")
    print(f"Output name: {output_name}")
    print(f"Items path: {items_path}")
    print(f"Requirements path: {requirements_path}")
    if args.load_in_4bit or args.load_in_8bit:
        print(f"Bitsandbytes requirement: {args.bitsandbytes_requirement}")
    print()
    print("Create dataset if needed:")
    print(
        f"python3 scripts/kaggle_with_account.py --account {args.account} -- "
        f"datasets create -p {assets_dir.relative_to(ROOT)} --dir-mode zip"
    )
    print()
    print("Or update existing dataset:")
    print(
        f"python3 scripts/kaggle_with_account.py --account {args.account} -- "
        f"datasets version -p {assets_dir.relative_to(ROOT)} -m update"
    )
    print()
    print("Push kernel:")
    print(
        f"python3 scripts/kaggle_with_account.py --account {args.account} -- "
        f"kernels push -p {kernel_dir.relative_to(ROOT)}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=int, default=1)
    parser.add_argument("--credential-file", type=Path)
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--dataset-slug", default="script-matters-pilot-assets")
    parser.add_argument("--dataset-title", default="Script Matters Pilot Assets")
    parser.add_argument("--items-path", type=Path, default=ROOT / "data/pilot/items.jsonl")
    parser.add_argument(
        "--requirements-path", type=Path, default=ROOT / "requirements-kaggle.txt"
    )
    parser.add_argument("--assets-job-name", default="pilot_assets")
    parser.add_argument("--job-name")
    parser.add_argument("--kernel-slug")
    parser.add_argument("--title")
    parser.add_argument("--output-name")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument(
        "--variants", nargs="+", default=["bangla", "banglish_clean", "english"]
    )
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument(
        "--prompt-mode",
        choices=[
            "baseline",
            "banglish_aware",
            "banglish_fewshot",
            "banglish_self_normalize",
            "banglish_self_translate_en",
            "banglish_external_normalize",
        ],
        default="baseline",
    )
    parser.add_argument("--load-in-4bit", action="store_true")
    parser.add_argument("--load-in-8bit", action="store_true")
    parser.add_argument("--bitsandbytes-requirement", default="bitsandbytes")
    parser.add_argument("--disable-thinking", action="store_true")
    parser.add_argument(
        "--prompt-wrapper",
        choices=["auto", "raw", "alpaca"],
        default="auto",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.load_in_4bit and args.load_in_8bit:
        raise SystemExit("Use only one quantization flag: --load-in-4bit or --load-in-8bit.")
    creds = credential_path(args.account, args.credential_file)
    username, _ = load_credentials(creds)
    prepare(args, username)


if __name__ == "__main__":
    main()
