import argparse
import aiohttp
import asyncio
import pyfiglet
import re
import datetime
from bs4 import BeautifulSoup

titulo = pyfiglet.figlet_format("HTML DIR SCAN")
print(titulo)
print('Criado por @hackingbr\n')
print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')

if __name__ == '__main__':
    program_name = argparse.ArgumentParser(description='HTML DIR SCAN')
    program_name.add_argument('-url', action='store', dest='url',
                              required=True, help='Informe uma URL para executar o scan ::: Exemplo: python3 html_dir_scan.py -url https://example.com.br ')                          
    argumentos_parser = program_name.parse_args()
    base_url = argumentos_parser.url


async def search_dir_in_html(session):
### access url and search for all paths in html code
    async with session.get(base_url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        ### regex to search for paths in html code
        search_dir = set(re.findall(r'/[a-zA-Z]+/', html))
        d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('[+] Data do Scan: ', d)
        print('[+] Directories Found in HTML:\n', search_dir)
        print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')
        print('[+] Testing Directories Access & Brute-Force\n')
        ### index for each path found
        tasks = []
        ## add each path in a index and create a url for each path 
        for x in search_dir:
            tasks.append(test_directory_access(session, base_url + x))
        await asyncio.gather(*tasks)


async def test_directory_access(session, url):
### make a request for each url with path found = http status 200, 301, 302
    try:
        data_log = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
        data_title = str(data_log)
        async with session.get(url) as response:
            if response.status in [200, 301, 302]:
                print('-->Send: ', url)
                print('-->Status: ', response.status)
                with open(data_title + "-wordlist.txt", "a") as output_file:
                    await output_file.write(url + '\n')
                
    except Exception as e:
        Result = str(e)


async def main():
    ### close session created by aiohttp after timout of 60 seconds
    async with aiohttp.ClientSession() as session:
        try:
            await asyncio.wait_for(search_dir_in_html(session), timeout=60)
        except asyncio.TimeoutError:
            print("Timeout reached. Exiting...")
        finally:
            await session.close()


asyncio.run(main())
