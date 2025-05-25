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
    echo "2 - Definir MTU (--mtu)"
    echo "3 - Timing Template (-T0 a -T5)"
    echo "4 - Scan Delay (--scan-delay)"
    echo "5 - Max Rate (--max-rate)"
    echo "6 - Decoys (-D)"
    echo "7 - Spoof IP (-S)"
    echo "8 - Spoof MAC (--spoof-mac)"
    echo "9 - Idle Scan (-sI)"
    echo "10 - TCP Connect Scan (-sT)"
    echo "11 - Source Port (--source-port)"
    echo "12 - Data Payload (--data)"
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
            read -p "Valor de MTU (ex: 24, 8, 1400): " mtu
            parametros+=" --mtu $mtu"
            ;;
        3)
            read -p "Timing (0 = paranoid até 5 = insane): " timing
            parametros+=" -T$timing"
            ;;
        4)
            read -p "Delay entre pacotes (ex: 1s, 500ms): " delay
            parametros+=" --scan-delay $delay"
            ;;
        5)
            read -p "Limite de pacotes por segundo (ex: 10): " rate
            parametros+=" --max-rate $rate"
            ;;
        6)
            read -p "Lista de IPs decoy (ex: 1.1.1.1,2.2.2.2,ME): " decoys
            parametros+=" -D $decoys"
            ;;
        7)
            read -p "IP para spoof (-S): " spoof_ip
            parametros+=" -S $spoof_ip"
            ;;
        8)
            read -p "MAC falso (ex: 00:11:22:33:44:55 ou Apple/0): " mac
            parametros+=" --spoof-mac $mac"
            ;;
        9)
            read -p "Zombie host (ex: 192.168.0.100): " zombie
            parametros+=" -sI $zombie"
            ;;
        10)
            parametros+=" -sT"
            ;;
        11)
            read -p "Source port: " source
            parametros+=" --source-port $source"
            ;;
        12)
            read -p "Data Payload: " data
            parametros+=" --data $data"
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
