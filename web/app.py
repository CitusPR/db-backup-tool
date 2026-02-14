from pathlib import Path
from flask import Flask, render_template, redirect, url_for, request

from src.core.backup_service import run_backup
from src.core.restore_service import run_restore

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

LAST_ACTION = ""


def collect_backups():
    items = []

    for storage_name, folder in [("local", Path("backups")), ("cloud", Path("cloud_storage"))]:
        if folder.exists():
            for f in sorted(folder.glob("*.zip")):
                items.append({
                    "name": f.name,
                    "storage": storage_name,
                    "size_kb": round(f.stat().st_size / 1024, 1)
                })

    items.sort(key=lambda x: x["name"], reverse=True)
    return items


@app.get("/")
def home():
    return render_template(
        "index.html",
        backups=collect_backups(),
        last_action=LAST_ACTION
    )


@app.post("/backup")
def backup():
    global LAST_ACTION
    backup_type = request.form.get("type", "full")
    storage = request.form.get("storage", "local")

    run_backup(backup_type=backup_type, storage=storage)
    LAST_ACTION = f"Backup: type={backup_type}, storage={storage}"

    return redirect(url_for("home"))


@app.post("/restore")
def restore():
    global LAST_ACTION
    storage = request.form.get("storage", "local")

    run_restore(storage=storage, filename=None)
    LAST_ACTION = f"Restore: latest, storage={storage}"

    return redirect(url_for("home"))


@app.get("/refresh")
def refresh():
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
