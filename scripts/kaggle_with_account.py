#!/usr/bin/env python3
"""Run Kaggle CLI commands with one of several local credential files.

Credential files are intentionally not printed. Supported formats:

1. Kaggle's downloaded JSON:
   {"username": "your_username", "key": "your_api_key"}

2. Environment-style text:
   KAGGLE_USERNAME=your_username
   KAGGLE_KEY=your_api_key

3. Two-line text:
   your_username
   your_api_key
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCAL_KAGGLE_CONFIG_DIR = ROOT / ".kaggle"


def parse_env_style(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def load_credentials(path: Path) -> tuple[str, str]:
    if not path.exists():
        raise SystemExit(f"Credential file does not exist: {path}")

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit(f"Credential file is empty: {path}")

    username = ""
    key = ""

    if text.startswith("{"):
        data = json.loads(text)
        username = str(data.get("username") or "")
        key = str(data.get("key") or "")
    else:
        data = parse_env_style(text)
        username = data.get("KAGGLE_USERNAME") or data.get("username") or ""
        key = data.get("KAGGLE_KEY") or data.get("KAGGLE_API_KEY") or data.get("key") or ""

        if not username or not key:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            if len(lines) >= 2:
                username, key = lines[0], lines[1]

    if not username or not key:
        raise SystemExit(
            "Could not parse credentials. File must include both Kaggle username and key."
        )

    return username, key


def credential_path(account: int | None, explicit: Path | None) -> Path:
    if explicit:
        return explicit
    if account is None:
        raise SystemExit("Pass --account N or --credential-file PATH.")
    root_path = ROOT / f"kaggle_api{account}.txt"
    if root_path.exists():
        return root_path
    local_config_path = LOCAL_KAGGLE_CONFIG_DIR / f"kaggle_api{account}.txt"
    if local_config_path.exists():
        return local_config_path
    return root_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=int, help="Use kaggle_apiN.txt from repo root.")
    parser.add_argument("--credential-file", type=Path)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate local file and Kaggle CLI availability without calling Kaggle.",
    )
    parser.add_argument("kaggle_args", nargs=argparse.REMAINDER)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = credential_path(args.account, args.credential_file)
    username, key = load_credentials(path)

    kaggle_bin = shutil.which("kaggle")
    if not kaggle_bin:
        raise SystemExit("Kaggle CLI is not installed. Install with: python3 -m pip install --user kaggle")

    env = os.environ.copy()
    env["KAGGLE_USERNAME"] = username
    env["KAGGLE_KEY"] = key
    env["KAGGLE_CONFIG_DIR"] = str(LOCAL_KAGGLE_CONFIG_DIR)
    LOCAL_KAGGLE_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if args.check_only:
        version = subprocess.run(
            [kaggle_bin, "--version"],
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )
        print(f"Credentials parsed for Kaggle username: {username}")
        print(f"Kaggle CLI found: {kaggle_bin}")
        print((version.stdout or version.stderr).strip())
        return

    kaggle_args = args.kaggle_args
    if kaggle_args and kaggle_args[0] == "--":
        kaggle_args = kaggle_args[1:]
    if not kaggle_args:
        raise SystemExit("Pass Kaggle CLI arguments after --, e.g. -- kernels list --mine")

    completed = subprocess.run([kaggle_bin, *kaggle_args], env=env, check=False)
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
