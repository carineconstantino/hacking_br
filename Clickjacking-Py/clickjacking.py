from flask import Flask, render_template_string, request, session
import requests
import re
from urllib.parse import urlparse, urljoin

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Defina uma chave secreta para as sessões

# Função para corrigir URLs relativas
def ajustar_urls_relativas(html, base_url):
    """
    Corrige URLs relativas no conteúdo HTML.
    """
    # Expressões regulares para encontrar os links href e src relativos e substituí-los pela URL absoluta.
    padroes = [
        # Corrige href e src relativos
        (r'(href|src)=["\']/([^"\']+)["\']', r'\1="' + base_url + r'/\2"')
    ]

    # Aplica os padrões para corrigir os links relativos
    for padrao, substituicao in padroes:
        html = re.sub(padrao, substituicao, html)

    return html

@app.route('/', methods=['GET', 'POST'])
def index():
    page_content = ""
    if request.method == 'POST':
        url = request.form.get('url')  # Obtém a URL do campo do formulário
        if url:
            # Armazenando a URL na sessão
            session['url'] = url
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Referer': 'https://www.google.com'
            }

            # Fazendo a requisição HTTP para a URL
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                # Corrigindo os links relativos da página
                base_url = urlparse(url).scheme + "://" + urlparse(url).hostname
                print("base url", base_url)
                page_content = ajustar_urls_relativas(response.text, base_url)
                print("page", page_content)
            else:
                page_content = f"Erro ao carregar a página: {response.status_code}"
        else:
            page_content = "Por favor, insira uma URL válida."

    return render_template_string("""
        <html>
            <head>
                <title>Clickjacking</title>
            </head>
            <style>
                body { 
                    background: #eef3f6;
                    font-family: arial;
                }    
                hr.dashed {
                    border-top: 3px dashed #bbb;
                }
                h1 {
                    color: Red;
                    }
                a {
                    color: red;
                    text-decoration: none;
                  }  
            </style>
            <body>
                <h1 align="center"><strong>Teste - Clickjacking</strong></h1>
                <h3 align="center"><a href="https://hackingbr.com.br">Hacking BR</a></h3>
                <hr class="dashed">

                <!-- Formulário para input da URL -->
                <form method="POST" action="/">
                    <label for="url">Digite a URL:</label>
                    <input type="text" id="url" name="url" placeholder="Digite a URL aqui" required>
                    <button type="submit">Carregar</button>
                </form>
                    <a href="/log"><button>Ver Log</button></a>  <a href="/"><button>Clear</button></a>
                <hr class="dashed">

                <!-- Exibindo conteúdo no iframe
                {% if page_content %}
                    <iframe srcdoc='{ page_content }'></iframe>
                {% endif %}-->
                <div><iframe srcdoc='{{ page_content }}' width="100%" height="800px" style="border:none;"></iframe></div>
            </body>
        </html>
    """, page_content=page_content)

@app.route('/log', methods=['GET', 'POST'])
def log():
    prepared_url = ""
    # Recupera a URL da sessão, se existir
    url = session.get('url')

    if url:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': 'https://www.google.com'
        }

        # Fazendo a requisição HTTP para a URL
        req = requests.Request("GET", url, headers=headers)
        prepared = req.prepare()
        prepared_url = prepared.url
        prepared_method = prepared.method
        prepared_headers = prepared.headers
        prepared_body = prepared.body

        # Corrigindo os links relativos da página
        #base_url = urlparse(url).scheme + "://" + urlparse(url).hostname
        #prepared_url = ajustar_urls_relativas(prepared.url, base_url)
    else:
        prepared_url = "Nenhuma URL foi fornecida. Por favor, insira uma URL na página principal."

    return render_template_string("""
        <html>
            <head>
                <title>Log da Requisição</title>
            </head>
            <style>
                body {
                    background: #eef3f6;
                    font-family: arial;
                }
                hr.dashed {
                    border-top: 3px dashed #bbb;
                }
                h1 {
                    color: Red;
                    }
                a {
                    color: red;
                    text-decoration: none;
                  }
            </style>

            <body>
                <h1 align="center"><strong>Log da Requisição</strong></h1>
                <hr>

                <form method="POST" action="/log">
                    <!--<label for="url">Digite a URL:</label>
                    <input type="text" id="url" name="url" placeholder="Digite a URL aqui" required>
                    <button type="submit">Ver Log</button>-->
                </form>

                
                <p><strong>URL Preparada:</strong> {{ prepared_url }}</p>
                <p><strong>Método:</strong> {{ prepared_method }}</p>
                <p><strong>Headers:</strong> {{ prepared_headers }}</p>
                <p><strong>Body:</strong> {{ prepared_body }}</p>
                <hr>
                <a href="/"><button>Novo Teste</button></a>
            </body>
        </html>
    """, prepared_url=prepared.url, prepared_method=prepared.method, prepared_headers=prepared.headers, prepared_body=prepared.body)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
