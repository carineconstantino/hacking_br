# NMAP 
### Principais comandos
```
NOT-PORT Scan (-sn): executa apenas ping
nmap -sn [rede] 

## Ping Scan (Ping Sweep)

for i in $(seq 1 254); do ping -c 2 10.10.150.$i; done

## Salva o resultado em 3 formatos oN .nmap, oG .gnmap, oX .xml

nmap [192.168.0.1-20] -sn -oA tnet | grep for | cut -d" " -f5

## Scan Múltiplos IPs

nmap -sn -oA tnet [IP1 IP2 IP3] | grep for | cut -d " " -f5

## Mostra a resposta dos hosts ao scan realizado

nmap [rede] -sn -PE --reason

## Desabilitar o ARP-Ping durante o scan 

nmap [rede] -sc -PE --disable-arp-ping --packet-trace

## Scan Range de Portas

nmap -p 1-1000

## Identifica o sistema operacional 

nmap -O 

nmap -O --osscan-guess

## Identifica a versão do serviço

nmap -sV 

## TCP Connect 

nmap -sT

## Custom Top-Ports

nmap -sT -A --top-ports=20 [IP] -oG [file-output.txt]

## Scan dentro do Metasploit

db_nmap -sV [IP]

## Ver informação sobre o script 

nmap --script-help [nome-do-script]

## Executa scripts padrão 

nmap -sC 

## Categoria Discovery

nmap [IP] --script=discovery

## Scan a partir de uma lista de hosts

nmap -iL [nome-do-arquivo]
```
### UDP Scan
```
nmap -sU

nmap [IP] -p 1-250 -sU

nmap [IP] -p [porta] -sUV

nmap [IP] -p [porta] -sU --script=discovery
```
### Formatos de output
```
nmap -sU

nmap [IP] -p 1-250 -sU

nmap [IP] -p [porta] -sUV

nmap [IP] -p [porta] -sU --script=discovery
```
### Importar resultado do scan com NMAP para o Metasploit
```
## Inicia o postgresql 

service postgresql start

## Verifica o status da conexão do MSF com o Postgresql

db_status

## Importa o resultado do NMAP para o MSF

db_import [nmap-output-xml]

## Verifica os hosts importados 

host 

## Verifica os serviços 

service
```
### Comandos para scan em API
```
# General Detection Scan 
Usa scripts padrão '-sC'

nmap -sC -sV [IP or network range] -oA nameofoutput

# Scan All Ports

nmap -p- [IP] -oA allportscan

# HTTP Enum Script

nmap -sV --script=http-enum <target> -p 80,443,8000,8080
```
