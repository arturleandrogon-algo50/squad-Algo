# ADR 0001: Portão de aprovação humana no harness para ações sensíveis (apagar, enviar, gastar)

## Contexto
No projeto cidade-de-agentes (Python), agentes podem solicitar ações irreversíveis ou com custo: apagar dados, enviar mensagens externas e gastar recursos. É preciso garantir que um humano aprove essas ações antes da execução, sem que os agentes tenham como contorná-las. O controle deve ficar fora dos agentes, na camada de harness, para manter a responsabilidade única de cada agente.

## Decisão
1) Os agentes nunca executam ações sensíveis diretamente: eles apenas emitem uma solicitação de ação em JSON (campos: id, agente, tipo_acao em {apagar, enviar, gastar}, alvo, parametros, justificativa, custo_estimado). 2) O harness valida a solicitação contra um schema JSON; solicitação inválida é rejeitada. 3) Um componente único no harness, o PortaoDeAprovacao, classifica a ação por uma política declarativa em JSON (lista de tipos sensíveis e limites). Ações sensíveis ficam em estado 'pendente' e não são executadas. 4) A interface apresenta ao humano a solicitação com resumo e impacto, e devolve uma decisão em JSON validado (id, decisao: aprovar|negar, aprovador, timestamp). 5) Somente com decisão 'aprovar' correspondente ao id da solicitação o harness libera a execução pelo executor da ação. 6) Padrão seguro por omissão: sem resposta, timeout ou resposta inválida significa negar. 7) Cada aprovação vale para uma única solicitação (não reutilizável) e todas as solicitações e decisões são registradas em log de auditoria. 8) Princípios SOLID: o portão depende de uma abstração de canal de aprovação (interface), permitindo trocar o canal sem alterar o harness (inversão de dependência); a política é extensível por configuração, sem modificar o código (aberto/fechado).

## Alternativas consideradas
- Cada agente pedir aprovação por conta própria: rejeitada por violar 'um agente = uma responsabilidade' e permitir inconsistência e contorno.
- Aprovação por confirmação interativa apenas na interface, sem contrato JSON: rejeitada por não ser auditável nem validável.
- Lista de ações pré-aprovadas com aprovação automática por limite de custo: mantida apenas como opção da política declarativa, com limites definidos pelo humano.
- Uso de padrões fora da lista (ex.: máquina de estados formal, fila de mensagens/broker, event sourcing): não utilizados; exigiriam aprovação.

## Consequências
- Ações sensíveis ficam centralizadas e auditáveis em um único ponto.
- Agentes ficam mais simples e sem poder de executar ações irreversíveis sozinhos.
- Aumenta a latência das ações sensíveis, pois dependem de resposta humana.
- É necessário manter schemas JSON de solicitação, decisão e política, com versionamento.
- Exige definir e revisar periodicamente a política de quais ações são sensíveis e seus limites.
- O canal de aprovação pode ser trocado sem mudar agentes nem o núcleo do harness.
