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
Nesse modelo, cada objeto como arquivos, registros na base de dados, e qualquer outro recurso dentro da aplicação possui uma lista de grupos de acesso com as permissões que os usuários neste grupo podem realizar (exemplo: read, write, delete). O gerenciamento de ACL pode se tornar complexo dependendo da quantidade de usuários e de funções/objetos, pois cada objeto tem sua própria ACL. 

### RBAC - Role Based Access Control 
No modelo RBAC, a permissão não é atribuída diretamente a um usuário individualmente como na ACL. Neste modelo, existe o conceito de função (role) e o usuário ou grupo de usuários são atribuídos a uma função, que possui as permissões de acesso necessárias para determinadas ações. Na imagem abaixo podemos ver o modelo ilustrado. Um usuário com a função Admin pode criar, deletar e editar, enquanto um usuário com a função Viewer apenas vai visualizar um objeto mas não poderá alterá-lo. 

RBAC se diferencia da ACL, pois na ACL as permissões são atribuídas diretamente para cada objeto, e cada objeto tem uma lista de usuários e permissões. Isso significa que a decisão de acesso é realizada no nível do objeto, ou seja, descentralizado. No RBAC, o gerenciamento de permissões é centralizado, associando funções a objetos ao invés de atribuir permissão individualmente. Esse modelo tem maior escalabilidade e atende melhor ambientes complexos, ao invés de atualizar listas de acesso descentralizadas, o RBAC gerencia as funções de acesso e no caso de alteração de usuário para outra função, troca-se apenas a "role", ou seja, a função do usuário. 

### ABAC - Attribute Based Access Control
Nesse modelo, as decisões de acesso são baseadas na combinação de atributos relacionadas com um objeto. Esses atributos incluem fatores como a função do usuário, o departamento, o tipo de dado que o usuário vai acessar (sensibilidade da informação), o horário de acesso, a localização do usuário, etc. Exemplo: um usuário pode acessar determinado objeto se corresponder a determinadas condições. Essas condições podem ser "acesso permitido apenas durante o horário comercial e através de uma rede segura". 

No ABAC o aceito de politica de acesso permite a configuração de atributos. Esas politicas de acesso são avaliadas em tempo real para determinar se todas as condições são atendidas na solicitação de acesso. 
