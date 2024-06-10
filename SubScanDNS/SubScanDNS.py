import dns.resolver
import argparse
import pyfiglet
from tabulate import tabulate
import datetime
import subprocess

# Banner
titulo = pyfiglet.figlet_format("SubScanDNS")
print(titulo)
print('Criado por @hackingbr\n')
print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')

# Argumentos
if __name__ == '__main__':
    program_name = argparse.ArgumentParser(description='SubScanDNS')
    program_name.add_argument('-domain', action='store', dest='domain',
                              required=True, help='Informe um domínio para executar o scan ::: Exemplo: python3 SubScanDNS.py -domain example.com.br')
    argumentos_parser = program_name.parse_args()
    base_domain = argumentos_parser.domain

    def enumRun():
        resolver = dns.resolver.Resolver()
        file_path = "subdomains.txt"
        results = []
        private_ip_count = 0  # contador para resultado com IP privado

        try:
            with open(file_path, 'r') as open_file:
                for line in open_file:
                    subdomain = line.strip()
                    if subdomain:  # verifica se o arquivo não esta vazio
                           try:
                                resolver.nameservers = ['8.8.8.8', '8.8.4.4'] # define os servidores DNS
                                full_domain = f'{subdomain}.{base_domain}' # define a estrutura para fazer a consulta DNS
                                enum = resolver.resolve(full_domain, 'A') # faz a consulta DNS para registros A
                                for rdata in enum:
                                      result = [full_domain, str(rdata)] # retorna o resultado da consulta
                                      # constroi o comando host para cada subdominio
                                      command = ['host', full_domain]
                                      # executa o comando
                                      check = subprocess.run(command, capture_output=True, text=True, check=True)
                                      # adiciona o resultado para o output
                                      results.append([full_domain, str(rdata), check.stdout.strip()])
                                      ip_address = rdata.address  # verifica se o IP é privado no output do comando hosts
                                      if ip_address.startswith(('10.', '172.', '192.168.')):
                                      	private_ip_count += 1
                                      else:
                                      	private_ip_count = 0  # interrompe a execução se o IP privado retorna 10x consecutivas
                                      if private_ip_count >= 10:
                                          print("[+] Stop :: Resolução DNS retorna IP privado.")
                                          return results
                           except dns.resolver.NXDOMAIN:
                               pass
                           except dns.resolver.NoAnswer:
                               pass
                           except dns.exception.Timeout:
                               pass
                           except dns.resolver.NoNameservers:
                               pass
                           except dns.resolver.YXDOMAIN:
                               pass
                           except dns.exception.DNSException as e:
                               pass
        except FileNotFoundError:
            print(f"File {file_path} not found.")
 
        if results:
            # print do resultado no formato tabela
            print(tabulate(results, headers=["Subdomain", "Resolved IP", "Lookup Description"], tablefmt="grid"))
            # variaveis de data e hora e de formatação para data/hora
            d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            str_current_datetime = str(d)

        # html para o relatorio
            html_content = """
            <html>
            <head>
                <title>SubEnum Results</title>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    table, th, td {
                        border: 1px solid black;
                    }
                    th, td {
                        padding: 15px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h2>SubEnum Results</h2>
                <table>
                    <tr>
                        <th>Subdomain</th>
                        <th>Resolved IP</th>
                        <th>Lookup Description</th>
                    </tr>"""
            for result in results:
                html_content += f"""
                    <tr>
                        <td>{result[0]}</td>
                        <td>{result[1]}</td>
                        <td>{result[2]}</td>
                    </tr>"""
            html_content += """
                </table>
            </body>
            </html>"""
            # cria o relatorio em html
            with open(str_current_datetime + "- SubScanDNS-Results.html", "w") as html_file:
                html_file.write(html_content)
            # informa que o relatorio foi salvo    
            print("\nResultado salvo no arquivo HTML"+str_current_datetime+"-SubScanDNS-Results.html")

    enumRun()
