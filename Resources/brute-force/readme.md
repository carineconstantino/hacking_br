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
### Types of Brute-Force with Burp Suite

- Sniper
- Used to test many different payloads for a single parameter.

- Battering Ram
- Used when the same payload needs to be tested on multiple parameters.

- Pitchfork
- Used when different payloads need to be tried on all parameters in a cross manner. For example, element from the first payload list is tried for the first parameter, element from the second payload list for the second parameter, and then crossing over the lists.
- Usado quando diferentes payloads precisam ser testados em todos os parâmetros, de modo que o payload da primeira wordlist é testado no primeiro parâmetro, o elemento da segunda wordlist é testado no segundo parâmetro, e depois os valores se invertem. 

- Cluster Bomb
- Used when separate payloads for all parameters are to be tried without crossover. Element from the first payload list is tried for the first parameter, while the second payload list is used for the second parameter.
- 
