# test.py

import time
from collections import Counter
from typing import Optional

from app import TravelAssistant
from langchain_core.messages import ToolMessage


assistant = TravelAssistant()


# ---------------- TEST CASES ---------------- #

TEST_CASES = [
    {
        "question": "What is the weather in Paris?",
        "city": "Paris",
        "expected_tool": "get_weather",
    },
    {
        "question": "Define passport",
        "city": None,
        "expected_tool": "define_word",
    },
    {
        "question": "Is it safe to travel to Lagos?",
        "city": None,
        "expected_tool": "web_search",
    },
    {
        "question": "Best travel route from Abuja to Accra",
        "city": None,
        "expected_tool": "web_search",
    },
    {
        "question": "Weather condition in Tokyo today",
        "city": "Tokyo",
        "expected_tool": "get_weather",
    },
    {
        "question": "Meaning of visa",
        "city": None,
        "expected_tool": "define_word",
    },
]


# ---------------- METRICS ---------------- #

latencies = []
tool_usage = Counter()
failures = 0
tool_mismatches = 0


# ---------------- HELPERS ---------------- #

def extract_tool_used(messages) -> Optional[str]:
    """
    Extract the first tool used from LangGraph messages.
    """
    for msg in messages:
        if isinstance(msg, ToolMessage):
            return msg.name
    return None


# ---------------- RUN TESTS ---------------- #

print("\n🧪 Running Travel Assistant System Tests...\n")

for i, case in enumerate(TEST_CASES, start=1):
    start = time.time()

    try:
        result = assistant.run(
            {
                "question": case["question"],
                "city": case["city"],
            }
        )

        elapsed = time.time() - start
        latencies.append(elapsed)

        answer = result.get("answer", "")
        messages = result.get("messages", [])

        used_tool = extract_tool_used(messages)
        expected_tool = case["expected_tool"]

        if used_tool:
            tool_usage[used_tool] += 1

        if used_tool == expected_tool:
            status = "✅ PASS"
        else:
            status = "⚠️ TOOL MISMATCH"
            tool_mismatches += 1

        print(f"[{i}] {status}")
        print(f"   Question       : {case['question']}")
        print(f"   Expected Tool  : {expected_tool}")
        print(f"   Used Tool      : {used_tool}")
        print(f"   Latency        : {elapsed:.2f}s")
        print(f"   Answer Preview : {answer[:120]}...\n")

    except Exception as e:
        failures += 1
        print(f"[{i}] ❌ FAILURE")
        print(f"   Error: {str(e)}\n")


# ---------------- SUMMARY ---------------- #

print("\n📊 TEST SUMMARY")
print("-" * 45)

total = len(TEST_CASES)
avg_latency = sum(latencies) / len(latencies) if latencies else 0

print(f"Total Tests Run      : {total}")
print(f"Failures             : {failures}")
print(f"Tool Mismatches      : {tool_mismatches}")
print(f"Average Latency      : {avg_latency:.2f}s")

print("\nTool Usage Breakdown:")
for tool, count in tool_usage.items():
    print(f"  - {tool}: {count}")

print("\n✅ Testing complete.\n")
