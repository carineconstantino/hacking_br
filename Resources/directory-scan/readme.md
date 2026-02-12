## FFUF 

### Scan Padrão
```
ffuf -u [url]:TESTE -w [wordlist]:TESTE
```

### Scan de Parâmetros GET
```
ffuf -u https://exemplo.com/script.php?TESTE=valor -w [wordlist]:TESTE

## Delay e Threads 
ffuf -u https://exemplo.com/script.php?TESTE=valor -w [wordlist]:TESTE -p 0.1 -t 10

ffuf -u https://exemplo.com/script.php?param=TESTE -w [wordlist]:TESTE
```

### Scan de Parâmetros POST
```
ffuf -w [wordlist]:TESTE -X POST -d "username=admin\&password=TESTE" -u https://target/login.php -fc 401

# Fuzz POST JSON data. Match all responses not containing text "error".
ffuf -w entries.txt -u https://example.org/ -X POST -H "Content-Type: application/json" \
      -d '{"name": "FUZZ", "anotherkey": "anothervalue"}' -fr "error"
```
### Scan Subdomínios
```
ffuf -u [url] -H "Host: TESTE.dominio.com" -w [wordlist]:TESTE
```
### Scan Extensions
```
ffuf -u http://172.20.3.144/indexFUZZ -w /root/Desktop/misc/SecLists/Discovery/Web-Content/web-extensions.txt
```

### Extensions
```
.asp
.aspx
.bat
.c
.cfm
.cgi
.css
.com
.dll
.exe
.htm
.html
.inc
.jhtml
.js
.jsa
.jsp
.log
.mdb
.nsf
.pcap
.php
.php2
.php3
.php4
.php5
.php6
.php7
.phps
.pht
.phtml
.pl
.reg
.sh
.shtml
.sql
.swf
.txt
.xml
```
### Scan Page
```
ffuf -u http://172.20.3.144/FUZZ.html -w /root/Desktop/misc/SecLists/Discovery/Web-Content/common.txt -v
```

## GoBuster

### Scan Subdominios
```
gobuster dns -d example.com -w /path/to/wordlist
```

### Scan VHOSTS
```
gobuster vhost -u https://example.com -w /path/to/wordlist

### Excluí respostas com um determinado tamanho
gobuster vhost -u https://example.com -w /path/to/wordlist --exclude-length 1542
```
### Scan extensions
```
gobuster dir -u 172.20.8.56 -w /root/Desktop/misc/SecLists/Discovery/Web-Content/common.txt --extensions php -v
```

## Feroxbuster
```
feroxbuster -u 172.20.8.56 -w /root/Desktop/misc/SecLists/Discovery/Web-Content/common.txt -x pdf
```

## DIRB
```
dirb http://172.20.8.56/ -X .html
```

