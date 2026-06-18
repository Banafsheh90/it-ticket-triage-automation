def count_by_field(tickets, field_name):
    """
    Count how many tickets exist for each value in a specific field.

    Example:
    field_name = "category"

    Result:
    {
        "Access": 2,
        "Application": 2,
        "Hardware": 2
    }
    """
    counts = {}

    for ticket in tickets:
        field_value = ticket.get(field_name, "Unknown")
        counts[field_value] = counts.get(field_value, 0) + 1

    return counts


def generate_ticket_summary(tickets):
    """
    Generate summary statistics for analyzed tickets.
    """
    total_tickets = len(tickets)

    open_tickets = 0
    closed_tickets = 0
    high_priority_tickets = 0
    sla_risk_tickets = 0

    for ticket in tickets:
        if ticket["status"] == "Open":
            open_tickets += 1

        if ticket["status"] == "Closed":
            closed_tickets += 1

        if ticket["priority"] == "High":
            high_priority_tickets += 1

        if ticket["sla_risk"] == "Yes":
            sla_risk_tickets += 1

    summary = {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "closed_tickets": closed_tickets,
        "high_priority_tickets": high_priority_tickets,
        "sla_risk_tickets": sla_risk_tickets,
        "tickets_by_category": count_by_field(tickets, "category"),
        "tickets_by_priority": count_by_field(tickets, "priority"),
        "tickets_by_queue": count_by_field(tickets, "suggested_queue"),
    }

    return summary