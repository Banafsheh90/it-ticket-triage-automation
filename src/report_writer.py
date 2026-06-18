import csv
import json
from pathlib import Path


def ensure_output_directory(output_dir):
    """
    Create the output directory if it does not already exist.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)


def write_summary_to_json(summary, file_path):
    """
    Write the ticket summary dictionary to a JSON file.
    """
    path = Path(file_path)
    ensure_output_directory(path.parent)

    with path.open(mode="w", encoding="utf-8") as json_file:
        json.dump(summary, json_file, indent=4)


def write_high_priority_tickets_to_csv(tickets, file_path):
    """
    Write high-priority tickets to a CSV file.
    """
    path = Path(file_path)
    ensure_output_directory(path.parent)

    high_priority_tickets = [
        ticket for ticket in tickets
        if ticket["priority"] == "High"
    ]

    fieldnames = [
        "ticket_id",
        "created_at",
        "category",
        "priority",
        "status",
        "suggested_queue",
        "ticket_age_days",
        "sla_limit_days",
        "sla_risk",
        "description",
        "requester_department",
    ]

    with path.open(mode="w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for ticket in high_priority_tickets:
            writer.writerow({
                field: ticket.get(field, "")
                for field in fieldnames
            })


def write_text_summary(summary, file_path):
    """
    Write a human-readable summary report to a text file.
    """
    path = Path(file_path)
    ensure_output_directory(path.parent)

    lines = [
        "IT Ticket Triage Automation Report",
        "===================================",
        "",
        f"Total tickets: {summary['total_tickets']}",
        f"Open tickets: {summary['open_tickets']}",
        f"Closed tickets: {summary['closed_tickets']}",
        f"High priority tickets: {summary['high_priority_tickets']}",
        f"Tickets at SLA risk: {summary['sla_risk_tickets']}",
        "",
        "Tickets by category:",
    ]

    for category, count in summary["tickets_by_category"].items():
        lines.append(f"- {category}: {count}")

    lines.append("")
    lines.append("Tickets by priority:")

    for priority, count in summary["tickets_by_priority"].items():
        lines.append(f"- {priority}: {count}")

    lines.append("")
    lines.append("Tickets by suggested queue:")

    for queue, count in summary["tickets_by_queue"].items():
        lines.append(f"- {queue}: {count}")

    with path.open(mode="w", encoding="utf-8") as text_file:
        text_file.write("\n".join(lines))