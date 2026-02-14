import time
import zipfile
from pathlib import Path

from src.logging.logger import get_logger


def _get_source_dir(storage: str) -> Path:
    return Path("cloud_storage") if storage == "cloud" else Path("backups")


def run_restore(storage: str = "local", filename: str | None = None) -> None:
    logger = get_logger()
    start_ts = time.time()

    logger.info(f"Restore START (storage={storage}, file={filename})")

    try:
        source_dir = _get_source_dir(storage)
        if not source_dir.exists():
            raise FileNotFoundError(f"Quelle existiert nicht: {source_dir}")

        # Datei wählen
        if filename:
            backup_zip = source_dir / filename
            if not backup_zip.exists():
                raise FileNotFoundError(f"Backup nicht gefunden: {backup_zip}")
        else:
            files = sorted(source_dir.glob("*.zip"))
            if not files:
                raise FileNotFoundError("Keine Backups gefunden.")
            backup_zip = files[-1]

        restore_dir = Path("restore")
        restore_dir.mkdir(exist_ok=True)

        with zipfile.ZipFile(backup_zip, "r") as zf:
            zf.extractall(restore_dir)

        duration = round(time.time() - start_ts, 2)
        logger.info(f"Restore SUCCESS ({duration}s) <- {backup_zip}")
        print(f"Restore abgeschlossen: {backup_zip} -> {restore_dir}")

    except Exception as e:
        duration = round(time.time() - start_ts, 2)
        logger.error(f"Restore FAIL ({duration}s) - {type(e).__name__}: {e}")
        print(f"Restore fehlgeschlagen: {e}")
