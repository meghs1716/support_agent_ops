from agent.graph import agent
from evaluation.rag_cases import RAG_CASES
from evaluation.rag_grounding import check_grounding


def extract_text(content):

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))

            elif isinstance(item, str):
                parts.append(item)

        return "\n".join(parts)

    return str(content)


def evaluate_case(case):

    print("\n" + "=" * 60)
    print("TEST:", case["id"])
    print("QUESTION:", case["question"])

    config = {
        "configurable": {
            "thread_id": f"rag-grounding-{case['id']}"
        }
    }

    try:

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": case["question"]
                    }
                ]
            },
            config=config
        )

        final_message = result["messages"][-1]

        answer = extract_text(final_message.content)

        passed = check_grounding(
            case["id"],
            answer
        )

        print("\nAGENT ANSWER:")
        print(answer)

        print("\nRESULT:", "PASS" if passed else "FAIL")

        return passed

    except Exception as e:

        print("\nERROR:")
        print(type(e).__name__)
        print(e)

        return False


def main():

    passed = 0
    total = len(RAG_CASES)

    for case in RAG_CASES:

        if evaluate_case(case):
            passed += 1

    accuracy = (passed / total) * 100

    print("\n" + "=" * 60)
    print("RAG GROUNDING EVALUATION")
    print("=" * 60)

    print(f"Passed: {passed}/{total}")
    print(f"Grounding Accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    main()