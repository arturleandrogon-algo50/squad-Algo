import json
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from agents import arquiteto, operador, produto
from harness.contrato import Mensagem, Resposta

AGENTES = {
    "produto": produto.executar,
    "arquiteto": arquiteto.executar,
    "dados": operador.criar("dados"),
    "design": operador.criar("design"),
    "testes": operador.criar("testes"),
}

_trava = threading.Lock()


def registrar(evento: dict) -> None:
    Path("logs").mkdir(exist_ok=True)
    evento["hora"] = datetime.now().isoformat(timespec="seconds")
    with _trava:
        with open("logs/squad.log", "a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(evento, ensure_ascii=False) + "\n")


def delegar(msg: Mensagem) -> Resposta:
    registrar({"evento": "delegou", **msg.model_dump()})
    agente = AGENTES.get(msg.para)
    if agente is None:
        resposta = Resposta(
            id=msg.id, de="chefe", status="erro", motivo=f"agente desconhecido: {msg.para}"
        )
    else:
        resposta = agente(msg)
    registrar({"evento": "respondeu", **resposta.model_dump()})
    return resposta


def pedir_aprovacao(resposta: Resposta) -> bool:
    """Portão de aprovação humana. Padrão seguro: qualquer coisa diferente de 's' nega."""
    registrar({"evento": "aguardando_aprovacao", "de": resposta.de, "motivo": resposta.motivo})
    print(f"\n[{resposta.de}] pede aprovação: {resposta.motivo or 'sem detalhes'}")
    aprovado = input("Aprovar? (s/n): ").strip().lower() == "s"
    registrar({"evento": "aprovado" if aprovado else "negado", "de": resposta.de})
    return aprovado


if __name__ == "__main__":
    pedido_usuario = "Quero uma cidade visual que mostre meus agentes trabalhando em tempo real."

    r1 = delegar(Mensagem(de="chefe", para="produto", tarefa=pedido_usuario))
    print(r1.model_dump_json(indent=2))
    if r1.status == "erro":
        raise SystemExit("Produto falhou.")
    if r1.status == "precisa_aprovacao" and not pedir_aprovacao(r1):
        raise SystemExit("Negado pelo usuário.")

    r2 = delegar(
        Mensagem(
            de="chefe",
            para="arquiteto",
            tarefa="Definir como a cidade visual lê o log dos agentes e mostra o estado de cada um.",
            contexto={"requisitos": r1.resultado},
        )
    )
    print(r2.model_dump_json(indent=2))
    if r2.status == "erro":
        raise SystemExit("Arquiteto falhou.")
    if r2.status == "precisa_aprovacao" and not pedir_aprovacao(r2):
        raise SystemExit("Negado pelo usuário.")

    equipe = [
        ("dados", "Definir o modelo de dados dos eventos do log que a cidade lê."),
        ("design", "Definir estados, cores e animações da cidade para cada estado dos agentes."),
        ("testes", "Definir os casos de teste do portão de aprovação humana do harness."),
    ]
    contexto = {"decisao_arquitetura": r2.resultado.get("decisao", "")}
    with ThreadPoolExecutor(max_workers=3) as pool:
        futuros = [
            pool.submit(delegar, Mensagem(de="chefe", para=a, tarefa=t, contexto=contexto))
            for a, t in equipe
        ]
        resultados = [f.result() for f in futuros]

    for r in resultados:
        print(r.model_dump_json(indent=2))
        if r.status == "precisa_aprovacao" and not pedir_aprovacao(r):
            print(f"{r.de}: negado, seguindo sem ele.")