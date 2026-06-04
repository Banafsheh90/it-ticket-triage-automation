from csv_loader import load_tickets_from_csv


def main():
    tickets = load_tickets_from_csv("data/sample_tickets.csv")

    print("\nIT Ticket Triage Automation")
    print("----------------------------")
    print(f"Loaded tickets: {len(tickets)}\n")

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