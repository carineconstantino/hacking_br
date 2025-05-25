<p align="left">
    <a href="https://github.com/carineconstantino/hackingbr">@hackingbr></a>
</p>

## 👾 NMAP [Ultimate Guide]

## Simple Scan
<p> Primeiro scan com pacotes SYN, detecção da versão dos serviços e os scripts padrão.
O pacote SYN não completa a conexão com o host, a avaliação do estado da porta ocorre da seguinte forma:</p>

Scan automático: [nmap.sh]()

* resposta do host com SYN-ACK = posta aberta
* resposta do host com RST = porta fechada
* sem resposta ou ICMP unreachable = porta bloqueada/filtrada pelo firewall

```
nmap -Pn -sS -sV -sC [IP] -oN [file]
```
* -Pn = disable ping
* -sS = syn scan
* -sV = version scan
* -sC = default scripts
* -oN = save nmap results

## Vulnerability Scan
<p>Scan de vulnerabilidades usando os scripts da categoria vuln</p>

```
nmap -Pn -T4 -sS -p [PORT] --script vuln [IP] -oN [file]
```

* -Pn = disable ping
* -T4 = timing 4 aggressive
* -sS = syn scan
* -p = port
* --script vuln
* -oN = save nmap results

### Firewall/Filtro Scan
<p>Scan para validar firewall/filtros na rede</p>

### ACK Scan 
<p>Faz o mapeamento de regras do firewall ao enviar pacotes com a flag ACK habilitada, se uma porta filtrada pelo firewall responder com RST, indica que a conexão foi possível usando o pacote ACK.</p> 
```
nmap -sA --reason --traceroute [IP] -oN [file]
```
### Window Scan
<p>Ao responder com RST, caso o pacote o campo window não seja nulo, isso indica que o serviço existe e está filtrado pelo firewall. Quando o valor no campo window é zero, então a porta está fechada.</p> 
```
nmap -sW --reason --traceroute [IP] -oN [file]
```
### Maimon Scan
<p>Sistemas baseados em BSD não enviam o pacote RST quando a porta está aberta</p>
```
nmap -sM --reason --traceroute [IP] -oN [file]
```


### 🎯 Resultado na CLI

<p align="left">
    <img src="nmap-mind-map.png"><p></p>
</p>

#
