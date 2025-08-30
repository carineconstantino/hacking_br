## Broken Object Level Access
Ocorre quando uma aplicação falha em garantir o controle de acesso a funções ou dados. 
Essa ausência de controle de acesso permite que um usuário não autorizado obtenha acesso a dados de outros usuários ao manipular um parâmetro da requisição. 
Isso ocorre porque a aplicação não faz a validação correta das permissões do usuário que solicita o acesso. 

### Defesas
- Verificar as permissões do usuário para cada objeto ou função solicitado: toda vez que o usuário solicitar acesso a um objeto ou função, a aplicação deve verificar se o mesmo possui permissão de acesso.
- Centralizar o controle de acesso: garantir que o controle de acesso em toda a aplicação, além de evitar o gerenciamento de permissões localmente.
- Validar todas as entradas de dados, principalmente as entradas relacionadas com funções ou objetos.
- Implementar o monitoramento através de logs para identificar ações anômalas.
- Realizar avaliação de segurança (pentest) regularmente para identificar previamente essa vulnerabilidade.

### ACL - Access Control List
Nesse modelo, cada objeto como arquivos, registros na base de dados, e qualquer outro recurso dentro da aplicação possui uma lista de grupos de acesso com as permissões que os usuários neste grupo podem realizar (exemplo: read, write, delete). O gerenciamento de ACL pode se tornar completo dependendo da quantidade de usuários e de funções/objetos, pois cada objeto tem sua própria ACL. 
