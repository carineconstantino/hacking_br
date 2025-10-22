## FFUF 

### Scan Padrão
```
ffuf -u [url]:TESTE -w [wordlist]:TESTE
```

### Scan de Parâmetros GET
```
ffuf -u https://exemplo.com/script.php?TESTE=valor -w [wordlist]:TESTE

ffuf -u https://exemplo.com/script.php?param=TESTE -w [wordlist]:TESTE
```

### Scan de Parâmetros POST
```
ffuf -w [wordlist]:TESTE -X POST -d "username=admin\&password=TESTE" -u https://target/login.php -fc 401
