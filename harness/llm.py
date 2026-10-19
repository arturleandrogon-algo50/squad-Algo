import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODELO = os.getenv("MODELO", "claude-sonnet-5-5")

_client = anthropic.Anthropic(
    default_headers={"anthropic-workspace-id": os.getenv("ANTHROPIC_WORKSPACE_ID")}
)


def perguntar(system: str, usuario: str, max_tokens: int = 4000) -> str:
    """Único ponto de contato com a LLM."""
    resposta = _client.messages.create(
        model=MODELO,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": usuario}],
    )
    return "".join(b.text for b in resposta.content if b.type == "text")