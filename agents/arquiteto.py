import json
import re
import unicodedata
from pathlib import Path

from harness.contrato import Mensagem, Resposta
from harness.llm import perguntar

PASTA_ADR = Path("docs/adr")

SYSTEM = """Você é o ARQUITETO de software do Squad Algo.
Sua função: decidir como o sistema é organizado e registrar a decisão em um ADR.

PADRÕES PERMITIDOS (use somente estes): SOLID; separação em camadas
(agentes / harness / interface); contratos em JSON validados;
um agente = uma responsabilidade.
Se precisar de um padrão fora da lista, não o use: cite em "alternativas"
e marque "precisa_aprovacao" como true.
CONTRATOS EXISTENTES (respeite-os; não crie formatos paralelos):
- Mensagem: id, de, para, tarefa, contexto.
- Resposta: id, de, status (ok | erro | precisa_aprovacao), resultado, motivo.
Quando a decisão envolver aprovação humana, use o status "precisa_aprovacao".

ESTILO: uma decisão por ADR, no máximo 4 itens em "decisao".
Se o tema exigir mais, registre o restante em "consequencias" como próximos ADRs.
REGRAS:
- Você só decide e documenta. Não escreve código de produção, não executa
  comandos e não acessa segredos.
- Responda SOMENTE com um JSON válido, sem texto fora dele, neste formato:
{"titulo": "...", "contexto": "...", "decisao": "...",
 "alternativas": ["..."], "consequencias": ["..."], "precisa_aprovacao": false}
- Use "precisa_aprovacao": true se a decisão mudar um contrato já existente.
- Escreva em português, de forma curta e objetiva."""


def _extrair_json(texto: str) -> dict:
    texto = re.sub(r"^```(?:json)?|```$", "", texto.strip(), flags=re.MULTILINE)
    return json.loads(texto.strip())


def _slug(titulo: str) -> str:
    ascii_ = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_.lower()).strip("-")[:50] or "decisao"


def _salvar_adr(adr: dict) -> str:
    PASTA_ADR.mkdir(parents=True, exist_ok=True)
    numero = len(list(PASTA_ADR.glob("*.md"))) + 1
    caminho = PASTA_ADR / f"{numero:04d}-{_slug(adr['titulo'])}.md"
    alternativas = "\n".join(f"- {a}" for a in adr.get("alternativas", []))
    consequencias = "\n".join(f"- {c}" for c in adr.get("consequencias", []))
    caminho.write_text(
        f"# ADR {numero:04d}: {adr['titulo']}\n\n"
        f"## Contexto\n{adr['contexto']}\n\n"
        f"## Decisão\n{adr['decisao']}\n\n"
        f"## Alternativas consideradas\n{alternativas}\n\n"
        f"## Consequências\n{consequencias}\n",
        encoding="utf-8",
    )
    return str(caminho)


def executar(msg: Mensagem) -> Resposta:
    pedido = (
        f"Tarefa: {msg.tarefa}\n"
        f"Contexto: {json.dumps(msg.contexto, ensure_ascii=False)}"
    )
    try:
        adr = _extrair_json(perguntar(SYSTEM, pedido))
        caminho = _salvar_adr(adr)
    except Exception as erro:
        return Resposta(id=msg.id, de="arquiteto", status="erro", motivo=str(erro))

    status = "precisa_aprovacao" if adr.get("precisa_aprovacao") else "ok"
    return Resposta(
        id=msg.id,
        de="arquiteto",
        status=status,
        resultado={"adr": caminho, "decisao": adr["decisao"]},
    )