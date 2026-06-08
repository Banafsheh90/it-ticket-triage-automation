from csv_loader import load_tickets_from_csv
from validator import validate_tickets
from router import load_routing_rules, assign_routing_queue


def main():
    try:
        tickets = load_tickets_from_csv("data/sample_tickets.csv")
        validate_tickets(tickets)

        routing_rules = load_routing_rules("config/routing_rules.json")
        routed_tickets = assign_routing_queue(tickets, routing_rules)

    except FileNotFoundError as error:
        print(f"File error: {error}")
        return

    except ValueError as error:
        print(error)
        return

    print("\nIT Ticket Triage Automation")
    print("----------------------------")
    print(f"Loaded, validated, and routed tickets: {len(routed_tickets)}\n")

    for ticket in routed_tickets:
        print(
            f"{ticket['ticket_id']} | "
            f"{ticket['priority']} | "
            f"{ticket['category']} | "
            f"{ticket['status']} | "
            f"{ticket['suggested_queue']} | "
            f"{ticket['description']}"
        )


if __name__ == "__main__":
    main()