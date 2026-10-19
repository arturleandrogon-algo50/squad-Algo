
## Criar uma visualização em formato de 'cidade' na qual cada agente do Squad Algo seja representado de forma visual e mostre, em tempo real, o que está fazendo (ocioso, trabalhando, aguardando aprovação, com erro), para que o usuário acompanhe o andamento do trabalho de forma intuitiva. (prioridade: media)
- Critérios de aceite:
  - [ ] Cada agente do Squad Algo aparece na cidade com identificação clara (nome e papel)
  - [ ] O estado de cada agente (ocioso, trabalhando, aguardando aprovação, erro) é visível e diferenciado visualmente
  - [ ] As mudanças de estado aparecem na tela em poucos segundos, sem recarregar a página
  - [ ] Ao selecionar um agente, o usuário vê a tarefa atual e as últimas atividades
  - [ ] A visualização não expõe segredos, credenciais nem dados sensíveis dos agentes
- Tarefas:
  - Definir com o usuário a lista de agentes e os estados que devem ser exibidos
  - Definir quais informações de cada agente podem ser mostradas (tarefa atual, histórico, etc.)
  - Definir o que significa 'tempo real' (atraso máximo aceitável de atualização)
  - Descrever o MVP: uma cena simples com um elemento visual por agente e seu estado
  - Encaminhar ao arquiteto a avaliação de viabilidade e da fonte dos eventos de atividade dos agentes
  - Registrar no backlog melhorias futuras (animações, prédios por função, histórico, sons)

## Criar uma visualização em formato de cidade que represente cada agente do Squad Algo como um elemento visual (ex.: prédio ou personagem) e mostre, em tempo real, o que cada um está fazendo, para que o usuário acompanhe o trabalho de forma intuitiva e rápida. (prioridade: media)
- Critérios de aceite:
  - [ ] Cada agente do Squad Algo aparece na cidade com identificação clara (nome e papel).
  - [ ] O estado de cada agente (ocioso, trabalhando, aguardando aprovação, erro) é exibido visualmente e se atualiza sem recarregar a página.
  - [ ] Ao selecionar um agente, o usuário vê a tarefa atual e as últimas atividades dele.
  - [ ] A atualização de um estado aparece na tela em poucos segundos após o evento acontecer (meta de latência a ser definida com o usuário).
  - [ ] A visualização é somente leitura e não exibe segredos, credenciais ou dados sensíveis.
- Tarefas:
  - Alinhar com o usuário o que significa 'tempo real' (latência aceitável) e quais informações mostrar por agente.
  - Definir a lista de estados e eventos dos agentes que a cidade deve refletir.
  - Definir o estilo visual desejado (2D simples, pixel art, isométrico) e referências.
  - Escrever as histórias de usuário da versão mínima (MVP): cidade com agentes e estados.
  - Solicitar ao arquiteto a abordagem técnica e a viabilidade de obter os eventos dos agentes.
  - Priorizar no backlog melhorias futuras (histórico, animações, métricas).

## Criar uma visualização em formato de 'cidade' em que cada agente do Squad Algo aparece como um elemento visual (prédio, personagem ou área) e seu estado de trabalho é mostrado em tempo real, para que o usuário acompanhe de relance quem está fazendo o quê. (prioridade: media)
- Critérios de aceite:
  - [ ] Cada agente do Squad Algo é representado por um elemento visual identificável (nome e ícone ou posição própria na cidade).
  - [ ] O estado de cada agente (ocioso, trabalhando, aguardando aprovação, erro) é exibido de forma visualmente distinta.
  - [ ] As mudanças de estado aparecem na tela em até alguns segundos, sem recarregar a página.
  - [ ] Ao selecionar um agente, o usuário vê a tarefa atual e as últimas atividades dele.
  - [ ] A visualização exibe apenas dados de status e atividade, sem expor segredos, credenciais ou conteúdo sensível.
- Tarefas:
  - Confirmar com o usuário o estilo visual desejado (2D simples, pixel art, isométrico etc.) e onde será exibida (navegador, painel local).
  - Definir a lista de estados de agente e as informações mostradas por agente (tarefa atual, histórico recente).
  - Definir o que significa 'tempo real' (atraso máximo aceitável de atualização).
  - Escrever a versão mínima (MVP): um mapa simples com um elemento por agente e o estado atual.
  - Priorizar evoluções futuras no backlog (animações, histórico, interações, sons).
  - Solicitar ao arquiteto a definição de como os eventos dos agentes chegam à visualização.

## Criar uma visualização em formato de cidade que represente os agentes do Squad Algo e mostre, em tempo real, o que cada um está fazendo, para que o usuário acompanhe o trabalho de forma intuitiva e visual. (prioridade: media)
- Critérios de aceite:
  - [ ] Cada agente aparece como um elemento identificável (nome e papel) na cidade
  - [ ] O estado de cada agente (ocioso, trabalhando, aguardando aprovação, com erro) é visível e diferenciado visualmente
  - [ ] As mudanças de estado aparecem na tela em até alguns segundos, sem precisar recarregar a página
  - [ ] Ao selecionar um agente, o usuário vê a tarefa atual e as últimas atividades
  - [ ] A visualização funciona com os agentes existentes e não exibe segredos nem dados sensíveis
- Tarefas:
  - Confirmar com o usuário quais agentes e quais estados devem ser exibidos na primeira versão
  - Definir quais informações de atividade cada agente deve expor (tarefa atual, status, histórico recente)
  - Definir o significado de 'tempo real' aceitável (ex.: atraso máximo em segundos)
  - Descrever o MVP: cidade simples com um prédio ou local por agente e indicadores de status
  - Listar itens fora do escopo da primeira versão (ex.: interação, edição de agentes pela cidade, animações complexas)
  - Encaminhar ao arquiteto a definição de como obter e transmitir os eventos de atividade
