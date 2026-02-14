import time
import zipfile
from datetime import datetime
from pathlib import Path

from src.logging.logger import get_logger


def _get_target_dir(storage: str) -> Path:
    return Path("cloud_storage") if storage == "cloud" else Path("backups")


def run_backup(backup_type: str = "full", storage: str = "local") -> None:
    logger = get_logger()
    start_ts = time.time()

    logger.info(f"Backup START (type={backup_type}, storage={storage})")

    try:
        target_dir = _get_target_dir(storage)
        target_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        txt_path = target_dir / f"backup_{backup_type}_{timestamp}.txt"

        # Simulierte Datenmenge je Typ (MVP)
        if backup_type == "full":
            content = "FULL BACKUP\n" + ("X" * 20000)
        elif backup_type == "differential":
            content = "DIFFERENTIAL BACKUP\n" + ("X" * 8000)
        else:  # incremental
            content = "INCREMENTAL BACKUP\n" + ("X" * 2000)

        # Dummy-"Dump" schreiben
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(content)

        # ZIP erstellen
        zip_path = target_dir / f"backup_{backup_type}_{timestamp}.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(txt_path, arcname=txt_path.name)

        # TXT löschen -> nur ZIP behalten
        txt_path.unlink(missing_ok=True)

        duration = round(time.time() - start_ts, 2)
        logger.info(f"Backup SUCCESS ({duration}s) -> {zip_path}")
        print(f"Backup erstellt: {zip_path}")

        # Optional: Notification (Simulation)
        print("Slack Notification: gesendet (Simulation)")

    except Exception as e:
        duration = round(time.time() - start_ts, 2)
        logger.error(f"Backup FAIL ({duration}s) - {type(e).__name__}: {e}")
        print(f"Backup fehlgeschlagen: {e}")
