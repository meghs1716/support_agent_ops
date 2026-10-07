import json
from pathlib import Path
from collections import Counter


TRACE_DIR = Path(__file__).resolve().parent / "traces"


def load_traces():

    traces = []

    for file in TRACE_DIR.glob("*.json"):

        try:

            with open(file, "r", encoding="utf-8") as f:
                traces.append(json.load(f))

        except Exception as e:

            print(f"Could not read {file.name}: {e}")

    return traces


def main():

    traces = load_traces()

    print("\n" + "=" * 60)
    print("AGENT TRACE REPORT")
    print("=" * 60)

    if not traces:
        print("\nNo traces found.")
        print("Run the agent to generate trace files.")
        return

    print(f"\nTotal runs: {len(traces)}")

    status_counts = Counter(
        trace.get("status", "unknown")
        for trace in traces
    )

    print("\nStatuses:")

    for status, count in status_counts.items():
        print(f"  {status}: {count}")

    tool_counts = Counter()

    for trace in traces:

        for tool in trace.get("tool_calls", []):

            tool_name = tool.get("name")

            if tool_name:
                tool_counts[tool_name] += 1

    print("\nTools used:")

    if tool_counts:

        for tool, count in tool_counts.most_common():
            print(f"  {tool}: {count}")

    else:

        print("  No tools recorded.")

    print("\nRecent runs:")

    for trace in traces[-10:]:

        print("\n---")

        print("Time:", trace.get("timestamp"))

        print(
            "Question:",
            trace.get("question")
        )

        tools = [
            tool.get("name")
            for tool in trace.get("tool_calls", [])
        ]

        print("Tools:", tools)

        print(
            "Status:",
            trace.get("status")
        )


if __name__ == "__main__":
    main()