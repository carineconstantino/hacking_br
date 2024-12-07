import socket
import time
import requests
import os
import re
import subprocess
from colorama import init, Fore, Back, Style
import pyfiglet

# Banner

titulo = pyfiglet.figlet_format("connTOR")
subtitulo = "[Troca o IP do TOR a cada 30 minutos]\n"
print(titulo)
print(subtitulo)
print("Criado por @hackingbr | www.hackingbr.com.br\n")
print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')

# Função para reiniciar o Tor
def reiniciar_tor():
    print(Fore.YELLOW + f" [+] Limpando a conexão na porta 9051...")
    clear_connection = os.system("fuser -k 9051/tcp >>/tmp/logtor.txt")
    print(Fore.BLUE + f" [+] Iniciando TOR...")
    init_tor = os.system("systemctl start tor")
    init_ip = requests.get('https://httpbin.org/ip')
    ip_origin = init_ip.json()['origin']
    print(Fore.GREEN + f" [+] IP sem Tor :::", ip_origin)
    # captura o status do TOR
    status_tor = "systemctl status tor"
    process = subprocess.Popen(status_tor, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    output = stdout.decode('utf-8')
    match = re.search(r'Active:\s*(\S+)', output)
    if match:
        status = match.group(1)
        print(Fore.GREEN + f" [+] Verificando Status:", status)
    else:
        print(Fore.RED + f" [+] Status não encontrado")

# Função para configurar o proxy SOCKS5
def configurar_proxy_tor():
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return proxies

# Função para testar a conexão via Tor
def testar_conexao_tor():
    proxies = configurar_proxy_tor()
    try:
        # paga o ip do TOR no header 'origin'
        response = requests.get('https://httpbin.org/ip', proxies=proxies)
        ip = response.json()['origin']
        # paga a geo location do ip
        ip_geo = requests.get(f"https://freegeoip.app/json/{ip}")
        geo_dados = ip_geo.json()
        country = geo_dados["country_name"]
        city = geo_dados["city"]
        print(Fore.CYAN + f" [+] Conexão bem-sucedida! IP via Tor: {ip} ::: {country} ::: {city}")
    except requests.RequestException as e:
        print(Fore.RED + f" [+] Erro na conexão com o Tor: {e}")

# Função principal
def main():
    # Loop para trocar o IP a cada 30 minutos
    while True:
        reiniciar_tor()
        # espera 30 minutos para trocar o novo ip
        tempo = 1800 
        for i in range(tempo, 0, -1):
            minutos = i // 60
            segundos = i % 60
            print(Fore.CYAN + f" [+] 30 minutos para a próxima troca de IP...{minutos:02d}:{segundos:02d}", end='\r')
            time.sleep(1) 
        print(Fore.CYAN + f"\n [+] Solicitando troca de IP...")
        testar_conexao_tor()

if __name__ == "__main__":
    main()
