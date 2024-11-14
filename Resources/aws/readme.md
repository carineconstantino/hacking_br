## Recon 

### configure as credenciais
```
aws configure --profile [name]
```
### ver as credenciais 
```
aws sts get-caller-identity --profile [name]
```
### listar usuários
```
aws iam list-users --profile [name]
```
### ver os grupos do usuário 
```
aws iam list-groups-for-user --user-name [username] --profile [name]
```
### ver a "managed policy" para o usuário 
```
aws iam list-attached-user-policies --user-name [username] --profile [name]
```
### ver a “inline policy” para o usuário
```
aws iam list-user-policies --user-name [username] --profile [name]
```
### listar grupos 
```
aws iam list-groups --profile [nome]
```
### ver os membros do grupo
```
aws iam list-group-policies --group-name [nome-do-grupo]
```
### ver a “managed policy” adicionada ao grupo
```
aws iam list-attached-group-policies --group-name [group-name]
```
### listar os nomes das “inline policies” adicionadas ao grupo
```
aws iam list-group-policies --group-name [group-name]
```
### ver todas as aws “roles” (funções) em uma conta
```
aws iam list-roles --profile [profile-name]
```
## ver todas as “managed policies” adicionadas a IAM role
```
aws iam list-attached-role-policies --role-name [ role-name]
```
### ver todas as “inline policies” adicionadas a IAM role 
```
aws iam list-role-policies --role-name [ role-name]
```
### ver todas as policies 
```
aws iam list-policies --profiles [profile-name]
```
### retona informação sobre uma “managed policy” específica
```
aws iam get-policy --policy-arn [policy-arn]
```
### retorna as versões de uma “managed policy” específica
```
aws iam list-policy-versions --policy-arn [policy-arn]
```
### ver as permissões em uma versão específica de uma policy
```
aws iam get-policy-version --policy-arn policy-arn --version-id [version-id]
```
### retorna as permissões (document) em uma “inline policy”

user
```
aws iam get-user-policy --user-name user-name --policy-name [policy-name] --profile [profile-name]
```
group
```
aws iam get-group-policy --group-name group-name --policy-name [policy-name] --profile [profile-name]
```
role
```
aws iam get-role-policy --role-name role-name --policy-name [policy-name] --profile [profile-name]
```
