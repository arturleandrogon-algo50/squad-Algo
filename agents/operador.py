import json
import re
from pathlib import Path

from harness.contrato import Mensagem, Resposta
from harness.llm import perguntar

PASTA = Path("docs")

CONFIG = {
    "dados": {
        "nome": "DADOS",
        "missao": "Definir o modelo de dados dos eventos do log (campos, tipos e exemplos) usado pelo harness e pela cidade.",
    },
    "design": {
        "nome": "DESIGN",
        "missao": "Definir o design da cidade visual: estados, cores, animações e acessibilidade.",
    },
    "testes": {
        "nome": "TESTES",
        "missao": "Definir casos de teste do harness (aprovar, negar, timeout, resposta inválida), com o resultado esperado de cada um.",
    },
}

MODELO_SYSTEM = """Você é o agente de {nome} do Squad Algo.
Sua missão: {missao}

REGRAS:
- Você só propõe e documenta. Não escreve código de produção, não executa
  comandos e não acessa segredos.
- Siga os contratos existentes: Mensagem (id, de, para, tarefa, contexto) e
  Resposta (id, de, status: ok | erro | precisa_aprovacao, resultado, motivo).
- Responda SOMENTE com um JSON válido neste formato:
{{"titulo": "...", "itens": ["..."], "alertas": ["..."], "precisa_aprovacao": false}}
- No máximo 6 itens, curtos e objetivos. Escreva em português."""


def _extrair_json(texto: str) -> dict:
    texto = re.sub(r"^```(?:json)?|```$", "", texto.strip(), flags=re.MULTILINE)
    return json.loads(texto.strip())


def _salvar(chave: str, dados: dict) -> str:
    PASTA.mkdir(parents=True, exist_ok=True)
    caminho = PASTA / f"{chave}.md"
    itens = "\n".join(f"- {i}" for i in dados.get("itens", []))
    alertas = "\n".join(f"- {a}" for a in dados.get("alertas", []))
    texto = f"# {dados['titulo']}\n\n## Itens\n{itens}\n"
    if alertas:
        texto += f"\n## Alertas\n{alertas}\n"
    caminho.write_text(texto, encoding="utf-8")
    return str(caminho)


def criar(chave: str):
    system = MODELO_SYSTEM.format(**CONFIG[chave])

    def executar(msg: Mensagem) -> Resposta:
        pedido = (
            f"Tarefa: {msg.tarefa}\n"
            f"Contexto: {json.dumps(msg.contexto, ensure_ascii=False)}"
        )
        try:
            dados = _extrair_json(perguntar(system, pedido))
            caminho = _salvar(chave, dados)
        except Exception as erro:
            return Resposta(id=msg.id, de=chave, status="erro", motivo=str(erro))
        status = "precisa_aprovacao" if dados.get("precisa_aprovacao") else "ok"
        return Resposta(
            id=msg.id,
            de=chave,
            status=status,
            resultado={"titulo": dados["titulo"], "arquivo": caminho},
            motivo="; ".join(dados.get("alertas", [])),
        )

    return executar