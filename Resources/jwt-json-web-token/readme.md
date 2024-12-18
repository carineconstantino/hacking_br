:hamburger: JWT é um token de autenticação/autorização que pode ser transmitido no header da requisição ou no cookie, e possui 3 partes:
   - Header: define o algoritmo que será usado para criar a assinatura do token (ex.: HS256, RS256)
   - Payload: define os dados que serão transmitidos e validados na autorização/autenticação. Os campos são customizados e são usados para validar a identidade e a sessão do usuário logado
   - Assinatura: verifica a integridade e autenticidade do token</p>

:fries:Checklist

- Algorithm Confusion
      <p>Teste se o token aceita o algoritmo do tipo "none". Quando o JWT aceita esse tipo de algoritmo, a assinatura do token é removida, ou seja, a integridade do token não é verificada no servidor. Se o JWT aceita o algoritmo "none", então é possível manipular os dados do payload podendo levar a explorações como IDOR para forjar o acesso/autorização de outros usuários</p>

- Brute forcing weak HMAC secrets 
      <p>Teste de força bruta na assinatura HMAC (HS256), se a "secret" for de baixa complexidade, é possível identificar a chave-secreta usada para assinar o token</p>

- RS256 to HS256 attack
        <p>A assinatura RS256 usa chave privada para criar a assinatura do token e a chave pública para fazer a verificação. Se a configuração estiver incorreta e a aplicação tratar a chave pública como HMAC, é possível assinar o jwt usando uma chave pública.</p>

- Header Injection
       <p>Neste ataque, adicionamos uma chave pública própria e o servidor usa essa chave-pública para forjar o token</p>
       <p>Parâmetros do header:
     - JWK - JSON Web Key - representa a assinatura do jwt
     - JKU - JSON Web Key Set URL - representa a url para buscar a chave
     - KID - Key ID - identifica qual chave usar quando existem várias</p>
      


        


