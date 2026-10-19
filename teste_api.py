import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(
    default_headers={"anthropic-workspace-id": os.getenv("ANTHROPIC_WORKSPACE_ID")}
)

resposta = client.messages.create(
    model=os.getenv("MODELO", "claude-sonnet-5-5"),
    max_tokens=200,
    messages=[{"role": "user", "content": "Diga olá em uma frase, como chefe do Squad Algo."}],
)

print(resposta.content[0].text)