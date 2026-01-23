import argparse
import aiohttp
import asyncio
import re
import datetime
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

# banner
banner = '''

	██╗  ██╗████████╗███╗   ███╗██╗         ██████╗ ██╗██████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗
	██║  ██║╚══██╔══╝████╗ ████║██║         ██╔══██╗██║██╔══██╗    ██╔════╝██╔════╝██╔══██╗████╗  ██║
	███████║   ██║   ██╔████╔██║██║         ██║  ██║██║██████╔╝    ███████╗██║     ███████║██╔██╗ ██║
	██╔══██║   ██║   ██║╚██╔╝██║██║         ██║  ██║██║██╔══██╗    ╚════██║██║     ██╔══██║██║╚██╗██║
	██║  ██║   ██║   ██║ ╚═╝ ██║███████╗    ██████╔╝██║██║  ██║    ███████║╚██████╗██║  ██║██║ ╚████║
	╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝╚══════╝    ╚═════╝ ╚═╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
        [ Criado por @hackingbr | https://hackingbr.gitbook.io/hacking-br/ ]
        
'''          

print(Fore.RED + banner)                                                                                       

# argumentos
if __name__ == '__main__':
    program_name = argparse.ArgumentParser(description='HTML DIR SCAN')
    program_name.add_argument('-url', action='store', dest='url',
                              required=True, help='Informe uma URL para executar o scan ::: Exemplo: python3 html_dir_scan.py -url https://example.com.br ')                          
    argumentos_parser = program_name.parse_args()
    base_url = argumentos_parser.url


async def search_dir_in_html(session):
### acessa a url e faz o 'parser' da resposta 
    async with session.get(base_url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        ### regex para buscar por diretório, ex: /path/
        search_dir = set(re.findall(r'/[a-zA-Z]+/', html))
        d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(Fore.GREEN + f"[+] Data do Scan: ", d)
        print('[+] Directories Found in HTML:\n', search_dir)
        print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')
        print('[+] Testing Directories Access & Brute-Force\n')
        ### index para cada diretório encontrado
        tasks = []
        ## adiciona cada diretórios no index e cria a url para cada um
        for x in search_dir:
            tasks.append(test_directory_access(session, base_url + x))
        await asyncio.gather(*tasks)


async def test_directory_access(session, url):
### faz a requisição para cada diretório encontrado, filtro para os status 200, 301, 302, 404, 401, 500
    try:
        data_log = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
        data_title = str(data_log)
        async with session.get(url) as response:
            if response.status in [200, 301, 302, 404, 401, 500]:
                print('-->Send: ', url)
                print('-->Status: ', response.status)
                with open(data_title + "-wordlist.txt", "a") as output_file:
                    await output_file.write(url + '\n')
                
    except Exception as e:
        Result = str(e)


async def main():
    ### fecha a sessão criado pelo aiohttp depois de um timeout de 60 seconds
    ### isso evita que o scrit demore pois espera uma resposta da requisição
    async with aiohttp.ClientSession() as session:
        try:
            await asyncio.wait_for(search_dir_in_html(session), timeout=60)
        except asyncio.TimeoutError:
            print("Timeout reached. Exiting...")
        finally:
            await session.close()


asyncio.run(main())
