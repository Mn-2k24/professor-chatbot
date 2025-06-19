from agents import Runner
import asyncio
from my_agents.teachers import professor

async def main():
    print("🧠 Talk to Professor! Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        result = await Runner.run(professor, user_input)
        print("Professor:", result.final_output)
        print()

asyncio.run(main())
