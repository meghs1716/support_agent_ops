from agent.graph import agent
from evaluation.e2e_cases import E2E_CASES
from evaluation.trace_utils import get_tool_calls
from evaluation.logger import log_trace


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


def run_case(case):

    print("\n" + "=" * 70)
    print("TEST:", case["id"])
    print("CATEGORY:", case["category"])
    print("QUESTION:", case["question"])

    config = {
        "configurable": {
            "thread_id": f"e2e-{case['id']}"
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

        tool_calls = get_tool_calls(result)

        tools_used = [
            call["name"]
            for call in tool_calls
        ]

        final_message = result["messages"][-1]

        answer = extract_text(
            final_message.content
        )

        expected_tools = case["expected_tools"]

        correct_tool = any(
            tool in tools_used
            for tool in expected_tools
        )

        print("\nExpected tools:", expected_tools)
        print("Tools used:", tools_used)

        print("\nAgent answer:")
        print(answer)

        print(
            "\nRouting:",
            "PASS" if correct_tool else "FAIL"
        )

        log_trace(
            question=case["question"],
            tool_calls=tool_calls,
            final_answer=answer,
            status="completed"
        )

        return correct_tool

    except Exception as e:

        print("\nERROR:")
        print(type(e).__name__)
        print(e)

        return False


def main():

    passed = 0

    total = len(E2E_CASES)

    for case in E2E_CASES:

        if run_case(case):
            passed += 1

    accuracy = (
        passed / total
    ) * 100

    print("\n" + "=" * 70)
    print("END-TO-END EVALUATION")
    print("=" * 70)

    print(f"Passed: {passed}/{total}")
    print(f"Routing Success: {accuracy:.2f}%")


if __name__ == "__main__":
    main()