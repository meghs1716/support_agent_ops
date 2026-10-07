def normalize(text):
    return (
        text.lower()
        .replace(",", "")
        .replace(".", "")
        .replace("$", "")
        .replace("-", " ")
        .strip()
    )


def contains_any(text, phrases):
    return any(
        phrase in text
        for phrase in phrases
    )


def check_grounding(case_id, answer):

    answer = normalize(answer)

    checks = {

        "RAG-G01": [
            ["customer confirmation", "customer confirmed"],
            ["resolved", "issue is resolved"]
        ],

        "RAG-G02": [
            ["open"],
            ["in_progress", "in progress"],
            ["resolved"],
            ["closed"]
        ],

        "RAG-G03": [
            ["incorrectly charged", "incorrect charge", "charged incorrectly"],
            ["service was not delivered", "service not delivered", "service was not provided"]
        ],

        "RAG-G04": [
            ["500"],
            ["supervisor approval", "supervisor"]
        ],

        "RAG-G05": [
            ["security incident", "security"],
            ["escalated", "escalate"],
            ["password"],
            ["token"],
            ["api key", "apikey"]
        ]
    }

    required_groups = checks.get(case_id)

    if not required_groups:
        return False

    matched = 0

    for group in required_groups:

        if contains_any(answer, group):
            matched += 1

    score = matched / len(required_groups)

    return score >= 0.75