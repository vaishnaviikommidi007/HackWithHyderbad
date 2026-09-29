from memory import recall_context

print("Testing Hindsight...")

try:
    result = recall_context(
        "demo-team",
        "team coding standards and review feedback"
    )

    print("SUCCESS")
    print("Number of memories:", len(result))

    for memory in result:
        print(memory)

except Exception as e:
    print("FAILED")
    print(type(e).__name__)
    print(str(e))