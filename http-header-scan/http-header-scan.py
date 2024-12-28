import requests
import re
from datetime import datetime
import argparse
from colorama import init, Fore, Back, Style
import pyfiglet

# Banner

titulo = pyfiglet.figlet_format("Header Scan")
subtitulo = "[ Scan HTTP Headers ]\n"
print(titulo)
print(subtitulo)
print("Criado por @hackingbr | www.hackingbr.com.br\n")
print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')

class ScanHeaders:

    def __init__(self, url):

        self.url = url

if __name__ == '__main__':

    program_name = argparse.ArgumentParser(description = 'Scan HTTP Header')
    program_name.add_argument('--url', action='store', dest='url',
                                         required = True, help=''' Informe uma URL para testar a segurança do cabeçalho HTTP ::: 
                                                               Exemplo: python3 scan_header_http_I.py --url https://exemplo.com  ''')

    argumentos_parser = program_name.parse_args()
    url = argumentos_parser.url

    def verifica(self):
        
        req = requests.get(self)
        status = req.status_code
        if status == 200:
            print(Fore.BLUE + f"VERIFICA ACESSO")
            print(Fore.BLUE + f"Status UP -",status,"\n")
        else:
            print(Fore.RED + f"URL Inacessível",status,"\n")

    def click_jacking(self):
        
        req = requests.get(self)
        header = req.headers
        #print(Fore.BLUE + f"REPORT SCAN\n")
        data = datetime.now()
        print(Fore.BLUE + f"SCAN EXECUTADO EM:",data)
        print(Fore.BLUE + f"RESULTADO DO SCAN\n")
        if ('X-Frame-Options') in header:
            print (Fore.GREEN + f'[+]' + Fore.WHITE + f'X-Frame-Options:' + req.headers['X-Frame-Options'])
        else:
            print (Fore.RED + f'[-]' + Fore.WHITE + f'X-Frame-Options não definido. Vulnerável a ataques de Clickjacking')

    def x_xss(self):
    
        req = requests.get(self)
        header = req.headers
        if ('X-XSS-Protection') in header and req.headers['X-XSS-Protection'] == '1; mode=block':
            print (Fore.GREEN + f'[+]' + Fore.WHITE + f'X-XSS-Protection:' + req.headers['X-XSS-Protection'])
        else:
            print (Fore.RED + f'[-]' + Fore.WHITE + f'X-XSS-Protection não definido. Vulnerável a ataques de XSS')

    def transport_security(self):
        
        req = requests.get(self)
        header = req.headers
        if ('Strict-Transport-Security') in header:
            print (Fore.GREEN + f'[+]' + Fore.WHITE + f'Strict-Transport-Security:' + req.headers['Strict-Transport-Security'])
        else:
            print (Fore.RED + f'[-]' + Fore.WHITE + f'Strict-Transport-Security não definido. Vulnerável a ataques de MITM')

    def content_type(self):
    
        req = requests.get(self)
        header = req.headers
        if ('X-Content-Type-Options') in header and req.headers['X-Content-Type-Options'] == 'nosniff':
            print (Fore.GREEN + f'[+]' + Fore.WHITE + f'X-Content-Type-Options:' + req.headers['X-Content-Type-Options'])
        else:
            print (Fore.RED + f'[-]' + Fore.WHITE + f'X-Content-Type-Options não tem proteção anti-MIME-Sniffing')


    def security_policy(self):
    
        req = requests.get(self)
        header = req.headers
        if ('Content-Security-Policy') in header:
            print (Fore.GREEN + f'[+]' + Fore.WHITE + f'Content-Security-Policy:' + req.headers['Content-Security-Policy'])
        else:    
            print (Fore.RED + f'[-]' + Fore.WHITE + f'Content-Security-Policy não definido. Vulnerável a ataques de injeção de códigos')    

    def discovery_server(self):
    
        req = requests.get(self)
        header = req.headers['Server']
        if re.search(re.compile('[a-m]'), header):
            print (Fore.RED + f'[-]' + Fore.WHITE + f'Server:' + req.headers['Server'] +' -- A versão do servidor está exposta')
        elif not re.search(re.compile('[a-m]'), header):
            print (Fore.GREEN + f'[+]' + Fore.WHITE + f'Server:' + req.headers['Server'] +' -- A versão do servidor não está exposta')
        else:
            print (Fore.GREEN + f'[-]' + Fore.WHITE + f'Server não está configurado no cabeçalho HTTP')


    def identify_framework(self):
    
        req = requests.get(self)
        header = req.headers
        if ('X-Powered-By') in header:
            print (Fore.RED + f'[-]' + Fore.WHITE + f'X-Powered-By: o framework está exposto')
        else: 
            print (Fore.GREEN + f'[+]' + Fore.WHITE + f'X-Powered-By: o framework não está configurada no cabeçalho HTTP')


    def asp_net(self):
    
        req = requests.get(self)
        header = req.headers
        if ('X-AspNet-Version') in  header:
            print (Fore.RED + f'[-]' + Fore.WHITE + f'X-AspNet-Version:' + req.headers['X-AspNet-Version'] +'-- a versão do ASP.NET está exposta')
        else:
            print (Fore.GREEN + f'[+]' + Fore.WHITE + f'X-AspNet-Version não está configurado\n')


verifica(url)
click_jacking(url)
x_xss(url)
transport_security(url)
content_type(url)
security_policy(url)
discovery_server(url)
identify_framework(url)
asp_net(url)

print (Fore.BLUE + f'[+++]' + 'Melhore a segurança do cabeçalho HTTP')
print (Fore.BLUE + f'[+++]' + 'Faça as correções dos pontos vulneráveis')
