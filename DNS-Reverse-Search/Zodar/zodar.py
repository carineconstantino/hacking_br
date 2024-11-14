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
subtitle = "Reverse DNS Search"
print(Fore.RED + '-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')
print(Fore.RED + '-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')
print(Fore.RED + titulo + "[ " + subtitle + " ]" + '\n')
print('Criado por @hackingbr | www.hackingbr.com.br')
print(Fore.RED + '-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')
print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')

# Argumentos
if __name__ == '__main__':
    program_name = argparse.ArgumentParser(description='Zodar')
    program_name.add_argument('-ip', action='store', dest='ip',
                              required=True, help='Informe um ip para executar o DNS reverso ::: Exemplo: python3 zodar.py -ip [IP]')
    argumentos_parser = program_name.parse_args()
    base_ip = argumentos_parser.ip

def reverse_dns(): 
	try:
		result = subprocess.run(['dig', '-x', base_ip], capture_output=True, text=True, check=True)
		# extrai do domínios da "ANSWER SECTION"
		output = result.stdout
		output_clear = "\n".join([line for line in output.splitlines() if ";;" not in line])
		ptr_records = re.findall(r'\s+PTR\s+([^\s]+)', output_clear)
		if ptr_records:
			print(Fore.GREEN + f"Domínios associados ao IP {base_ip}:",'\n')
			for domain in ptr_records:
				print(Fore.GREEN + '[+]', Fore.CYAN + domain)
		else:
			print("Nenhum registro PTR encontrado")

		print(Fore.MAGENTA + "\nThat's it for now !!")
	except subprocess.CalledProcessError as e:
		print(f"Error executing dig command: {e}")
	except Exception as e:
		print(f"An unexpected error occurred: {e}")

reverse_dns()