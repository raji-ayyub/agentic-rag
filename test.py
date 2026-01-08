# test.py

import time
from collections import Counter

from app import TravelAssistant, TravelState


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


# ---------------- RUN TESTS ---------------- #

print("\n🧪 Running Travel Assistant System Tests...\n")

for i, case in enumerate(TEST_CASES, start=1):
    state: TravelState = {
        "question": case["question"],
        "city": case["city"],
        "answer": None,
    }

    start = time.time()

    try:
        result = assistant.run(state)
        elapsed = time.time() - start
        latencies.append(elapsed)

        answer = result["answer"]

        # Infer tool used from answer content (pragmatic approach)
        if "Weather in" in answer:
            used_tool = "get_weather"
        elif "Definition not found" in answer or "document" in answer.lower():
            used_tool = "define_word"
        else:
            used_tool = "web_search"

        tool_usage[used_tool] += 1

        status = "✅ PASS" if used_tool == case["expected_tool"] else "⚠️ TOOL MISMATCH"

        print(f"[{i}] {status}")
        print(f"   Question: {case['question']}")
        print(f"   Expected Tool: {case['expected_tool']}")
        print(f"   Used Tool: {used_tool}")
        print(f"   Latency: {elapsed:.2f}s")
        print(f"   Answer Preview: {answer[:120]}...\n")

    except Exception as e:
        failures += 1
        print(f"[{i}] ❌ FAILURE")
        print(f"   Error: {str(e)}\n")


# ---------------- SUMMARY ---------------- #

print("\n📊 TEST SUMMARY")
print("-" * 40)

total = len(TEST_CASES)
avg_latency = sum(latencies) / len(latencies) if latencies else 0

print(f"Total Tests Run: {total}")
print(f"Failures: {failures}")
print(f"Average Latency: {avg_latency:.2f}s")

print("\nTool Usage Breakdown:")
for tool, count in tool_usage.items():
    print(f"  - {tool}: {count}")

print("\n✅ Testing complete.\n")
