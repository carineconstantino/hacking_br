## FFUF 

### Scan Padrão
```
ffuf -u [url]:TESTE -w [wordlist]:TESTE
```

### Scan de Parâmetros GET
```
ffuf -u https://exemplo.com/script.php?TESTE=valor -w [wordlist]

ffuf -u https://exemplo.com/script.php?param=TESTE -w [wordlist]
```

