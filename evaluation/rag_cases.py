RAG_CASES = [

    {
        "id": "RAG-G01",
        "question": "Can a support ticket be closed without customer confirmation?",
        "expected_answer": "No. A ticket should only be closed after the issue is resolved and the customer has confirmed the resolution.",
    },

    {
        "id": "RAG-G02",
        "question": "What are the valid ticket statuses?",
        "expected_answer": "OPEN, IN_PROGRESS, RESOLVED, and CLOSED.",
    },

    {
        "id": "RAG-G03",
        "question": "When can a refund be initiated?",
        "expected_answer": "A refund can be initiated when the customer was incorrectly charged or the service was not delivered.",
    },

    {
        "id": "RAG-G04",
        "question": "When does a refund require supervisor approval?",
        "expected_answer": "Refunds above $500 require supervisor approval.",
    },

    {
        "id": "RAG-G05",
        "question": "What should the agent do with a security incident?",
        "expected_answer": "A security incident should be escalated and passwords, tokens, and API keys must not be exposed.",
    },
    
    {
        "id": "RAG-G06",
        "question": "What is our internal policy for employee cryptocurrency reimbursements?",
        "expected_answer": "The internal knowledge base does not contain sufficient information."
    },
    {
        "id": "RAG-G07",
        "question": "What should I do if a customer sends an API key?",
        "expected_answer": "The security incident should be escalated and secrets such as API keys must not be exposed."
    },
]