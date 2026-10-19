# Casos de teste do portão de aprovação humana do harness

## Itens
- APROVAR: o agente devolve Resposta com status=precisa_aprovacao e o humano aprova dentro do prazo. Esperado: antes da decisão, o estado derivado é 'aguardando aprovação' e a ação não é executada. Após a aprovação, a ação segue, a Resposta final tem status=ok e o estado volta a 'ocioso'.
- NEGAR: o humano nega o pedido. Esperado: a ação não é executada, o harness registra Resposta com status=erro e motivo='negado pelo humano' (o contrato não tem status 'negado'), o estado vira 'com erro' e não há nova tentativa automática.
- TIMEOUT: nenhuma decisão chega até o prazo. Esperado: tratamento fail-safe equivalente a negação. A ação não é executada, a Resposta tem status=erro e motivo='timeout de aprovação', o estado vira 'com erro', e uma decisão tardia posterior é ignorada.
- RESPOSTA INVÁLIDA: JSON malformado, campo obrigatório ausente, status fora de ok|erro|precisa_aprovacao (ex.: 'aprovado') ou id sem pedido pendente. Esperado: o harness descarta o registro, ele não conta como aprovação nem chega à interface, e o pedido continua 'aguardando aprovação' até decisão válida ou timeout.
- DECISÃO DUPLICADA OU CONFLITANTE: aprovar e negar chegam para o mesmo id, ou a mesma decisão chega duas vezes. Esperado: só a primeira decisão válida prevalece, a ação executa no máximo uma vez, e a segunda é ignorada e registrada como descartada.
- SANITIZAÇÃO NO PEDIDO: o 'contexto' ou 'resultado' do pedido de aprovação contém um campo fora da lista permitida ou um segredo. Esperado: a interface recebe apenas campos permitidos (truncados se necessário), nunca o segredo, e o fluxo de aprovação segue normalmente com os dados sanitizados.

## Alertas
- O canal da decisão humana não está definido: a interface é somente leitura e não acessa os agentes, então é preciso definir por onde a aprovação entra no harness (ex.: endpoint próprio) antes de implementar estes testes.
- O valor do prazo de aprovação não está definido. Não confundir com o atraso máximo de 5 s da interface: são tempos diferentes.
- O contrato não tem status de negação nem de timeout: usei status=erro com motivo. Se for criado um status novo, os casos 2 e 3 precisam ser revistos.
- Deve haver um teste de que nenhuma ação sensível executa sem aprovação explícita. Falha fechada é o comportamento esperado em qualquer ambiguidade.
