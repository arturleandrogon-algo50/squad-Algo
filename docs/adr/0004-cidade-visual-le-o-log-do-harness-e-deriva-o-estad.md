# ADR 0004: Cidade visual lê o log do harness e deriva o estado dos agentes

## Contexto
A cidade visual precisa mostrar o estado de cada agente (ocioso, trabalhando, aguardando aprovação, erro), a tarefa atual e as últimas atividades, em poucos segundos e sem expor dados sensíveis. Os contratos Mensagem e Resposta já existem e devem ser mantidos. Os agentes não devem ganhar responsabilidades novas.

## Decisão
1) Fonte única: o harness grava cada Mensagem e cada Resposta, nos contratos atuais, em um log append-only de JSON linhas. A hora de gravação é metadado do log, não campo do contrato. Os agentes não emitem eventos de status. 2) Estado derivado: um componente de leitura no harness, com uma única responsabilidade, calcula o estado a partir do log. Mensagem com 'para' = X leva X a 'trabalhando'. Resposta de X com status ok leva a 'ocioso', erro leva a 'erro' e precisa_aprovacao leva a 'aguardando aprovação'. Sem eventos, o estado é 'ocioso'. 3) Contrato de leitura: a interface consome uma visão somente leitura em JSON validado por schema, com agente, estado, tarefa atual e as últimas N atividades. Ela atualiza por polling a cada ~2 s, sem recarregar a página. O atraso máximo de 5 s é uma proposta a confirmar com o usuário. 4) Privacidade: a visão expõe apenas id, agente, estado, título curto da tarefa e hora. Os campos 'contexto' e 'resultado' nunca são enviados à interface, e 'motivo' só aparece truncado e sanitizado. A sanitização é feita no harness, não na interface.

## Alternativas consideradas
- Agentes emitirem eventos de status próprios: descartada, pois criaria um formato paralelo, alteraria os contratos e aumentaria a responsabilidade dos agentes.
- Interface ler o log bruto diretamente: descartada, pois acopla a interface ao formato do log e aumenta o risco de vazamento de dados sensíveis.
- Push em tempo real (WebSocket/SSE) ou arquitetura orientada a eventos com broker: padrões fora da lista permitida, não usados. Só entrariam com aprovação, se o polling não bastar.
- Reprocessar o log inteiro a cada leitura: descartada. O componente de leitura deve manter o estado em memória e ler só as linhas novas.

## Consequências
- Nenhum contrato existente é alterado; a decisão não exige aprovação.
- Depende de a Resposta carregar o mesmo id da Mensagem que a originou, o que deve ser confirmado. Se não carregar, o vínculo precisará de outro ADR com aprovação.
- O polling é simples, mas gera tráfego constante e atraso de até ~2 s; é aceitável para o MVP.
- Próximos ADRs: (a) retenção e rotação do log; (b) formato do schema da visão de leitura e regras de sanitização; (c) hospedagem da interface (navegador ou painel local) após o usuário definir o estilo visual; (d) registro da hora no log como metadado do harness.
- O harness passa a ter a responsabilidade de registrar o log e expor a visão; o componente de leitura deve ficar separado do roteamento de mensagens.
