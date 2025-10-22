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




