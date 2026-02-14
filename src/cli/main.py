import argparse

from src.core.backup_service import run_backup
from src.core.restore_service import run_restore
from src.core.list_service import run_list


def main():
    parser = argparse.ArgumentParser(description="DB Backup Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # BACKUP
    backup_parser = subparsers.add_parser("backup", help="Erstellt ein Backup")
    backup_parser.add_argument(
        "--type",
        choices=["full", "incremental", "differential"],
        default="full",
        help="Backup-Typ (default: full)"
    )
    backup_parser.add_argument(
        "--storage",
        choices=["local", "cloud"],
        default="local",
        help="Speicherziel (default: local)"
    )

    # RESTORE
    restore_parser = subparsers.add_parser("restore", help="Stellt ein Backup wieder her")
    restore_parser.add_argument(
        "--storage",
        choices=["local", "cloud"],
        default="local",
        help="Quelle (default: local)"
    )
    restore_parser.add_argument(
        "--file",
        default=None,
        help="Optional: Dateiname der ZIP (sonst latest)"
    )

    # LIST
    subparsers.add_parser("list", help="Listet vorhandene Backups auf")

    args = parser.parse_args()

    if args.command == "backup":
        run_backup(backup_type=args.type, storage=args.storage)

    elif args.command == "restore":
        run_restore(storage=args.storage, filename=args.file)

    elif args.command == "list":
        run_list()


if __name__ == "__main__":
    main()
