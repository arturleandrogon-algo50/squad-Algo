# ADR 0003: Cidade visual lê o log dos agentes por uma projeção de estado somente leitura no harness

## Contexto
A cidade precisa mostrar em poucos segundos o estado de cada agente (ocioso, trabalhando, aguardando aprovação, erro), a tarefa atual e as últimas atividades, sem vazar dados sensíveis. Já existem os contratos Mensagem (id, de, para, tarefa, contexto) e Resposta (id, de, status ok|erro|precisa_aprovacao, resultado, motivo), e o log dos agentes. Não existe ainda um fluxo de eventos próprio nem uma interface gráfica. Estilo visual, plataforma e público continuam em aberto e ficam para outro ADR.

## Decisão
1) Fonte única: o log existente de Mensagens e Respostas. A interface nunca lê o log nem os agentes diretamente; consome apenas uma saída somente leitura do harness. Nenhum agente muda e nenhum contrato é alterado. 2) Um componente do harness, com uma só responsabilidade (projetor de estado), deriva o estado de cada agente a partir do log: Mensagem para o agente sem Resposta de mesmo id = trabalhando; Resposta status precisa_aprovacao = aguardando aprovação; Resposta status erro = erro; Resposta status ok ou nenhuma pendência = ocioso. Papel e nome vêm da lista de agentes configurada. 3) Sanitização por lista de permissão no harness, antes de chegar à interface: expõe apenas agente, papel, estado, tarefa (resumida e truncada), id e horário das últimas atividades. Os campos contexto e resultado, o texto livre de motivo e qualquer credencial nunca saem do harness. A saída é uma visão derivada em JSON validado por esquema, não um novo formato de mensagem entre agentes. 4) Atualização por consulta periódica (polling) da interface ao harness a cada 2 s, com atraso máximo aceitável de 5 s (valores a confirmar com o usuário), sem recarregar a página.

## Alternativas consideradas
- Interface lendo o arquivo de log diretamente: rejeitada, pois viola a separação em camadas e aumenta o risco de vazamento.
- Barramento de eventos (publish/subscribe) ou event sourcing: padrão fora da lista permitida; só com aprovação (precisa_aprovacao=true) caso o polling não atenda.
- Adicionar um campo de estado em Mensagem ou Resposta, ou novos status como 'trabalhando': mudaria contratos existentes e exigiria aprovação; rejeitada por ser desnecessária.
- Cada agente publicar o próprio estado: quebra 'um agente = uma responsabilidade' e acopla os agentes à interface.

## Consequências
- Nenhum contrato existente é alterado, portanto não há aprovação por mudança de contrato. O escopo geral (nova interface) ainda depende da aprovação do usuário, conforme o requisito.
- 'Ocioso' e 'trabalhando' são inferidos do log. Um agente que falha sem enviar Resposta fica como 'trabalhando'; é preciso um limite de tempo (timeout), a definir em ADR próprio.
- O polling é simples e atende ao MVP, mas gera consultas repetidas; a revisão fica para o backlog se houver mais agentes ou exigência de latência menor.
- A lista de permissão deve ter testes que garantam que contexto, resultado e segredos nunca apareçam na saída.
- Próximos ADRs: (a) estilo visual, plataforma e público da cidade; (b) esquema JSON da visão derivada e transporte entre harness e interface; (c) política de retenção e tamanho do histórico exibido; (d) timeout para agente sem resposta.
