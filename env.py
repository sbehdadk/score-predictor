# env.py
import sys
from pathlib import Path

# Add the project root to sys.path
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent
sys.path.append(str(project_root))
