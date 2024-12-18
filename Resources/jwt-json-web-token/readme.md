<p>JWT é um token de authenticação/autorização que pode ser transmitido no header da requisição ou no cookie, e possui 3 partes:
   - Header: define o algoritmo que será usado para criar a assinatura do token (ex.: HS256, RS256)
   - Payload: define os dados que serão transmitidos e validados na autorização/autenticação. Os campos são customizados e são usados para validar a identidade e a sessão do usuário logado
   - Assinatura: verifica a integridade e autenticidade do token</p>



