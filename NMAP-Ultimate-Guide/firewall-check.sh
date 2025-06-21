#!/bin/bash

ORANGE="\e[0;33m"

# valida os parametros de entrada
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <IP> <Resultado>"
    exit 1
fi

IP="$1"
RESULTADO="$2"

echo -e "${ORANGE}┌─**------------------------------------------------------**─┐"
echo -e "${ORANGE}  * Avaliação de regras e filtros de firewall: $IP"
echo -e "${ORANGE}  * Resultados serão salvos em $RESULTADO"
echo -e "${ORANGE}└─**------------------------------------------------------**─┘" 

# Executa os scans com diferentes técnicas
echo -e "${ORANGE}┌─**---------------------------------------**─┐"
echo -e "${ORANGE}  * ACK Scan: $IP"
echo -e "${ORANGE}└─**---------------------------------------**─┘" 
nmap -sA --reason --traceroute "$IP" -oN "$RESULTADO-ACK.txt"
echo -e "${ORANGE}┌─**---------------------------------------**─┐"
echo -e "${ORANGE}  * NULL Scan: $IP"
echo -e "${ORANGE}└─**---------------------------------------**─┘" 
nmap -sN --reason --traceroute "$IP" -oN "$RESULTADO-NULL.txt"
echo -e "${ORANGE}┌─**---------------------------------------**─┐"
echo -e "${ORANGE}  * FIN  Scan: $IP"
echo -e "${ORANGE}└─**---------------------------------------**─┘" 
nmap -sF --reason --traceroute "$IP" -oN "$RESULTADO-FIN.txt"
echo -e "${ORANGE}┌─**---------------------------------------**─┐"
echo -e "${ORANGE}  * XMAS  Scan: $IP"
echo -e "${ORANGE}└─**---------------------------------------**─┘"
nmap -sX --reason --traceroute "$IP" -oN "$RESULTADO-XMAS.txt"
echo -e "${ORANGE}┌─**---------------------------------------**─┐"
echo -e "${ORANGE}  * Scan Finalizado. Resultado salvo"
echo -e "${ORANGE}  * $RESULTADO-ACK.txt"
echo -e "${ORANGE}  * $RESULTADO-NULL.txt"
echo -e "${ORANGE}  * $RESULTADO-FIN.txt"
echo -e "${ORANGE}  * $RESULTADO-XMAS.txt"
echo -e "${ORANGE}└─**---------------------------------------**─┘"
