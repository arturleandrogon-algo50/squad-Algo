# ADR 0002: Aprovação humana no harness antes de ações sensíveis (apagar, enviar, gastar)

## Contexto
Agentes podem pedir ações irreversíveis ou com custo. Hoje não há ponto único que garanta aprovação humana antes da execução. Precisamos de um fluxo que respeite as camadas (agentes / harness / interface) e use somente os contratos existentes de Mensagem e Resposta.

## Decisão
1) O harness é o único portão: ele mantém uma lista configurável em JSON das ações sensíveis (apagar, enviar, gastar), validada na carga. Agentes nunca executam essas ações diretamente nem decidem se precisam de aprovação. 2) Ao receber a tarefa de um agente que casa com a lista, o harness não executa e responde com a Resposta {id, de: 'harness', status: 'precisa_aprovacao', resultado: {acao, alvo, custo_estimado quando houver}, motivo: por que é sensível}. 3) A interface mostra o pedido ao humano e devolve uma Mensagem {de: 'interface', para: 'harness', tarefa: 'aprovar' ou 'negar', contexto: {id_original}}. O harness valida o JSON, aceita apenas de='interface', confere que o id_original está pendente e executa exatamente os parâmetros originais, uma única vez. 4) Política de negar por padrão: negação, timeout, id desconhecido ou parâmetros divergentes resultam em Resposta com status 'erro' e motivo, sem execução.

## Alternativas consideradas
- Cada agente pedir confirmação direto ao humano: viola a separação em camadas e a responsabilidade única do agente.
- Flag 'confirmado' enviada pelo próprio agente: o agente poderia se autoaprovar.
- Novo formato de mensagem ou fila de aprovação dedicada: cria contrato paralelo e mudaria os contratos existentes (exigiria aprovação).
- Aprovação prévia permanente ou em lote (allowlist): padrão fora da lista permitida; precisa de aprovação antes de ser considerado.

## Consequências
- Nenhum contrato muda: reutiliza o status 'precisa_aprovacao' e os campos 'resultado', 'motivo' e 'contexto'.
- O harness passa a guardar pedidos pendentes; é preciso definir expiração e persistência.
- Os campos internos de 'resultado' e 'contexto' ganham um esquema JSON próprio, validado pelo harness.
- Próximos ADRs: (a) esquema JSON de 'resultado' e 'contexto' para aprovações; (b) timeout e expiração de pendências; (c) limites de gasto e critérios de sensibilidade; (d) trilha de auditoria das aprovações e negações.
