import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

LOG = Path("logs/squad.log")
INDEX = Path("web/index.html")

AGENTES = {
    "chefe": ("Prefeitura (Chefe)", "Delega, confere e registra"),
    "produto": ("Produto", "Requisitos e backlog"),
    "arquiteto": ("Arquiteto", "Decisões e ADRs"),
    "dados": ("Dados", "Modelo de dados"),
    "design": ("Design", "Estados e animações"),
    "testes": ("Testes", "Casos de teste"),
}
EQUIPE = ("produto", "arquiteto", "dados", "design", "testes")
EVENTOS_PUBLICOS = {"delegou", "respondeu", "aguardando_aprovacao", "aprovado", "negado"}


def ler_eventos() -> list[dict]:
    if not LOG.exists():
        return []
    eventos = []
    for linha in LOG.read_text(encoding="utf-8").splitlines():
        try:
            eventos.append(json.loads(linha))
        except json.JSONDecodeError:
            continue
    return eventos


def estado_de(agente: str, eventos: list[dict]) -> dict:
    ultimo = None
    for i, e in enumerate(eventos):
        if e.get("evento") == "delegou" and e.get("para") == agente:
            ultimo = i
    if ultimo is None:
        return {"estado": "ocioso", "tarefa": "", "hora": ""}

    delegou = eventos[ultimo]
    depois = eventos[ultimo + 1:]
    resposta = next(
        (e for e in depois if e.get("evento") == "respondeu" and e.get("id") == delegou.get("id")),
        None,
    )
    estado = "trabalhando"
    if resposta:
        status = resposta.get("status")
        if status == "erro":
            estado = "erro"
        elif status == "ok":
            estado = "concluido"
        else:
            estado = "aguardando_aprovacao"
            for e in depois[depois.index(resposta) + 1:]:
                if e.get("de") == agente and e.get("evento") == "aprovado":
                    estado = "concluido"
                if e.get("de") == agente and e.get("evento") == "negado":
                    estado = "negado"
    return {
        "estado": estado,
        "tarefa": (delegou.get("tarefa") or "")[:80],
        "hora": (delegou.get("hora") or "")[11:19],
    }


def listar_entregas() -> list[dict]:
    arquivos = list(Path("docs/adr").glob("*.md")) + list(Path("docs").glob("*.md"))
    arquivos.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return [
        {
            "arquivo": p.name,
            "hora": datetime.fromtimestamp(p.stat().st_mtime).strftime("%H:%M:%S"),
        }
        for p in arquivos[:8]
    ]


def montar_estado() -> dict:
    eventos = ler_eventos()
    agentes = []
    for chave in EQUIPE:
        nome, papel = AGENTES[chave]
        agentes.append({"id": chave, "nome": nome, "papel": papel, **estado_de(chave, eventos)})

    ocupado = any(a["estado"] in ("trabalhando", "aguardando_aprovacao") for a in agentes)
    concluidos = sum(1 for a in agentes if a["estado"] == "concluido")
    nome, papel = AGENTES["chefe"]
    if ocupado:
        estado_chefe, tarefa_chefe = "trabalhando", "Coordenando o Squad Algo"
    elif concluidos:
        estado_chefe, tarefa_chefe = "concluido", f"Rodada concluída: {concluidos} agentes entregaram"
    else:
        estado_chefe, tarefa_chefe = "ocioso", ""
    chefe = {
        "id": "chefe", "nome": nome, "papel": papel,
        "estado": estado_chefe, "tarefa": tarefa_chefe, "hora": "",
    }

    atividade = []
    for e in reversed(eventos[-10:]):
        if e.get("evento") in EVENTOS_PUBLICOS:
            atividade.append({
                "hora": (e.get("hora") or "")[11:19],
                "evento": e["evento"],
                "agente": e.get("para") or e.get("de", ""),
            })
    return {"agentes": [chefe] + agentes, "atividade": atividade, "entregas": listar_entregas()}


class Handler(BaseHTTPRequestHandler):
    def _enviar(self, codigo: int, tipo: str, corpo: bytes) -> None:
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self) -> None:
        rota = self.path.split("?")[0]
        if rota == "/api/estado":
            corpo = json.dumps(montar_estado(), ensure_ascii=False).encode("utf-8")
            return self._enviar(200, "application/json; charset=utf-8", corpo)
        if rota in ("/", "/index.html") and INDEX.exists():
            return self._enviar(200, "text/html; charset=utf-8", INDEX.read_bytes())
        self._enviar(404, "text/plain; charset=utf-8", b"nao encontrado")

    def log_message(self, *args) -> None:
        pass


if __name__ == "__main__":
    servidor = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Cidade em http://127.0.0.1:8000  (Ctrl+C para parar)")
    servidor.serve_forever()