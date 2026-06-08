import json
from datetime import datetime
from pathlib import Path


def load_sla_rules(file_path):
    """
    Load SLA rules from a JSON configuration file.

    Example:
    {
        "High": 1,
        "Medium": 3,
        "Low": 5
    }
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"SLA rules file not found: {file_path}")

    with path.open(mode="r", encoding="utf-8") as rules_file:
        sla_rules = json.load(rules_file)

    return sla_rules


def calculate_ticket_age_days(created_at, reference_date=None):
    """
    Calculate how many days a ticket has been open.

    If no reference date is provided, today's date is used.
    A fixed reference date can be passed for testing or demo purposes.
    """
    if reference_date is None:
        reference_date = datetime.today()

    created_date = datetime.strptime(created_at, "%Y-%m-%d")
    ticket_age = reference_date - created_date

    return ticket_age.days


def add_sla_risk_status(tickets, sla_rules, reference_date=None):
    """
    Add SLA-related fields to each ticket:
    - ticket_age_days
    - sla_limit_days
    - sla_risk
    """
    tickets_with_sla = []

    for ticket in tickets:
        priority = ticket["priority"]
        created_at = ticket["created_at"]

        ticket_age_days = calculate_ticket_age_days(created_at, reference_date)
        sla_limit_days = sla_rules.get(priority)

        ticket_with_sla = ticket.copy()
        ticket_with_sla["ticket_age_days"] = ticket_age_days
        ticket_with_sla["sla_limit_days"] = sla_limit_days

        if ticket["status"] == "Closed":
            ticket_with_sla["sla_risk"] = "No"
        elif sla_limit_days is None:
            ticket_with_sla["sla_risk"] = "Manual Review"
        elif ticket_age_days > sla_limit_days:
            ticket_with_sla["sla_risk"] = "Yes"
        else:
            ticket_with_sla["sla_risk"] = "No"

        tickets_with_sla.append(ticket_with_sla)

    return tickets_with_sla