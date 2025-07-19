#!/usr/bin/env python3

from pydantic_ai import Agent


def main():
    agent = Agent(
        "google-gla:gemini-1.5-flash",
        system_prompt=(
            "You are a helpful conversational assistant. "
            "Be friendly, concise, and engaging in your responses. "
            'If the user says "quit", "exit", or "bye", respond with "Goodbye!"'
        ),
    )

    print("🤖 Chat Agent - Type 'quit', 'exit', or 'bye' to exit")
    print("-" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Bot: Goodbye!")
                break

            result = agent.run_sync(user_input)
            print(f"Bot: {result.output}")

        except KeyboardInterrupt:
            print("\nBot: Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue


if __name__ == "__main__":
    main()

