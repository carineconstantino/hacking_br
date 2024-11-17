import subprocess
import re
import argparse
import pyfiglet
import datetime
from colorama import init, Fore, Back, Style
import requests


init()

# Banner
titulo = pyfiglet.figlet_format("Zodar")
subtitle = "Subdomain Search"
print(Fore.RED + '-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')
print(Fore.RED + '-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')
print(Fore.RED + titulo + "[ " + subtitle + " ]" + '\n')
print('Criado por @hackingbr | www.hackingbr.com.br')
print(Fore.RED + '-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')
print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')

# Argumentos
if __name__ == '__main__':
    program_name = argparse.ArgumentParser(description='Zodar')
    program_name.add_argument('-domain', action='store', dest='domain',
                              required=True, help='Informe um domínio para executar a busca ::: Exemplo: python3 zodar.py -domain [dominio]')
    argumentos_parser = program_name.parse_args()
    base_domain = argumentos_parser.domain

def subdomain_search():
    file_path = "subdomains.txt"
    print(Fore.GREEN + f"Lista de Subdominios para *.{base_domain}")
    try:
        with open(file_path, 'r') as open_file:
            for line in open_file:
                subdomain = line.strip()
                domain_base = f'{subdomain}.{base_domain}'
                try:
                    result = subprocess.run(['host', domain_base], capture_output=True, text=True, check=True)
                    output = result.stdout
                    if "has address" in output:
                        print(Fore.GREEN + f"{domain_base}")
                except subprocess.CalledProcessError as e:
                    pass
                    #print(Fore.RED + f"Erro ao consultar o domínio {domain_base}: {e}")
                    #print(f"Saída de erro: {e.stderr}")  # Exibe o stderr do erro
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

subdomain_search()
