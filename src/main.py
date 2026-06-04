from csv_loader import load_tickets_from_csv
from validator import validate_tickets


def main():
    try:
        tickets = load_tickets_from_csv("data/sample_tickets.csv")
        validate_tickets(tickets)

    except FileNotFoundError as error:
        print(f"File error: {error}")
        return

    except ValueError as error:
        print(error)
        return

    print("\nIT Ticket Triage Automation")
    print("----------------------------")
    print(f"Loaded and validated tickets: {len(tickets)}\n")

    for ticket in tickets:
        print(
            f"{ticket['ticket_id']} | "
            f"{ticket['priority']} | "
            f"{ticket['category']} | "
            f"{ticket['status']} | "
            f"{ticket['description']}"
        )


if __name__ == "__main__":
    main()