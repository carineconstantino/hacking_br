### O que é Cross-site Scripting (XSS)?

Cross-site Scripting (XSS) é um tipo de vulnerabilidade comum em aplicações web, que se baseia principalmente em ataques de injeção de código no lado do cliente. Os atacantes visam executar código JavaScript malicioso nos navegadores dos usuários que visitam as páginas ou aplicações web onde o código XSS foi incorporado.

O ataque é acontece quando os usuários visitam uma página ou aplicação web que contém o código malicioso. A página ou aplicação web atua como um meio para executar os scripts maliciosos no navegador do usuário. Vulnerabilidades XSS são frequentemente detectadas em plataformas que incluem fóruns, interfaces de mensagens e campos de comentários onde os usuários inserem informações.

### Efeitos dos ataques XSS

Os ataques de Cross-site Scripting (XSS) podem levar a sérias ameaças à segurança, como roubo de cookies de sessão do usuário, vazamento de dados confidenciais, alteração do conteúdo da página da web ou execução de ações não autorizadas no aplicativo.

### Roubo de Cookies de Sessão

Ataques XSS permitem que invasores roubem os cookies de sessão dos usuários. Os cookies armazenam informações de sessão dos usuários e são comumente usados ​​para login automático em sites. Quando os invasores obtêm acesso a esses cookies, eles podem acessar contas de usuários sem autorização e realizar ações em nome deles.

### Vazamento de Dados Sensíveis

Ataques XSS podem levar ao vazamento de informações sensíveis. Os invasores podem capturar dados de formulários, informações de cartões de crédito e outros dados pessoais por meio de scripts maliciosos. Esses vazamentos de dados podem resultar em consequências graves, como fraudes e roubo de identidade.

### Modificação do Conteúdo de Páginas Web

Ataques XSS podem ser usados ​​para alterar a aparência e o conteúdo de uma página web. Isso pode impactar negativamente a experiência do usuário, apresentando conteúdo falso ou malicioso, potencialmente induzindo-o ao erro. Além disso, pode prejudicar a imagem corporativa e a confiança do cliente.

### Execução de Operações Não Autorizadas

Ataques XSS permitem que invasores façam uso indevido das permissões dos usuários em aplicações web. Por exemplo, um invasor pode usar a conta da vítima para prejudicar outros usuários, adicionar novos administradores, excluir ou modificar dados e realizar operações não autorizadas.

### Ataques de Engenharia Social

Ataques XSS podem ser usados ​​como parte de campanhas mais amplas de engenharia social. Os invasores podem tentar enganar os usuários enviando links ou mensagens maliciosas que parecem vir de uma fonte confiável.

### Acionamento de outras vulnerabilidades de segurança

As vulnerabilidades XSS comprometem a segurança geral de um site ou aplicativo. Essas vulnerabilidades podem servir como porta de entrada para outros tipos de ataques, como Cross-Site Request Forgery (CSRF).

### Os ataques XSS são categorizados em três tipos principais:

<b>XSS Refletido (XSS Não Persistente):</b> Ocorre quando os dados enviados por um usuário são refletidos imediatamente por uma aplicação web sem a devida filtragem e, em seguida, executados pelo navegador do usuário. Scripts maliciosos geralmente são enviados por meio de parâmetros de URL e executados quando o usuário abre a URL.

<b>XSS Armazenado (XSS Persistente):</b> Ocorre quando scripts maliciosos são armazenados no banco de dados da aplicação web e executados quando outros usuários visualizam o conteúdo afetado.

<b>XSS baseado em DOM (XSS baseado em DOM):</b>: Scripts maliciosos são executados diretamente manipulando o Modelo de Objeto de Documento (DOM) no navegador do usuário. Nesse caso, o atacante aciona a execução de scripts do lado do cliente de uma aplicação web alterando o DOM.

<b>DOM (Document Object Model):</b> Uma interface de programação que representa um documento HTML como uma estrutura hierárquica em árvore, permitindo a interação com o documento usando linguagens como JavaScript.

### Content Security Policy (CSP)
A security protocol that restricts the sources from which a web page can load scripts, helping to prevent XSS attacks.
```
Content-Security-Policy: script-src 'self' https://apis.example.com
```
### Commonly Used JavaScript Functions and Objects in XSS Attacks
```
alert()	## Displays a message box to the user.
prompt()	## Prompts the user for input and returns the entered value.
confirm()	## Displays a confirmation box to the user. The user can choose "OK" or "Cancel".
eval()	## Evaluates a string as JavaScript code and executes it. Unsafe for user inputs and may lead to vulnerabilities.
fetch()	## Sends an HTTP request to the specified URL and returns a Promise. The request result can be handled in the Promise chain.
document.cookie	## Provides access to the browser's cookies.
innerHTML	## Used to change the content of an HTML element.
setTimeout()	## Executes a specified function after a certain time interval.
setInterval()	## Repeatedly executes a specified function at certain time intervals.
XMLHttpRequest	## Used to exchange data with a server in the background.
localStorage	## Used to store persistent data in the browser.
sessionStorage	## Provides access to the browser's session storage.
```
### Commonly Used HTML Tags in XSS Attacks
```
<script>	## Used to include JavaScript code in the page.
<img>	## Used to embed an image.
<iframe>	## Used to embed another web page into the current page.
<a>	## Used to create a hyperlink.
<input>	## Used to get user input.
<textarea>	## Used to get multi-line user input.
<svg>	## Used to create vector graphics.
```
### Análise do código-fonte
A causa fundamental da vulnerabilidade é a renderização direta da entrada do usuário no navegador sem verificações ou filtragens suficientes. Essa situação leva a vulnerabilidades de segurança, particularmente ataques XSS.
