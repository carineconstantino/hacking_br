## Session Fixation
Essa falha ocorre quando a aplicação não modifica o token de sessão após o login do usuário. A aplicação mantém o mesmo SESSION ID da sessão desautenticada após o usuário logar. 
Outro cenário possível onde a vulnerabilidade de Session Fixation ocorre é quando o token não é descartado após o logout da sessão. Nesse caso, o token de sessão de um usuário que fez o logou pode ser reaproveitado. 
