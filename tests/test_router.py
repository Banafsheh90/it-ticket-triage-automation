from src.router import assign_routing_queue


def test_assign_routing_queue_with_known_category():
    tickets = [
        {
            "ticket_id": "1001",
            "category": "Access",
        }
    ]

    routing_rules = {
        "Access": "IAM / Application Administration"
    }

    result = assign_routing_queue(tickets, routing_rules)

    assert result[0]["suggested_queue"] == "IAM / Application Administration"


def test_assign_routing_queue_with_unknown_category():
    tickets = [
        {
            "ticket_id": "1002",
            "category": "Unknown",
        }
    ]

    routing_rules = {
        "Access": "IAM / Application Administration"
    }

    result = assign_routing_queue(tickets, routing_rules)

    assert result[0]["suggested_queue"] == "Manual Review"