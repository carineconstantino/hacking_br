#!/usr/bin/env python3
import re
import sys
import requests
from collections import defaultdict
from datetime import datetime
from colorama import init, Fore, Back, Style

# Banner
# Link para criar o banner: https://patorjk.com/software/taag/
banner = '''

	     ██╗███████╗    ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗
	     ██║██╔════╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║
	     ██║███████╗    ███████╗█████╗  ███████║██████╔╝██║     ███████║
	██   ██║╚════██║    ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║
	╚█████╔╝███████║    ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║
	 ╚════╝ ╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
        [ Criado por @hackingbr | https://hackingbr.gitbook.io/hacking-br/ ]
        
'''

print(Fore.RED + banner)                                                 

# =========================
# REGEX DE SECRETS
# =========================
_regex = {
    'google_api'     : r'AIza[0-9A-Za-z-_]{35}',
    'firebase'  : r'AAAA[A-Za-z0-9_-]{7}:[A-Za-z0-9_-]{140}',
    'google_captcha' : r'6L[0-9A-Za-z-_]{38}|^6[0-9a-zA-Z_-]{39}$',
    'google_oauth'   : r'ya29\.[0-9A-Za-z\-_]+',
    'amazon_aws_access_key_id' : r'A[SK]IA[0-9A-Z]{16}',
    'amazon_mws_auth_toke' : r'amzn\.mws\.[0-9a-f\-]{36}',
    'amazon_aws_url' : r's3\.amazonaws.com[/]+|[a-zA-Z0-9_-]*\.s3\.amazonaws.com',
    'amazon_aws_url2' : r"([a-zA-Z0-9\-\._]+\.s3\.amazonaws\.com|"
                         r"s3://[a-zA-Z0-9\-\._]+|"
                         r"s3-[a-zA-Z0-9\-\._\/]+|"
                         r"s3.amazonaws.com/[a-zA-Z0-9\-\._]+|"
                         r"s3.console.aws.amazon.com/s3/buckets/[a-zA-Z0-9\-\._]+)",
    'facebook_access_token' : r'EAACEdEose0cBA[0-9A-Za-z]+',
    'authorization_basic' : r'basic [a-zA-Z0-9=:_\+\/-]{5,100}',
    'authorization_bearer' : r'bearer [a-zA-Z0-9_\-\.=:_\+\/]{5,100}',
    'authorization_api' : r'api[key|_key|\s+]+[a-zA-Z0-9_\-]{5,100}',
    'mailgun_api_key' : r'key-[0-9a-zA-Z]{32}',
    'twilio_api_key' : r'SK[0-9a-fA-F]{32}',
    'twilio_account_sid' : r'AC[a-zA-Z0-9_\-]{32}',
    'twilio_app_sid' : r'AP[a-zA-Z0-9_\-]{32}',
    'paypal_braintree_access_token' : r'access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}',
    'square_oauth_secret' : r'sq0csp-[0-9A-Za-z\-_]{43}|sq0[a-z]{3}-[0-9A-Za-z\-_]{22,43}',
    'square_access_token' : r'sqOatp-[0-9A-Za-z\-_]{22}|EAAA[a-zA-Z0-9]{60}',
    'stripe_standard_api' : r'sk_live_[0-9a-zA-Z]{24}',
    'stripe_restricted_api' : r'rk_live_[0-9a-zA-Z]{24}',
    'github_access_token' : r'[a-zA-Z0-9_-]*:[a-zA-Z0-9_\-]+@github\.com',
    'rsa_private_key' : r'-----BEGIN RSA PRIVATE KEY-----',
    'ssh_dsa_private_key' : r'-----BEGIN DSA PRIVATE KEY-----',
    'ssh_ec_private_key' : r'-----BEGIN EC PRIVATE KEY-----',
    'pgp_private_block' : r'-----BEGIN PGP PRIVATE KEY BLOCK-----',
    'json_web_token' : r'ey[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_.+/=]*',
    'slack_token' : r'xox[a-zA-Z]-[a-zA-Z0-9-]+',
    'SSH_privKey' : r'BEGIN [A-Z ]+ PRIVATE KEY',
    'Heroku API KEY' : r'[0-9a-fA-F\-]{36}',
    'possible_Creds' : r'(?i)(password\s*[`=:\"]+\s*[^\s]+|'
                       r'password is\s*[`=:\"]*\s*[^\s]+|'
                       r'pwd\s*[`=:\"]*\s*[^\s]+|'
                       r'passwd\s*[`=:\"]+\s*[^\s]+)'
}

