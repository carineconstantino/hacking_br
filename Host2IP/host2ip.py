import subprocess
import pyfiglet

# Banner
titulo = pyfiglet.figlet_format("Host2IP")
print(titulo)
print('Criado por @hackingbr\n')
print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')

def get_ip_address(hostname):
    try:
        # executa o comando hosts para cada url
        result = subprocess.run(['host', hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # verifica se o comando foi executado com sucesso
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"
        
        # verifica na saida do comando o IP 
        output_lines = result.stdout.splitlines()
        for line in output_lines:
            if 'has address' in line:
                return line.split()[-1]
        
        return "No IP address found"
    except Exception as e:
        return f"Exception: {str(e)}"

def main():
    # solicita o nome do arquivo para execução
    filename = input("Arquivo: ")
    
    try:
        # lê o arquivo com a lista de urls
        with open(filename, 'r') as file:
            hostnames = [line.strip() for line in file.readlines()]
        
        # para cada url executa o comando hosts e retorna a url:ip
        for hostname in hostnames:
            ip_address = get_ip_address(hostname)
            print(f"{hostname}: {ip_address}")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
