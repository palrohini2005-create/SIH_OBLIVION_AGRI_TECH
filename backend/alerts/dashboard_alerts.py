def get_alert_summary(alerts):
    summary = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for alert in alerts:
        severity = alert.get("alert_severity", "LOW")

        if severity in summary:
            summary[severity] += 1

    return summary


def sort_alerts_by_priority(alerts):
    priority = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1
    }

    return sorted(
        alerts,
        key=lambda alert: priority.get(
            alert.get("alert_severity", "LOW"), 1
        ),
        reverse=True
    )