# =========================
# REGEX DE LINKS / URLS
# =========================
JS_LINK_REGEX = r"""
(?:"|')
(
  (
    (?:[a-zA-Z]{1,10}://|//)
    [^"'/]{1,}\.
    [a-zA-Z]{2,}[^"']{0,}
  )
  |
  (
    (?:/|\.\./|\./)
    [^"'><,;| *()(%%$^/\\\[\]]
    [^"'><,;|()]{1,}
  )
  |
  (
    [a-zA-Z0-9_\-/]{1,}/
    [a-zA-Z0-9_\-/.]{1,}
    \.(?:[a-zA-Z]{1,4}|action)
    (?:[\?|#][^"|']{0,}|)
  )
  |
  (
    [a-zA-Z0-9_\-/]{1,}/
    [a-zA-Z0-9_\-/]{3,}
    (?:[\?|#][^"|']{0,}|)
  )
  |
  (
    [a-zA-Z0-9_\-]{1,}
    \.(?:php|asp|aspx|jsp|json|action|html|js|txt|xml)
    (?:[\?|#][^"|']{0,}|)
  )
)
(?:"|')
"""

# =========================
def fetch_js(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0"}
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return r.text

def scan_secrets(content):
    findings = defaultdict(set)
    for name, pattern in _regex.items():
        for match in re.findall(pattern, content):
            findings[name].add(match)
    return findings

def scan_links(content):
    links = set()
    matches = re.findall(JS_LINK_REGEX, content, re.VERBOSE)
    for match in matches:
        for group in match:
            if group:
                links.add(group)
    return links

def export_html(results):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    str_current_datetime = str(date)
    filename = f"js_sensitive_bulk_report.{str_current_datetime}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        	f.write('\n'.join(results))

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Javascripts Secrets & Links Report</title>
<style>
body {{ background:#020617; color:#e5e7eb; font-family:Arial; padding:20px }}
h1 {{ color:#38bdf8 }}
h2 {{ color:#f87171 }}
h3 {{ color:#22c55e }}
pre {{ background:#020617; padding:10px; color:#22c55e }}
.card {{ margin-bottom:30px; border-left:4px solid #ef4444; padding-left:15px }}
.url {{ color:#60a5fa; word-break:break-all }}
</style>
</head>
<body>

<h1>JavaScripts Secrets & Link Discovery</h1>
<p><b>Date:</b> {date}</p>
<hr>
"""

    for url, data in results.items():
        html += f"<div class='card'><div class='url'><b>URL:</b> {url}</div><br>"

        secrets = data.get("secrets", {})
        links = data.get("links", set())

        if secrets:
            html += "<h2>Secrets</h2>"
            for k, vals in secrets.items():
                html += f"<h3>{k}</h3>"
                for v in vals:
                    html += f"<pre>{v}</pre>"

        if links:
            html += "<h2>Discovered Links</h2>"
            for l in sorted(links):
                html += f"<pre>{l}</pre>"

        if not secrets and not links:
            html += "<i>Nenhuma informação encontrada</i>"

        html += "</div>"

    html += "</body></html>"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(Fore.GREEN + f"[+] Relatório HTML gerado: {filename}")

def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} [url-file-name].txt")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        urls = [u.strip() for u in f if u.strip()]

    results = {}

    for url in urls:
        print(Fore.GREEN + f"[+] Analisando {url}")
        try:
            content = fetch_js(url)
            results[url] = {
                "secrets": scan_secrets(content),
                "links": scan_links(content)
            }
        except Exception as e:
            print(f"[-] Erro: {e}")
            results[url] = {}

    export_html(results)

if __name__ == "__main__":
    main()
