import sys
from pathlib import Path

# Load `PROJECT_ROOT/` into `sys.path` for easy import
base_import_dir = Path(__file__).resolve().parents[2]

if base_import_dir not in sys.path:
    sys.path.append(str(base_import_dir))
