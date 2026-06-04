import csv
from pathlib import Path


def load_tickets_from_csv(file_path):
    """
    Load ticket data from a CSV file and return it as a list of dictionaries.

    Each row in the CSV becomes one dictionary.
    Example:
    {
        "ticket_id": "1001",
        "created_at": "2026-05-01",
        "category": "Access",
        ...
    }
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    tickets = []

    with path.open(mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            tickets.append(row)

    return tickets