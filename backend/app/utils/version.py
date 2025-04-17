# utils/version.py

import subprocess

def get_git_version():
    try:
        version = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"]
        ).decode("utf-8").strip()
        return version
    except Exception:
        return "unknown"
