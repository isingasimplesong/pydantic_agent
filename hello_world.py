from pydantic_ai import Agent

agent = Agent(
    "google-gla:gemini-2.5-flash",
    system_prompt="Be creative",
)

result = agent.run_sync("Write a sonnet that basically just says Hello World!")
print(result.output)
