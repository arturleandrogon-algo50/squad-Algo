import json
import re
from pathlib import Path

from harness.contrato import Mensagem, Resposta
from harness.llm import perguntar

BACKLOG = Path("docs/backlog.md")

SYSTEM = """Você é o agente de PRODUTO do Squad Algo.
Sua função: transformar o pedido do usuário em requisitos claros, com critérios
de pronto, e manter o backlog priorizado. Você cuida do "o quê" e do "porquê";
a arquitetura ("como") é do arquiteto.

REGRAS:
- Não decide arquitetura, não escreve código, não executa comandos e não
  acessa segredos.
- Se o pedido for ambíguo ou aumentar o escopo do projeto, use
  "precisa_aprovacao": true e explique em "alertas".
- Responda SOMENTE com um JSON válido neste formato:
{"requisito": "...", "criterios_de_aceite": ["..."], "prioridade": "alta|media|baixa",
 "tarefas": ["..."], "alertas": ["..."], "precisa_aprovacao": false}
- No máximo 5 critérios e 6 tarefas. Escreva em português, curto e objetivo."""


def _extrair_json(texto: str) -> dict:
    texto = re.sub(r"^```(?:json)?|```$", "", texto.strip(), flags=re.MULTILINE)
    return json.loads(texto.strip())


def _salvar_backlog(item: dict) -> str:
    BACKLOG.parent.mkdir(parents=True, exist_ok=True)
    criterios = "\n".join(f"  - [ ] {c}" for c in item.get("criterios_de_aceite", []))
    tarefas = "\n".join(f"  - {t}" for t in item.get("tarefas", []))
    with open(BACKLOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            f"\n## {item['requisito']} (prioridade: {item.get('prioridade', 'media')})\n"
            f"- Critérios de aceite:\n{criterios}\n"
            f"- Tarefas:\n{tarefas}\n"
        )
    return str(BACKLOG)


def executar(msg: Mensagem) -> Resposta:
    pedido = (
        f"Pedido: {msg.tarefa}\n"
        f"Contexto: {json.dumps(msg.contexto, ensure_ascii=False)}"
    )
    try:
        item = _extrair_json(perguntar(SYSTEM, pedido))
        caminho = _salvar_backlog(item)
    except Exception as erro:
        return Resposta(id=msg.id, de="produto", status="erro", motivo=str(erro))

    status = "precisa_aprovacao" if item.get("precisa_aprovacao") else "ok"
    return Resposta(
        id=msg.id,
        de="produto",
        status=status,
        resultado={**item, "backlog": caminho},
        motivo="; ".join(item.get("alertas", [])),
    )