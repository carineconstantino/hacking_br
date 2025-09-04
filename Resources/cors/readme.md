## CORS

### Origin 
Indica a origem (scheme + host + porta) do código (tipicamente JavaScript) que iniciou a requisição.
```
Origin: https://app.exemplo.com
```
Se o navegador em https://app.exemplo.com fizer uma requisição AJAX para https://api.exemplo.com/data, o cabeçalho Origin será https://app.exemplo.com.
O servidor de destino pode então decidir se vai permitir ou negar essa requisição com base nessa origem.

### SOP - Same-Origin Policy
O Origin é peça central na Same-Origin Policy (SOP), que define se scripts de uma origem podem acessar dados de outra.
Se Origin A tentar acessar recursos de Origin B, a política SOP e o Origin determinam se isso será bloqueado ou permitido.

### CORS
CORS (Cross-Origin Resource Sharing) é um mecanismo de segurança implementado pelos navegadores modernos que regula como recursos (ex.: APIs, fontes, imagens, scripts) 
podem ser requisitados de um domínio diferente daquele em que a aplicação web foi carregada.

Same-Origin Policy (SOP):
Exemplo: uma página em https://app.exemplo.com não pode, por padrão, ler a resposta de uma API em https://api.outraempresa.com.
Isso evita que código malicioso injetado em um site consiga roubar dados de outros sistemas autenticados pelo usuário.

### Cabeçalhos CORS:
Para permitir exceções seguras, o servidor de destino pode configurar HTTP Headers que instruem o navegador sobre quais origens externas são confiáveis. Alguns exemplos:

Access-Control-Allow-Origin: define quais domínios podem acessar (* = qualquer origem).

Access-Control-Allow-Methods: quais métodos HTTP são permitidos (GET, POST, PUT, DELETE...).

Access-Control-Allow-Headers: quais cabeçalhos customizados podem ser enviados pelo cliente.

Access-Control-Allow-Credentials: define se cookies e tokens de autenticação podem ser enviados em requisições cross-origin.
