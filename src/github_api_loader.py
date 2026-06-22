import requests


GITHUB_API_BASE_URL = "https://api.github.com"


def fetch_repository_issues(owner, repo, state="open", per_page=10):
    """
    Fetch issues from a public GitHub repository using the GitHub REST API.

    Pull requests can also appear in the issues endpoint, so they are filtered out.
    """
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/issues"

    params = {
        "state": state,
        "per_page": per_page,
    }

    try:
        response = requests.get(url, params=params, timeout=10)

    except requests.exceptions.Timeout as error:
        raise ConnectionError(
            "GitHub API request timed out. Please try again later."
        ) from error

    except requests.exceptions.ConnectionError as error:
        raise ConnectionError(
            "Could not connect to GitHub API. Please check your internet connection."
        ) from error

    except requests.exceptions.RequestException as error:
        raise ConnectionError(
            f"GitHub API request failed: {error}"
        ) from error

    if response.status_code == 404:
        raise ValueError(
            f"GitHub repository not found: {owner}/{repo}. "
            "Please check the owner and repository name."
        )

    if response.status_code == 403:
        raise ValueError(
            "GitHub API access was forbidden. This may be caused by rate limits "
            "or missing permissions."
        )

    if response.status_code != 200:
        raise ValueError(
            f"GitHub API request failed with status code {response.status_code}: "
            f"{response.text}"
        )

    issues = response.json()

    if not isinstance(issues, list):
        raise ValueError(
            "Unexpected GitHub API response format. Expected a list of issues."
        )

    real_issues = [
        issue for issue in issues
        if "pull_request" not in issue
    ]

    return real_issues


def get_label_names(issue):
    """
    Extract label names from a GitHub issue.
    """
    return [
        label["name"].lower()
        for label in issue.get("labels", [])
    ]


def map_labels_to_priority(label_names):
    """
    Map GitHub labels to internal ticket priority values.
    """
    if "high" in label_names or "priority: high" in label_names:
        return "High"

    if "medium" in label_names or "priority: medium" in label_names:
        return "Medium"

    if "low" in label_names or "priority: low" in label_names:
        return "Low"

    return "Medium"


def map_labels_to_category(label_names):
    """
    Map GitHub labels to internal ticket category values.
    """
    if "access" in label_names:
        return "Access"

    if "application" in label_names or "bug" in label_names:
        return "Application"

    if "hardware" in label_names:
        return "Hardware"

    if "onboarding" in label_names:
        return "Onboarding"

    if "security" in label_names:
        return "Security"

    if "confluence" in label_names or "documentation" in label_names:
        return "Confluence"

    return "Application"


def map_state_to_status(state):
    """
    Map GitHub issue state to internal ticket status.
    """
    if state == "open":
        return "Open"

    if state == "closed":
        return "Closed"

    return "In Progress"


def normalize_github_issue(issue):
    """
    Convert a GitHub issue object into the internal ticket format used by this project.
    """
    label_names = get_label_names(issue)

    return {
        "ticket_id": f"github-{issue['number']}",
        "created_at": issue["created_at"][:10],
        "category": map_labels_to_category(label_names),
        "priority": map_labels_to_priority(label_names),
        "status": map_state_to_status(issue["state"]),
        "description": issue["title"],
        "requester_department": "GitHub",
    }


def load_tickets_from_github_issues(owner, repo, state="open", per_page=10):
    """
    Load GitHub issues and normalize them into the internal ticket format.
    """
    issues = fetch_repository_issues(owner, repo, state, per_page)

    if not issues:
        return []

    tickets = [
        normalize_github_issue(issue)
        for issue in issues
    ]

    return tickets