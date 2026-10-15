from src.graph import build_graph


def main() -> None:
    graph = build_graph()
    print("\nLangGraph Benchmark Study — demo application")
    print("Ask a question, or type 'exit' to stop.")
    print("Tip: set OPENAI_API_KEY to use a hosted model; otherwise demo mode is used.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not question:
            continue

        result = graph.invoke({"question": question})
        print(f"\nRoute: {result.get('route', 'unknown')}")
        print(f"Answer: {result.get('final_answer', result.get('draft_answer', 'No answer produced.'))}")
        if result.get("verification_note"):
            print(f"Verification note: {result['verification_note']}")
        print()


if __name__ == "__main__":
    main()
