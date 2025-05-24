#!/bin/bash

ORANGE="\e[0;33m"

# verifica se os argumentos foram informados
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <IP> <nome_base_arquivo>"
    exit 1
fi

IP="$1"
BASE="$2"

# primeiro scan
echo -e "${ORANGE}┌─**-------------------------------------------------------------------------------**─┐"
echo -e "${ORANGE}  * Scan inicial == SYN Packet, Version Detect, Common Scripts: $IP"
echo -e "${ORANGE}└─**-------------------------------------------------------------------------------**─┘"
nmap -Pn -sS -sV -sC -oN "${BASE}.txt" "$IP"

# scan portas identificadas
echo -e "${ORANGE}┌─**--------------------------**─┐"
echo -e "${ORANGE}  * Scan de vulnerabilidade"
echo -e "${ORANGE}└─**--------------------------**─┘"
PORTAS=$(grep -E "^[0-9]+/tcp\s+open" "${BASE}.txt" | cut -d'/' -f1)

# executa scan de vulnerabilidade para cada porta
for PORTA in $PORTAS; do
    echo -e "${ORANGE}┌─**-----------------------------------------------**─┐"
    echo -e "${ORANGE}  * Scan de vulnerabilidades na porta $PORTA"
    echo -e "${ORANGE}└─**-----------------------------------------------**─┘"
    echo ""
    nmap -Pn -T4 -sS -sV -sC -p "$PORTA" --script vuln -oN "${PORTA}.txt" "$IP"
done

echo "[*] Scan finalizado"
