TEST_CASES = [

    # ============================================================
    # RAG — INTERNAL KNOWLEDGE
    # ============================================================

    {
        "id": "RAG-01",
        "category": "rag",
        "question": "What are the allowed statuses for a support ticket?",
        "expected_tool": "rag"
    },

    {
        "id": "RAG-02",
        "category": "rag",
        "question": "When can a support ticket be closed?",
        "expected_tool": "rag"
    },

    {
        "id": "RAG-03",
        "category": "rag",
        "question": "When does a refund require supervisor approval?",
        "expected_tool": "rag"
    },

    {
        "id": "RAG-04",
        "category": "rag",
        "question": "A customer was incorrectly charged. What does our internal policy say about refunds?",
        "expected_tool": "rag"
    },

    {
        "id": "RAG-05",
        "category": "rag",
        "question": "What should support do if a customer sends us an API key?",
        "expected_tool": "rag"
    },

    {
        "id": "RAG-06",
        "category": "rag",
        "question": "When should a support issue be escalated according to our internal procedures?",
        "expected_tool": "rag"
    },

    {
        "id": "RAG-07",
        "category": "rag",
        "question": "What does our internal documentation say about resolving a ticket before closing it?",
        "expected_tool": "rag"
    },


    # ============================================================
    # WEB — PUBLIC / CURRENT INFORMATION
    # ============================================================

    {
        "id": "WEB-01",
        "category": "websearch",
        "question": "What is the latest stable version of Python?",
        "expected_tool": "websearch"
    },

    {
        "id": "WEB-02",
        "category": "websearch",
        "question": "What is the current latest version of PostgreSQL?",
        "expected_tool": "websearch"
    },

    {
        "id": "WEB-03",
        "category": "websearch",
        "question": "What is the latest stable release of FastAPI?",
        "expected_tool": "websearch"
    },

    {
        "id": "WEB-04",
        "category": "websearch",
        "question": "Find the current official documentation for LangGraph.",
        "expected_tool": "websearch"
    },

    {
        "id": "WEB-05",
        "category": "websearch",
        "question": "What does the latest Python documentation recommend for creating virtual environments?",
        "expected_tool": "websearch"
    },


    # ============================================================
    # HUMAN — MISSING / AMBIGUOUS INFORMATION
    # ============================================================

    {
        "id": "HUMAN-01",
        "category": "clarification",
        "question": "Process the customer's refund.",
        "expected_tool": "ask_human"
    },

    {
        "id": "HUMAN-02",
        "category": "clarification",
        "question": "Change the ticket status.",
        "expected_tool": "ask_human"
    },

    {
        "id": "HUMAN-03",
        "category": "clarification",
        "question": "Update the customer's support ticket.",
        "expected_tool": "ask_human"
    },

    {
        "id": "HUMAN-04",
        "category": "clarification",
        "question": "Close the ticket for me.",
        "expected_tool": "ask_human"
    },

    {
        "id": "HUMAN-05",
        "category": "clarification",
        "question": "Please change the ticket to the correct status.",
        "expected_tool": "ask_human"
    },


    # ============================================================
    # SQLITE WRITE — EXPLICIT DATABASE MODIFICATION
    # ============================================================

    {
        "id": "WRITE-01",
        "category": "write",
        "question": "Change ticket TICK-001 to RESOLVED.",
        "expected_tool": "sqlite_write"
    },

    {
        "id": "WRITE-02",
        "category": "write",
        "question": "Update TICK-001 with the note 'Customer confirmed the issue is resolved'.",
        "expected_tool": "sqlite_write"
    },

    {
        "id": "WRITE-03",
        "category": "write",
        "question": "Set TICK-001 to IN_PROGRESS and add the note 'Investigation started'.",
        "expected_tool": "sqlite_write"
    },

    {
        "id": "WRITE-04",
        "category": "write",
        "question": "Modify TICK-001 so its status is OPEN.",
        "expected_tool": "sqlite_write"
    },

    {
        "id": "WRITE-05",
        "category": "write",
        "question": "Record on TICK-001 that the customer confirmed the issue has been resolved.",
        "expected_tool": "sqlite_write"
    },


    # ============================================================
    # NO TOOL — CONVERSATIONAL / GENERAL
    # ============================================================

    {
        "id": "NONE-01",
        "category": "no_tool",
        "question": "Hello, can you help me?",
        "expected_tool": None
    },

    {
        "id": "NONE-02",
        "category": "no_tool",
        "question": "Thanks, that solved my problem.",
        "expected_tool": None
    },

    {
        "id": "NONE-03",
        "category": "no_tool",
        "question": "Explain in simple terms what a support ticket is.",
        "expected_tool": None
    },

    {
        "id": "NONE-04",
        "category": "no_tool",
        "question": "What is the difference between a question and a support request?",
        "expected_tool": None
    },


    # ============================================================
    # CROSS-TOOL / ADVERSARIAL CASES
    # ============================================================

    # Looks like a database operation because a ticket ID is present,
    # but the user is asking about policy.
    {
        "id": "CROSS-01",
        "category": "cross_tool",
        "question": "Can TICK-001 be closed without customer confirmation?",
        "expected_tool": "rag"
    },

    # Looks like an internal-policy question because it mentions
    # company security, but the user asks about a public standard.
    {
        "id": "CROSS-02",
        "category": "cross_tool",
        "question": "What does the current OWASP guidance recommend for handling exposed API keys?",
        "expected_tool": "websearch"
    },

    # Looks like a refund-policy question, but the user is asking
    # to perform an action without giving enough information.
    {
        "id": "CROSS-03",
        "category": "cross_tool",
        "question": "The customer says they were charged incorrectly. Give them the refund.",
        "expected_tool": "ask_human"
    },

    # Looks like a policy question because it mentions resolution,
    # but the user explicitly requests a database modification.
    {
        "id": "CROSS-04",
        "category": "cross_tool",
        "question": "The customer confirmed the issue is resolved, so update TICK-001 to CLOSED.",
        "expected_tool": "sqlite_write"
    },
]