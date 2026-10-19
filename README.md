# Squad Algo — Cidade de Agentes

Squad de agentes de IA em Python, construído sobre a API do Claude: um chefe que delega, agentes especialistas com uma responsabilidade cada, controle humano sobre ações sensíveis e uma **cidade visual** que mostra o squad trabalhando em tempo real.

## Como funciona

1. O **chefe** recebe um pedido e o delega ao agente de **Produto**, que escreve requisitos e backlog.
2. Se o pedido for ambíguo, o Produto devolve `precisa_aprovacao` e o sistema **para até um humano aprovar** (padrão seguro: qualquer resposta diferente de `s` nega).
3. O **Arquiteto** define a solução e registra a decisão em um **ADR**.
4. Os operadores de **Dados, Design e Testes** rodam **em paralelo** e entregam documentos.
5. A **cidade** lê o log e mostra o estado de cada agente (ocioso, trabalhando, aguardando aprovação, concluído, erro, negado).

## Arquitetura

```
chefe.py              delega, registra o log e controla a aprovação humana
agents/
  produto.py          requisitos e backlog
  arquiteto.py        decisões e ADRs
  operador.py         dados, design e testes (mesmo molde, missões diferentes)
harness/
  contrato.py         Mensagem e Resposta validadas (Pydantic)
  llm.py              único ponto de contato com a LLM
servidor.py + web/    cidade em tempo real (lê o log, só leitura)
docs/                 ADRs, backlog e documentos gerados pelo squad
```

## Decisões de projeto

- **Permissões no código, não só no prompt.** Cada agente só devolve texto; quem grava arquivos é o código, e apenas em pastas definidas (`docs/adr/`, `docs/backlog.md`, `docs/<área>.md`).
- **Contrato validado.** Toda comunicação usa `Mensagem` e `Resposta`, com status `ok`, `erro` ou `precisa_aprovacao`.
- **LLM isolada.** Trocar de modelo ou de fornecedor significa alterar um único arquivo (`harness/llm.py`).
- **Aprovação humana com padrão de negar** em ações sensíveis.
- **Auditoria.** Cada evento fica registrado em `logs/squad.log` (JSON por linha).
- **Sanitização na interface.** A cidade só recebe agente, papel, estado, tarefa resumida e hora; nunca contexto, resultado ou credenciais.

## Como rodar

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # preencha a sua chave no .env
python servidor.py          # terminal 1 → http://127.0.0.1:8000
python chefe.py             # terminal 2
```

Variáveis do `.env`: `ANTHROPIC_API_KEY`, `MODELO` e, se a sua chave não estiver vinculada a um workspace, `ANTHROPIC_WORKSPACE_ID`.

> Nunca envie o arquivo `.env` ao GitHub. Ele já está no `.gitignore`.

## Status e próximos passos

Projeto em desenvolvimento. O agente de Testes apontou uma lacuna no contrato atual: falta um status próprio para **negação** e **timeout** da aprovação humana.

- [ ] Status de negação e timeout no contrato
- [ ] Agente que gera código, com aprovação humana
- [ ] QA e documentação de APIs
- [ ] Execução em Docker e em VPS com permissões limitadas

## Autor

Artur Leandro Gonçalves