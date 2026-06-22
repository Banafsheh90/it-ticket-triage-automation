from datetime import datetime

from src.sla_checker import calculate_ticket_age_days, add_sla_risk_status


def test_calculate_ticket_age_days():
    reference_date = datetime.strptime("2026-05-12", "%Y-%m-%d")

    result = calculate_ticket_age_days("2026-05-10", reference_date)

    assert result == 2


def test_add_sla_risk_status_for_open_ticket_over_limit():
    tickets = [
        {
            "ticket_id": "1001",
            "created_at": "2026-05-01",
            "priority": "High",
            "status": "Open",
        }
    ]

    sla_rules = {"High": 1}
    reference_date = datetime.strptime("2026-05-12", "%Y-%m-%d")

    result = add_sla_risk_status(tickets, sla_rules, reference_date)

    assert result[0]["ticket_age_days"] == 11
    assert result[0]["sla_limit_days"] == 1
    assert result[0]["sla_risk"] == "Yes"


def test_add_sla_risk_status_for_closed_ticket():
    tickets = [
        {
            "ticket_id": "1007",
            "created_at": "2026-05-07",
            "priority": "Low",
            "status": "Closed",
        }
    ]

    sla_rules = {"Low": 5}
    reference_date = datetime.strptime("2026-05-12", "%Y-%m-%d")

    result = add_sla_risk_status(tickets, sla_rules, reference_date)

    assert result[0]["sla_risk"] == "No"