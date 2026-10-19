# ADR 0005: Cidade visual lê o log existente via harness e deriva o estado de cada agente

## Contexto
A cidade visual precisa mostrar nome, papel, estado (ocioso, trabalhando, aguardando aprovação, com erro), tarefa atual e atividades recentes de cada agente, com atualização em poucos segundos e sem expor segredos. Já existem os contratos Mensagem (id, de, para, tarefa, contexto) e Resposta (id, de, status, resultado, motivo). O log dos agentes é composto por esses registros, então não é necessário criar um formato novo.

## Decisão
1) Camadas: o harness lê o log, valida cada registro como Mensagem ou Resposta (JSON validado) e descarta o que for inválido. A interface (cidade) não acessa o log nem os agentes diretamente; só consome o que o harness entrega, em modo somente leitura. Os agentes não mudam e não conhecem a cidade. 2) Sem formato paralelo: a interface recebe os próprios registros Mensagem e Resposta, já sanitizados pelo harness. O harness remove ou trunca 'contexto' e 'resultado' por lista de campos permitidos, e nunca repassa segredos. O estado é derivado, não gravado, por uma função pura na interface: Mensagem com para=X sem Resposta de mesmo id → 'trabalhando'; Resposta de X com status ok → 'ocioso'; status erro → 'com erro'; status precisa_aprovacao → 'aguardando aprovação'. Agente sem registros começa 'ocioso'. 3) Tempo real: a interface consulta o endpoint de leitura do harness a cada 2 s (atraso máximo aceitável proposto: 5 s), sem recarregar a página, e atualiza apenas os elementos que mudaram. 4) Seleção de agente: a tarefa atual é o campo 'tarefa' da última Mensagem pendente; as últimas atividades são os N registros mais recentes (N=10 proposto) em que o agente aparece como 'de' ou 'para'. Cada responsabilidade fica em um componente próprio: leitor de log, validador/sanitizador, derivador de estado e renderização.

## Alternativas consideradas
- Criar um novo contrato de 'evento de atividade' emitido pelos agentes: rejeitada, pois cria formato paralelo e muda contrato existente.
- Push em tempo real (WebSocket/SSE com publish-subscribe): fora dos padrões permitidos; não usada, exigiria aprovação (precisa_aprovacao=true) se o polling não bastar.
- Interface lendo o log diretamente: rejeitada, pois viola a separação em camadas e aumenta o risco de vazar dados sensíveis.
- Cada agente publicar seu próprio estado: rejeitada, pois acopla agentes à interface e foge de 'um agente = uma responsabilidade'.

## Consequências
- Nenhum contrato existente é alterado, então não há aprovação arquitetural adicional. A aprovação do usuário sobre o escopo do MVP, pedida pelo analista, continua necessária antes da implementação.
- Premissa a confirmar: a Resposta usa o mesmo 'id' da Mensagem que a originou. Se não usar, o vínculo entre as duas precisa ser decidido em outro ADR.
- Polling gera pequena carga periódica e atraso de poucos segundos, o que atende ao critério 'até alguns segundos'.
- Próximos ADRs: (a) fonte do nome e papel de cada agente; (b) lista de campos permitidos na sanitização e regras de privacidade; (c) formato e localização do log; (d) layout da cidade (2D simples) e itens fora do escopo.
