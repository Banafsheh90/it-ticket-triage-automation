from datetime import datetime

from csv_loader import load_tickets_from_csv
from validator import validate_tickets
from router import load_routing_rules, assign_routing_queue
from sla_checker import load_sla_rules, add_sla_risk_status
from summary import generate_ticket_summary


def main():
    try:
        tickets = load_tickets_from_csv("data/sample_tickets.csv")
        validate_tickets(tickets)

        routing_rules = load_routing_rules("config/routing_rules.json")
        routed_tickets = assign_routing_queue(tickets, routing_rules)

        sla_rules = load_sla_rules("config/sla_rules.json")

        reference_date = datetime.strptime("2026-05-12", "%Y-%m-%d")
        analyzed_tickets = add_sla_risk_status(
            routed_tickets,
            sla_rules,
            reference_date
        )

        summary = generate_ticket_summary(analyzed_tickets)

    except FileNotFoundError as error:
        print(f"File error: {error}")
        return

    except ValueError as error:
        print(error)
        return

    print("\nIT Ticket Triage Automation")
    print("----------------------------")
    print(f"Loaded, validated, routed, and analyzed tickets: {len(analyzed_tickets)}\n")

    print("Summary")
    print("-------")
    print(f"Total tickets: {summary['total_tickets']}")
    print(f"Open tickets: {summary['open_tickets']}")
    print(f"Closed tickets: {summary['closed_tickets']}")
    print(f"High priority tickets: {summary['high_priority_tickets']}")
    print(f"Tickets at SLA risk: {summary['sla_risk_tickets']}\n")

    print("Tickets by category:")
    for category, count in summary["tickets_by_category"].items():
        print(f"- {category}: {count}")

    print("\nTickets by priority:")
    for priority, count in summary["tickets_by_priority"].items():
        print(f"- {priority}: {count}")

    print("\nTickets by suggested queue:")
    for queue, count in summary["tickets_by_queue"].items():
        print(f"- {queue}: {count}")

    print("\nDetailed tickets")
    print("----------------")

    for ticket in analyzed_tickets:
        print(
            f"{ticket['ticket_id']} | "
            f"{ticket['priority']} | "
            f"{ticket['category']} | "
            f"{ticket['status']} | "
            f"{ticket['suggested_queue']} | "
            f"Age: {ticket['ticket_age_days']} days | "
            f"SLA limit: {ticket['sla_limit_days']} days | "
            f"SLA risk: {ticket['sla_risk']} | "
            f"{ticket['description']}"
        )


if __name__ == "__main__":
    main()