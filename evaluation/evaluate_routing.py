from agent.graph import agent
from evaluation.test_cases import TEST_CASES
import uuid
from evaluation.reset_database import reset_database
def get_tool_calls(result):
    """
    Extract tool names called by the agent.
    """

    tool_calls = []

    for message in result["messages"]:

        if not hasattr(message, "tool_calls"):
            continue

        for tool_call in message.tool_calls:
            tool_calls.append(tool_call["name"])

    return tool_calls


def evaluate_case(test_case):

    print("\n" + "=" * 60)
    print("TEST:", test_case["id"])
    print("QUESTION:", test_case["question"])

   

    config = {
        "configurable": {
            "thread_id": f"evaluation-{test_case['id']}-{uuid.uuid4()}"
        }
    }

    try:

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": test_case["question"]
                    }
                ]
            },
            config=config
        )

        tools_used = get_tool_calls(result)

        expected_tool = test_case["expected_tool"]

        print("Expected:", expected_tool)
        print("Tools used:", tools_used)

        if expected_tool is None:
            
            passed = len(tools_used) == 0
        else:
            passed = tools_used==[expected_tool]
        if passed:
            print("RESULT: PASS")
            return True

        print("RESULT: FAIL")
        return False

    except Exception as e:

        print("ERROR:", type(e).__name__)
        print(e)

        return False


def main():
    reset_database()
    passed = 0
    total = len(TEST_CASES)

    for test_case in TEST_CASES:

        if evaluate_case(test_case):
            passed += 1

    accuracy = (passed / total) * 100

    print("\n" + "=" * 60)
    print("FINAL EVALUATION")
    print("=" * 60)

    print(f"Passed: {passed}/{total}")
    print(f"Tool Selection Accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    main()