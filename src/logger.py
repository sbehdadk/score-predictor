import os
import logging
from pathlib import Path
from datetime import datetime

log_dir = os.getenv("LOG_DIR", "/tmp/logs")
log_dir_path = Path(log_dir)
log_dir_path.mkdir(parents=True, exist_ok=True)
current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

subfolder_path = log_dir_path / current_time
subfolder_path.mkdir(parents=True, exist_ok=True)


log_file_path = subfolder_path / f"{current_time}.log"

logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
