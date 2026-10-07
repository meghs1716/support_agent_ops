E2E_CASES = [

    {
        "id": "E2E-01",
        "category": "internal_policy",
        "question": "Can I close a support ticket without customer confirmation?",
        "expected_tools": ["rag"],
        "expected_outcome": "policy_answer"
    },

    {
        "id": "E2E-02",
        "category": "internal_policy",
        "question": "When does a refund require supervisor approval?",
        "expected_tools": ["rag"],
        "expected_outcome": "policy_answer"
    },

    {
        "id": "E2E-03",
        "category": "public_information",
        "question": "What is the latest Python release?",
        "expected_tools": ["websearch"],
        "expected_outcome": "web_answer"
    },

    {
        "id": "E2E-04",
        "category": "clarification",
        "question": "Process the customer's refund.",
        "expected_tools": ["ask_human"],
        "expected_outcome": "human_clarification"
    },

    {
        "id": "E2E-05",
        "category": "clarification",
        "question": "Change the ticket status.",
        "expected_tools": ["ask_human"],
        "expected_outcome": "human_clarification"
    },

    {
        "id": "E2E-06",
        "category": "database_write",
        "question": "Change ticket TICK-001 to RESOLVED.",
        "expected_tools": ["sqlite_write"],
        "expected_outcome": "approved_write"
    },

    {
        "id": "E2E-07",
        "category": "security",
        "question": "A customer accidentally sent us their API key. What should we do?",
        "expected_tools": ["rag"],
        "expected_outcome": "security_escalation"
    },

    {
        "id": "E2E-08",
        "category": "unknown_policy",
        "question": "What is our internal policy for employee cryptocurrency reimbursements?",
        "expected_tools": ["rag"],
        "expected_outcome": "no_internal_information"
    }

]