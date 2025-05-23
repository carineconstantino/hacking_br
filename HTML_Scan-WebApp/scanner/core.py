import requests
import bs4
import re
import socket
from urllib.parse import urlparse, urljoin
import datetime
import streamlit as st



# Regex para encontrar domínios com TLDs
tld_regex = re.compile(
    r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:dev|stg|prod|local|com|net|org|edu|gov|mil|biz|xyz|co|us)\b'
)

# Regex para encontrar endereço ip
ip_regex = re.compile(
    r'\b(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'  # First octet
    r'(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'     # Second octet
    r'(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'     # Third octet
    r'(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\b'     # Fourth octet
)

# Regex para encontrar credencial no JavaScript
leak_creds_regex = re.compile(
    r'(?i)((database|api_key|username|password|access_key|access_token|admin_pass|admin_user|algolia_admin_key|algolia_api_key|alias_pass|alicloud_access_key|amazon_secret_access_key|amazonaws|ansible_vault_password|aos_key|api_key_secret|api_key_sid|api_secret|api.googlemaps AIza|apidocs|apikey|apiSecret|app_debug|app_id|app_key|app_log_level|app_secret|appkey|appkeysecret|application_key|appsecret|appspot|auth_token|authorizationToken|authsecret|aws_access|aws_access_key_id|aws_bucket|aws_key|aws_secret|aws_secret_key|aws_token|AWSSecretKey|b2_app_key|bashrc password|bintray_apikey|bintray_gpg_password|bintray_key|bintraykey|bluemix_api_key|bluemix_pass|browserstack_access_key|bucket_password|bucketeer_aws_access_key_id|bucketeer_aws_secret_access_key|built_branch_deploy_key|bx_password|cache_driver|cache_s3_secret_key|cattle_access_key|cattle_secret_key|certificate_password|ci_deploy_password|client_secret|client_zpk_secret_key|clojars_password|cloud_api_key|cloud_watch_aws_access_key|cloudant_password|cloudflare_api_key|cloudflare_auth_key|cloudinary_api_secret|cloudinary_name|codecov_token|config|conn.login|connectionstring|consumer_key|consumer_secret|credentials|cypress_record_key|database_password|database_schema_test|datadog_api_key|datadog_app_key|db_password|db_server|db_username|dbpasswd|dbpassword|dbuser|deploy_password|digitalocean_ssh_key_body|digitalocean_ssh_key_ids|docker_hub_password|docker_key|docker_pass|docker_passwd|docker_password|dockerhub_password|dockerhubpassword|dot-files|dotfiles|droplet_travis_password|dynamoaccesskeyid|dynamosecretaccesskey|elastica_host|elastica_port|elasticsearch_password|encryption_key|encryption_password|env.heroku_api_key|env.sonatype_password|eureka.awssecretkey)[a-z0-9_ .\-,@]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}["\']([0-9a-zA-Z\-_=@!#\$%\^&\*\(\)\+\[\]\{\}\|;:,<>\?~`]{1,64})["\']'
)

# Regex para encontrar cookies no JavaScript
cookie_regex = re.compile(r'document\.cookie\s*=\s*["\']([^"\']+)["\'];', re.IGNORECASE)

# Regex para encontrar localStorage no JavaScript
local_storage_regex = re.compile(r'localStorage\.setItem\s*\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']\s*\)', re.IGNORECASE)

# Header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def extract_data(url, extract_options):
    try:
        js_file = url.endswith('.js')
        
        if ".js" in url:
            url = url.split(".js")[0] + ".js"
            js_file = url
         
        links = []  # Initialize links
        images = []  # Initialize images
        cookies = []  # Initialize cookies
        cookie_strings = []  # Initialize cookie_strings
        forms = []  # Initialize forms

        if js_file:
            scripts = [url]
        else:
            scripts = []
            # GET request 
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Trata HTTPError para respostas (4xx and 5xx)
            # Faz o Parsing do conteúdo HTML 
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extrai os links
            links = []
            links = [urljoin(url, link.get('href')) for link in soup.find_all(['a', 'link']) if link.get('href')]
            # Extrai URLs de imagem
            images = [urljoin(url, img.get('src')) for img in soup.find_all('img') if img.get('src')]
            # Extrai cookies
            cookies = response.cookies
            cookie_strings = [f"{cookie.name}={cookie.value}" for cookie in cookies]
            # Extrai formularios e campos de input
            forms = []
            for form in soup.find_all('form'):
                form_data = {'action': form.get('action'), 'method': form.get('method'), 'inputs': []}
                for input_tag in form.find_all('input'):
                    input_data = {
                    'name': input_tag.get('name'),
                    'type': input_tag.get('type'),
                    'value': input_tag.get('value'),
                }
                form_data['inputs'].append(input_data)
                forms.append(form_data)
                # Extrai URLs/domains/subdomains/IPs de scripts JS
                scripts = [urljoin(url, script.get('src')) for script in soup.find_all('script') if script.get('src')]
        
        js_urls = set()  # Usa "set" para evitar urls duplicadas 
        potential_domains = set()
        potential_ips = set()
        leaked_creds = []
        cookies_js = []
        local_storage = []

        for script in scripts:
            hostname = urlparse(script).hostname
            try:
                # Acessa o conteúdo do script JS
                js_response = requests.get(script, headers=headers)
                js_response.raise_for_status()
                js_content = js_response.text

                # Extrai URLs com http or https
                js_urls.update(re.findall(r'https?://[^\s\'"<>]+', js_content))

                # Extrai dominios, subdominios e endereço IP
                potential_domains.update(re.findall(tld_regex, js_content))
                potential_ips.update(re.findall(ip_regex, js_content))

                # Busca credencial
                leaked_creds.extend(leak_creds_regex.findall(js_content))

                # Extrai cookies
                cookies_js = cookie_regex.findall(js_content)

                # Extrai localStorage 
                local_storage = local_storage_regex.findall(js_content)
             
            except requests.RequestException as e:
                st.warning(f"Could not fetch {script}: {e}")

        result = {}
        if extract_options['links']:
            result['links'] = links
        if extract_options['images']:
            result['images'] = images
        if extract_options['cookies']:
            result['cookies'] = cookie_strings
        if extract_options['forms']:
            result['forms'] = forms
        if extract_options['js_urls']:
            result['js_urls'] = list(js_urls)
        if extract_options['domains']:
            result['domains'] = list(potential_domains)
        if extract_options['ips']:
            result['ips'] = list(potential_ips)
        if extract_options['leaked_creds']:
            result['leaked_creds'] = leaked_creds
        if extract_options['cookies_js']:
            result['cookies_js'] = cookies_js
        if extract_options['local_storage']:
            result['local_storage'] = local_storage

        return result

    except requests.ConnectionError:
        st.error("Connection Error")
        return None
    except requests.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        st.error(f"An error occurred: {err}")
        return None
