#!/bin/bash

# Função: IP → Decimal
ip_to_decimal() {
    local IFS=.
    read -r o1 o2 o3 o4 <<< "$1"
    echo $(( (o1 << 24) + (o2 << 16) + (o3 << 8) + o4 ))
}

# Função: Decimal → IP
decimal_to_ip() {
    local dec=$1
    echo "$(( (dec >> 24) & 255 )).$(( (dec >> 16) & 255 )).$(( (dec >> 8) & 255 )).$(( dec & 255 ))"
}

# Validação simples de IP
valid_ip() {
    [[ $1 =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || return 1
    for i in $(echo $1 | tr "." " "); do
        (( i >= 0 && i <= 255 )) || return 1
    done
}

echo "=== Gerador de Wordlist IP Range ==="
read -p "IP inicial: " start_ip
read -p "IP final: " end_ip
read -p "Nome do arquivo de saída: " output_file

# Validações
if ! valid_ip "$start_ip"; then
    echo "IP inicial inválido."
    exit 1
fi

if ! valid_ip "$end_ip"; then
    echo "IP final inválido."
    exit 1
fi

start_dec=$(ip_to_decimal "$start_ip")
end_dec=$(ip_to_decimal "$end_ip")

if (( start_dec > end_dec )); then
    echo "IP inicial deve ser menor que IP final."
    exit 1
fi

echo "[+] Gerando wordlist..."

for (( i=start_dec; i<=end_dec; i++ )); do
    decimal_to_ip "$i"
done > "$output_file"

echo "[✔] Wordlist criada: $output_file"
echo "[+] Total de entradas: $((end_dec - start_dec + 1))"
