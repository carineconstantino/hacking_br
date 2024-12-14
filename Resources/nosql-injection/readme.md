# NoSQL Injection

<p>:fries: NoSQL Injection é quando um atacante manipula consultas para bancos de dados NoSQL através de um "ponto de entrada" na aplicação.
Base de dados NoSQL possuem um modelo de armazenamento e recuperação de dados diferente dos tradicionais bancos de dados relacionais. São reconhecidos como bases mais flexíveis e escaláveis atendendo a demanda por armazenamento de dados não-relacionais. 
Tipos de bases de dados NoSQL: armazenamento de documentos (MongoDB), armazenamento no formato "chave-valor" (key-value) (Redis), armazenamento de grande volume de dados em coluna (Cassandra), e armazenamento do tipo Graph (Neo4j). 
Flexibilidade: o schema da base de dados não é fixa, permitindo mudar a estrutura dos dados. 
Escalabilidade: são escaláveis em arquiteturas distribuidas.
Casos de Uso: Aplicações Big Data, serviços de "Real-time", dispositivos IoT, etc</p>

- Mongo Playground para testar consultas e códigos: https://mongoplayground.net/
- Mongo Cheatsheet: https://www.mongodb.com/developer/products/mongodb/cheat-sheet/
- NoSQL Scanner: extensão do Burp Suite para detectar automaticamente pontos de injeção.

:fries:Checklist

- Qual é a base de dados NoSQL usada pela aplicação (MongoDB, CounchDB, etc)?
- Identifique os "pontos de entrada":
    - Parâmetros na URL
    - Campos de formulário
    - Cabeçalho HTTP (ex.: cookies)
    - Out-of-band (quando os dados são retornados a partir de uma "origem" externa)
- Teste nos "pontos de entrada", diferentes operadores:
    - $eq (iguais)
    - $ne (não igual)
    - $gt (maior que '>')
    - $gte (maior ou igual)
    - $lt (menor que '<')
    - $lte (menor ou igual)
- É possível "forçar" respostas diferentes quando um "ponto de entrada" é manipulado?
- Teste se é possível fazer o "bypass" de login usando os operadores NoSQL
- Teste se a aplicação é vulnerável a "blind NoSQLi"
- Analise as mensagens de erro
- Teste payloads para ataques de "time delay"
- Teste encode e ofuscação para fazer o "bypass" de filtros e bloqueios
