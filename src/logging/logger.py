import logging
from pathlib import Path

def get_logger():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("dbbackup")
    logger.setLevel(logging.INFO)

    # Wichtig: nicht doppelt Handler hinzufügen
    if not logger.handlers:
        file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
