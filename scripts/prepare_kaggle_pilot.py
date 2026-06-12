#!/usr/bin/env python3
"""Prepare Kaggle dataset and kernel folders for the first pilot run."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from kaggle_with_account import credential_path, load_credentials


ROOT = Path(__file__).resolve().parents[1]
JOBS = ROOT / "kaggle_jobs"
PILOT_ASSETS = JOBS / "pilot_assets"
PILOT_KERNEL = JOBS / "pilot_qwen20"


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_kernel_script(path: Path, dataset_slug: str) -> None:
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


def copytree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


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
print("GPU info:")
print(gpu_info.stdout or gpu_info.stderr)

if "P100" in gpu_info.stdout or "6.0" in gpu_info.stdout:
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
subprocess.run(
    [
        sys.executable,
        "scripts/run_eval_kaggle.py",
        "--input",
        "data/pilot/items.jsonl",
        "--output",
        "/kaggle/working/results/runs/qwen2_5_0_5b_pilot20.jsonl",
        "--model",
        "Qwen/Qwen2.5-0.5B-Instruct",
        "--limit",
        "20",
        "--variants",
        "bangla",
        "banglish_clean",
        "english",
    ],
    check=True,
)
''',
        encoding="utf-8",
    )


def prepare(username: str) -> None:
    dataset_slug = "script-matters-pilot-assets"
    dataset_ref = f"{username}/{dataset_slug}"
    kernel_slug = "script-matters-qwen-0-5b-20-pilot"
    kernel_ref = f"{username}/{kernel_slug}"

    if PILOT_ASSETS.exists():
        shutil.rmtree(PILOT_ASSETS)
    if PILOT_KERNEL.exists():
        shutil.rmtree(PILOT_KERNEL)

    copy_file(ROOT / "data/pilot/items.jsonl", PILOT_ASSETS / "items.jsonl")
    copy_file(ROOT / "requirements-kaggle.txt", PILOT_ASSETS / "requirements-kaggle.txt")
    copy_file(ROOT / "scripts/run_eval_kaggle.py", PILOT_ASSETS / "run_eval_kaggle.py")

    write_json(
        PILOT_ASSETS / "dataset-metadata.json",
        {
            "id": dataset_ref,
            "licenses": [{"name": "unknown"}],
            "title": "Script Matters Pilot Assets",
        },
    )

    write_kernel_script(PILOT_KERNEL / "pilot_qwen20.py", dataset_slug)
    write_json(
        PILOT_KERNEL / "kernel-metadata.json",
        {
            "code_file": "pilot_qwen20.py",
            "dataset_sources": [dataset_ref],
            "enable_gpu": True,
            "enable_internet": True,
            "id": kernel_ref,
            "is_private": True,
            "kernel_type": "script",
            "language": "python",
            "title": "Script Matters Qwen 0.5B 20 Pilot",
        },
    )

    print(f"Prepared dataset folder: {PILOT_ASSETS}")
    print(f"Prepared kernel folder: {PILOT_KERNEL}")
    print()
    print("Create or update the Kaggle dataset:")
    print(
        "python3 scripts/kaggle_with_account.py --account 1 -- "
        "datasets create -p kaggle_jobs/pilot_assets --dir-mode zip"
    )
    print()
    print("Push the Kaggle kernel:")
    print(
        "python3 scripts/kaggle_with_account.py --account 1 -- "
        "kernels push -p kaggle_jobs/pilot_qwen20"
    )
    print()
    print("Check status:")
    print(
        "python3 scripts/kaggle_with_account.py --account 1 -- "
        f"kernels status {kernel_ref}"
    )
    print()
    print("Download outputs:")
    print(
        "python3 scripts/kaggle_with_account.py --account 1 -- "
        f"kernels output {kernel_ref} -p results/runs/qwen2_5_0_5b_pilot20"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=int, default=1)
    parser.add_argument("--credential-file", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    creds = credential_path(args.account, args.credential_file)
    username, _ = load_credentials(creds)
    prepare(username)


if __name__ == "__main__":
    main()
