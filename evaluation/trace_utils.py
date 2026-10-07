def get_tool_calls(result):

    tool_calls = []

    for message in result.get("messages", []):

        if not hasattr(message, "tool_calls"):
            continue

        for tool_call in message.tool_calls:

            tool_calls.append({
                "name": tool_call.get("name"),
                "arguments": tool_call.get("args", {})
            })

    return tool_calls