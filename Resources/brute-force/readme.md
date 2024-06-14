## Brute-Force
### Wordlists
#### Assetnote
```https://wordlists.assetnote.io/```

#### Seclists
```sudo apt install seclists```

Search in Seclists
```find /usr/share/seclists -iname “*[string]*”```

### FFUF
[1] Copia a requisição do burp e salva em um arquivo .txt<p>
[2] Adiciona nos campos de login: FUZZUSER e FUZZPASS

```ffuf -request req.txt -request-proto https -mode clusterbomb -w /usr/share/seclists/users.txt:FUZZUSER -w /usr/share/seclists/pass.txt:FUZZPASS -mc 302```

### HYDRA
#### SSH
```
hydra -v -l [username] -P senhas.txt [IP] ssh -s [PORT]
```
### MEDUSA
#### POSTGRES
Instalação do client no Ubuntu ```apt install postgresql-client-common```
```
medusa -H ips.txt -u [nome-do-usuario] -p [senha] -M [modulo] -n [porta]

### ver os módulos

medusa -d 
```


