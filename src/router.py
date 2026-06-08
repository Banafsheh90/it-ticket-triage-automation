import json
from pathlib import Path


def load_routing_rules(file_path):
    """
    Load category-based routing rules from a JSON configuration file.

    Example:
    {
        "Access": "IAM / Application Administration",
        "Application": "Application Support"
    }
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Routing rules file not found: {file_path}")

    with path.open(mode="r", encoding="utf-8") as rules_file:
        routing_rules = json.load(rules_file)

    return routing_rules


def assign_routing_queue(tickets, routing_rules):
    """
    Add a suggested_queue field to each ticket based on its category.

    If a category is not found in the routing rules, the ticket is assigned
    to 'Manual Review'.
    """
    routed_tickets = []

    for ticket in tickets:
        category = ticket["category"]
        suggested_queue = routing_rules.get(category, "Manual Review")

        routed_ticket = ticket.copy()
        routed_ticket["suggested_queue"] = suggested_queue

        routed_tickets.append(routed_ticket)

    return routed_tickets