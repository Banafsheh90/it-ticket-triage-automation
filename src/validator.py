from datetime import datetime


REQUIRED_FIELDS = [
    "ticket_id",
    "created_at",
    "category",
    "priority",
    "status",
    "description",
    "requester_department",
]

VALID_PRIORITIES = ["High", "Medium", "Low"]
VALID_STATUSES = ["Open", "Closed", "In Progress"]


def validate_tickets(tickets):
    """
    Validate ticket data loaded from CSV.

    Checks:
    - Dataset is not empty
    - Required fields exist
    - Priority values are accepted
    - Status values are accepted
    - created_at follows YYYY-MM-DD format
    """
    if not tickets:
        raise ValueError("No tickets found. The CSV file is empty.")

    validation_errors = []

    for row_number, ticket in enumerate(tickets, start=2):
        missing_fields = [
            field for field in REQUIRED_FIELDS
            if field not in ticket or ticket[field].strip() == ""
        ]

        if missing_fields:
            validation_errors.append(
                f"Row {row_number}: Missing required fields: {', '.join(missing_fields)}"
            )
            continue

        if ticket["priority"] not in VALID_PRIORITIES:
            validation_errors.append(
                f"Row {row_number}: Invalid priority '{ticket['priority']}'. "
                f"Expected one of: {', '.join(VALID_PRIORITIES)}"
            )

        if ticket["status"] not in VALID_STATUSES:
            validation_errors.append(
                f"Row {row_number}: Invalid status '{ticket['status']}'. "
                f"Expected one of: {', '.join(VALID_STATUSES)}"
            )

        try:
            datetime.strptime(ticket["created_at"], "%Y-%m-%d")
        except ValueError:
            validation_errors.append(
                f"Row {row_number}: Invalid created_at date '{ticket['created_at']}'. "
                "Expected format: YYYY-MM-DD"
            )

    if validation_errors:
        error_message = "Ticket validation failed:\n" + "\n".join(validation_errors)
        raise ValueError(error_message)

    return True