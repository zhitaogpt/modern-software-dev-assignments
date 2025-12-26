import subprocess
import sys
from pathlib import Path

def run_tests(target=None):
    repo_root = Path(__file__).resolve().parents[2]
    week5_dir = repo_root / "week5"
    
    cmd = ["pytest"]
    
    if target == "notes":
        cmd.append("backend/tests/test_notes.py")
    elif target == "action_items":
        cmd.append("backend/tests/test_action_items.py")
    elif target == "extract":
        cmd.append("backend/tests/test_extract.py")
    else:
        cmd.append("backend/tests/")
    
    print(f"Running command: {' '.join(cmd)}")
    import os
    env = os.environ.copy()
    env["PYTHONPATH"] = str(week5_dir)
    result = subprocess.run(cmd, cwd=week5_dir, env=env)
    return result.returncode

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    exit_code = run_tests(target)
    sys.exit(exit_code)
