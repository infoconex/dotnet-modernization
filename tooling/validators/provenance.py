"""Capture and enforce immutable Git checkout identity for validation evidence."""
import re
import subprocess
from pathlib import Path


def git(root, *args):
    try:
        result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True,
                                errors='replace', timeout=10, check=False)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def snapshot(source):
    root = Path(source).resolve(strict=True)
    dirty = git(root, 'status', '--porcelain', '--untracked-files=normal')
    return {'commit': git(root, 'rev-parse', 'HEAD'),
            'branch': git(root, 'branch', '--show-current'),
            'dirty_paths': dirty.splitlines() if dirty is not None else None}


def require_commit(observed, expected):
    if expected is None:
        return
    if not isinstance(expected, str) or not re.fullmatch(r'[0-9a-fA-F]{40}', expected):
        raise ValueError('expected commit must be a full 40-character Git SHA')
    if observed is None or observed.lower() != expected.lower():
        raise ValueError('checkout does not match expected Git commit')
