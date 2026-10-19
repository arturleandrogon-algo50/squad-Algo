# Modelo de dados dos eventos do log lidos pela cidade

## Itens
- Formato do log: JSON Lines (um registro por linha, UTF-8, só acrescenta). Não há campo de tipo. Mensagem = tem 'para' e 'tarefa'. Resposta = tem 'status'. A ordem dos eventos é a posição da linha no log.
- Mensagem: id (string, obrigatório, único), de (string, agente), para (string, agente), tarefa (string), contexto (objeto, opcional, sanitizado). Ex.: {"id":"m-0042","de":"orquestrador","para":"dados","tarefa":"Definir modelo do log","contexto":{"decisao":"resumo"}}
- Resposta: id (string, igual ao da Mensagem), de (string, agente que respondeu), status (enum: ok | erro | precisa_aprovacao), resultado (objeto ou string, opcional), motivo (string, obrigatório se status for erro ou precisa_aprovacao, senão null ou ausente). Ex.: {"id":"m-0042","de":"dados","status":"ok","resultado":{"itens":6},"motivo":null}
- Correlação: o id liga a Mensagem à sua Resposta, e Resposta.de deve ser igual a Mensagem.para. Mensagem sem Resposta do mesmo id fica pendente (estado 'trabalhando'). Resposta órfã ou duplicada é descartada pelo harness.
- Validação e sanitização no harness: descarta linha que não seja JSON, tenha campo obrigatório ausente, tipo errado ou status fora do enum. Em 'contexto' e 'resultado' mantém só os campos da lista permitida, trunca strings (ex.: 500 caracteres) e remove chaves sensíveis (senha, token, chave). O registro entregue mantém o mesmo schema.
- Entrega à cidade (somente leitura): o endpoint devolve a lista de Mensagens e Respostas válidas e sanitizadas, na ordem do log. A cidade deriva o estado de cada agente por função pura e mostra a tarefa atual (última Mensagem pendente) e as últimas N=10 atividades (agente como 'de' ou 'para').

## Alertas
- O contrato não tem timestamp. A ordenação usa a posição no log, o que impede mostrar hora das atividades. Adicionar um campo 'ts' alteraria o contrato e exigiria aprovação.
- Mensagem pendente sem Resposta mantém o agente em 'trabalhando' indefinidamente. Convém definir um timeout ou aceitar essa limitação.
- A lista de campos permitidos de 'contexto' e 'resultado' ainda precisa ser definida e mantida pelo harness. Sem ela, o padrão deve ser descartar tudo.
