#!/bin/bash

ORANGE="\e[0;33m"

echo -e "${ORANGE}┌─**--------------------------------------**─┐"
echo -e "${ORANGE}  * Evasão de Firewall / IDS / IPS com Nmap"
echo -e "${ORANGE}└─**--------------------------------------**─┘"
read -p "${ORANGE} Digite o IP: " alvo
read -p "${ORANGE} Digite o nome do arquivo para salvar os resultados: " arquivo

# Inicializa os parâmetros
parametros=""

# Função de menu
menu() {
    echo ""
    echo -e "${ORANGE}┌─**----------------------------------------------**─┐"
    echo "Escolha as técnicas de evasão (digite o número, 0 para finalizar):"
    echo "1 - Fragmentação (-f)"
    echo "2 - Source Port (-g)"
    echo "3 - Data Length (--data-length)"
    echo "4 - TTL Scan (--ttl)"
    echo "5 - Decoy Scan (-D)"
    echo "6 - Spoof IP (-S)"
    echo "0 - Finalizar seleção"
    echo -e "${ORANGE}└─**---------------------------------------------**─┘"
}

while true; do
    menu
    read -p "Opção: " opcao

    case $opcao in
        1)
            parametros+=" -f"
            ;;
        2)
            read -p "Source port (-g):" source
            parametros+=" -g $source"
            ;;
        3)
            read -p "Data Length (--data-length):" data
            parametros+=" --data-length" $data
            ;;
        4)
            read -p "TTL Scan (--ttl):" ttl
            parametros+=" --ttl $ttl"
            ;;
        5)
            read -p "Decoy Scan (-D):" decoy
            parametros+=" -D $decoy"
            ;;
        6)
            read -p "Spoof IP address (-S):" spoofip
            parametros+=" -S $spoofip"
            ;;    
        0)
            break
            ;;
        *)
            echo "Opção inválida."
            ;;
    esac
done

echo ""
echo -e "${ORANGE}┌─**---------------------------------------------**─┐"
echo -e "${ORANGE}   * Iniciando o scan com os seguintes parâmetros:"
echo -e "${ORANGE}   * nmap $parametros $alvo -oN $arquivo"
echo -e "${ORANGE}└─**---------------------------------------------**─┘"
echo ""

# Executa o nmap com os parâmetros escolhidos
nmap $parametros $alvo -oN "$arquivo"
