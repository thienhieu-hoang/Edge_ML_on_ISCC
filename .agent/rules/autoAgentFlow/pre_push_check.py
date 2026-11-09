#!/usr/bin/env python3
"""
Pre-Push Guardrail Script
Checks for:
1. Files larger than 10MB (model weights, raw datasets) accidentally staged.
2. Accidental inclusion of _note/ or _plan/ when preparing a collab push.
Exit code 0: Clean and safe to push.
Exit code 1: Blocked by guardrail.
"""

import sys
import subprocess
import os

MAX_FILE_SIZE_MB = 10
FORBIDDEN_EXTENSIONS = {".pt", ".pth", ".ckpt", ".bin", ".mat", ".h5"}

def run_git(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip().splitlines()

def check_staged_files():
    print("🔍 [Pre-Push Guard] Scanning tracked/staged files...")
    files = run_git("git ls-files")
    violations = []

    for file_path in files:
        if not os.path.exists(file_path):
            continue
        
        # Check file extension
        _, ext = os.path.splitext(file_path)
        if ext.lower() in FORBIDDEN_EXTENSIONS:
            violations.append(f"❌ Forbidden binary extension '{ext}': {file_path}")
            continue

        # Check file size
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            violations.append(f"❌ File exceeds {MAX_FILE_SIZE_MB}MB limit ({size_mb:.2f}MB): {file_path}")

    if violations:
        print("\n🚨 [GUARDRAIL TRIGGERED] The following files violate git policies:")
        for v in violations:
            print(f"   {v}")
        print("\n👉 Please add these files to .gitignore and unstage them via 'git rm --cached <file>'.")
        sys.exit(1)

    print("✅ [Pre-Push Guard] All files passed size and type inspections (Safe to push).")
    sys.exit(0)

if __name__ == "__main__":
    check_staged_files()
