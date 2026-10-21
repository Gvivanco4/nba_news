from anthropic import Anthropic
import os
from dotenv import load_dotenv
import json

load_dotenv()

class LLM:
    def __init__(self, client):
        self.__client = client

    def prompt_ai(self, data):
        response = self.__client.messages.create(
            system=(
                "Preserve the original JSON structure and the attributes "
                "and values of retained items. "
                "Return only valid JSON. "
                "Do not include Markdown, code fences, or explanations."
            ),
            model="claude-sonnet-5-5",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"Filter the provided NBA data to include only news about "
                            f"Stats, Games, Records. Avoid news like: Starting 5: Finishing the preseason in style, NBA milestones to watch this season, etc."
                            f"{json.dumps(data, ensure_ascii=False)}",
            }],
        )

        text = "".join(
            block.text
            for block in response.content
            if block.type == "text"
        )

        return json.loads(text)

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

ai_caller = LLM(client)


    

    
