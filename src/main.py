from datetime import datetime

from csv_loader import load_tickets_from_csv
from validator import validate_tickets
from router import load_routing_rules, assign_routing_queue
from sla_checker import load_sla_rules, add_sla_risk_status
from summary import generate_ticket_summary
from report_writer import (
    write_summary_to_json,
    write_high_priority_tickets_to_csv,
    write_text_summary,
)


TICKET_DATA_FILE = "data/sample_tickets.csv"
ROUTING_RULES_FILE = "config/routing_rules.json"
SLA_RULES_FILE = "config/sla_rules.json"

SUMMARY_JSON_OUTPUT = "output/ticket_summary.json"
HIGH_PRIORITY_CSV_OUTPUT = "output/high_priority_tickets.csv"
TEXT_SUMMARY_OUTPUT = "output/summary.txt"

DEMO_REFERENCE_DATE = datetime.strptime("2026-05-12", "%Y-%m-%d")


def load_and_analyze_tickets():
    """
    Load tickets, validate the input data, apply routing rules,
    calculate SLA risk, and generate summary statistics.
    """
    tickets = load_tickets_from_csv(TICKET_DATA_FILE)
    validate_tickets(tickets)

    routing_rules = load_routing_rules(ROUTING_RULES_FILE)
    routed_tickets = assign_routing_queue(tickets, routing_rules)

    sla_rules = load_sla_rules(SLA_RULES_FILE)
    analyzed_tickets = add_sla_risk_status(
        routed_tickets,
        sla_rules,
        DEMO_REFERENCE_DATE
    )

    summary = generate_ticket_summary(analyzed_tickets)

    return analyzed_tickets, summary


def write_reports(analyzed_tickets, summary):
    """
    Write structured reports to the output folder.
    """
    write_summary_to_json(summary, SUMMARY_JSON_OUTPUT)
    write_high_priority_tickets_to_csv(
        analyzed_tickets,
        HIGH_PRIORITY_CSV_OUTPUT
    )
    write_text_summary(summary, TEXT_SUMMARY_OUTPUT)


def print_summary_section(summary):
    """
    Print the summary statistics in a readable terminal format.
    """
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


def print_detailed_tickets(analyzed_tickets):
    """
    Print analyzed ticket details in a readable terminal format.
    """
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


def main():
    try:
        analyzed_tickets, summary = load_and_analyze_tickets()
        write_reports(analyzed_tickets, summary)

    except FileNotFoundError as error:
        print(f"File error: {error}")
        return

    except ValueError as error:
        print(error)
        return

    print("\nIT Ticket Triage Automation")
    print("----------------------------")
    print(f"Loaded, validated, routed, and analyzed tickets: {len(analyzed_tickets)}")
    print("Reports generated in the output folder.\n")

    print_summary_section(summary)
    print_detailed_tickets(analyzed_tickets)


if __name__ == "__main__":
    main()