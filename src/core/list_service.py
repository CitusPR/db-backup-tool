from pathlib import Path

def run_list():
    backup_dir = Path("backups")
    files = sorted(backup_dir.glob("*.zip"))

    if not files:
        print("Keine Backups gefunden.")
        return

    print("Vorhandene Backups:")
    for f in files:
        size_kb = f.stat().st_size / 1024
        print(f"- {f.name}  ({size_kb:.1f} KB)")
