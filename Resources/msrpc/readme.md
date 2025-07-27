## MSRPC
<p>A Microsoft Remote Procedure Call (MSRPC) é um protocolo de comunicação usado para solicitar um serviço de um programa localizado em outro computador na rede. Em outras palavras, o MSRPC é usado para chamar outros processos em sistemas remotos como se estivessem sendo chamados do sistema local. Isso é realizado usando o modelo "cliente-servidor" ou "request-response".
Especificamente, um RPC é iniciado pelo cliente, que envia uma mensagem de solicitação a um servidor remoto conhecido para executar um procedimento especificado com parâmetros fornecidos.</p>

<p>O RPC pode ser acessado através da porta TCP e UDP 135, por meio de SMB (pipe) usando uma sessão nula ou autenticada (TCP 139 e 445) e, como um serviço da web, ouvindo a porta TCP 593. Além disso, é comum encontrar portas RPC abertas em 49xxx.</p>

<p>O serviço MSRPC usa mecanismos IPC, como pipes, netbios ou winsock, para estabelecer comunicação entre o cliente e o servidor. Os protocolos IPC$ Transport, TCP, UDP e HTTP são usados para fornecer acesso aos serviços. É importante entender quando se trata do MSRCP sobre SMB.</p>

### Basic
```
nmap --script msrpc-enum -p 135 <target-ip>
```

### Enumerating RPC Endpoints – rpcdump.py
<p>O script do Impacket rpcdump.py interage com o RPC para listar serviços e endpoints. Isso nos permite catalogar serviços interessantes que usam TCP, UDP, HTTP e pipes SMB.</p>

- O RPC é acessado usando os seguintes protocolos:
    - ncacn_ip_tcp — TCP port 135
    - ncadg_ip_udp — UDP port 135
    - ncacn_http — RPC over HTTP via TCP port 80, 593, and others
    - ncacn_np — the \pipe\epmapper named pipe via SMB

