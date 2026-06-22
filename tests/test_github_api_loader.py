from src.github_api_loader import (
    map_labels_to_priority,
    map_labels_to_category,
    map_state_to_status,
)


def test_map_labels_to_priority_high():
    labels = ["access", "priority: high"]

    result = map_labels_to_priority(labels)

    assert result == "High"


def test_map_labels_to_priority_default_medium():
    labels = ["access"]

    result = map_labels_to_priority(labels)

    assert result == "Medium"


def test_map_labels_to_category_security():
    labels = ["security", "priority: high"]

    result = map_labels_to_category(labels)

    assert result == "Security"


def test_map_state_to_status_open():
    result = map_state_to_status("open")

    assert result == "Open"


def test_map_state_to_status_closed():
    result = map_state_to_status("closed")

    assert result == "Closed"