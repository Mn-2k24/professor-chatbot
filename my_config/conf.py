
from decouple import config
from openai import AsyncOpenAI

my_key = config("GEMINI_API_KEY")

client = AsyncOpenAI(api_key=my_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

class GeminiModel:
    def __init__(self, model, openai_client):
        self.model = model
        self.client = openai_client

    async def chat(self, system_message, user_message):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content

MODEL = GeminiModel(model="gemini-2.0-flash", openai_client=client)
