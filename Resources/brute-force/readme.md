## Brute-Force
:fries: Checklist
- observe a diferença no tamanho das respostas (Lenght)
- observe a diferença no "status code" das respostas
- observe a diferença no tempo de resposta

:fries: Checklist para MFA
- tente acessar a página logada diretamente apenas "forçando" o path na requisição
- tente acessar a página logada diretamente apenas "dropando" a requisição do MFA
- observe parâmetros e campos da requisição MFA e tente modificá-los
- observe o tipo de código MFA e faça brute-force neles
- teste códigos de backup
- tente usar o mesmo código MFA mais de uma vez em uma mesma conta ou em outras contas
- observe mensagens de erro

<p>:bulb: Adicione no campo de senha uma grande quantidade de caracteres. Quando a aplicação identificar um usuário válido, vai tentar processar a requisição e o tempo de resposta será diferente dos demais. Esse "delay" na resposta indica que a aplicação tentou processar a autenticação de um usuário válido.</p> 

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
<p>NOTA: Em alguns ambientes pode ser necessário instalar o Postgres-Client antes de executar um brute-force nesse serviço</p>
```
apt install postgresql-client-common # instalação no Ubuntu
```

