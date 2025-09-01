## Session Fixation
Essa falha ocorre quando a aplicação não modifica o token de sessão após o login do usuário. A aplicação mantém o mesmo SESSION ID da sessão desautenticada após o usuário logar. 
Outro cenário possível é quando o token não é descartado após o logout da sessão. Nesse caso, o token de sessão de um usuário que fez o logout pode ser reaproveitado. A captura do token de sessão pode ocorrer em um ataque de Cross-Site Scripting, ao transmitir o token de sessão como parâmetro na requisição GET ou quando a aplicação processa Javascript de outros sites (falha CORS). 

### Defesas 
- Invalidar o token de sessão após um novo token ser criado
- Modificar o token de sessão após o usuário realizar o login
- Habilitar HttpOnly no cookie de sessão: previne que o cookie seja acessado por Javascript malicioso
- Habilitar Secure no cookie de sessão: garante que o cookie é transmitido apenas por HTTPS e não por HTTP
- Adicione Expire e Max-Age no cookie de sessão: define um tempo para o cookie de sessão expirar
- Implemente SESSION ID de forma randomica através de frameworks seguros para evitar que o atacante consiga reproduzir o cookie de sessão
- Habilitar SameSite: não permite que o cookie seja transmitido para outro site, apenas o site original pode transmitir o cookie de sessão

  
