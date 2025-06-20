class Agent:
    def __init__(self, name, instructions, model):
        self.name = name
        self.instructions = instructions
        self.model = model

    async def run(self, message):
        return await self.model.chat(self.instructions, message)

class Runner:
    @staticmethod
    async def run(agent, message):
        return await agent.run(message)
