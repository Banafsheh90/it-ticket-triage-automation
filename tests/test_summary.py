from src.summary import generate_ticket_summary


def test_generate_ticket_summary():
    tickets = [
        {
            "ticket_id": "1001",
            "category": "Access",
            "priority": "High",
            "status": "Open",
            "suggested_queue": "IAM / Application Administration",
            "sla_risk": "Yes",
        },
        {
            "ticket_id": "1002",
            "category": "Application",
            "priority": "Medium",
            "status": "Closed",
            "suggested_queue": "Application Support",
            "sla_risk": "No",
        },
        {
            "ticket_id": "1003",
            "category": "Access",
            "priority": "Low",
            "status": "Open",
            "suggested_queue": "IAM / Application Administration",
            "sla_risk": "No",
        },
    ]

    summary = generate_ticket_summary(tickets)

    assert summary["total_tickets"] == 3
    assert summary["open_tickets"] == 2
    assert summary["closed_tickets"] == 1
    assert summary["high_priority_tickets"] == 1
    assert summary["sla_risk_tickets"] == 1

    assert summary["tickets_by_category"]["Access"] == 2
    assert summary["tickets_by_priority"]["High"] == 1
    assert summary["tickets_by_queue"]["IAM / Application Administration"] == 2