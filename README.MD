## ONBOARDING US UPDATE SIGNATURE W8 BEN DOCUMENT
#### _FISSION PARA ATUALIZAÇÃO DE ASSINATURA DO DOCUMENTO W8 BEN
___
### Esse projeto refere-se a rota do Sphinx:

```
UserService.update_w8_form_confirmation
```
&nbsp; 
### 1.1. `update-w8-ben-signature`
&nbsp; 
#### MODELO DE REQUISIÇÃO:

```http://127.0.0.1:9000/update-w8-ben-signature```

&nbsp; 
##### BODY REQUEST
```
{
  "w8_form_confirmation": true
    }
```
&nbsp;

#### MODELO DE RESPOSTA:

```
{
    "result": true,
    "message": "The W8 Form Was Updated Successfully",
    "success": true,
    "code": 0
}
```
&nbsp;
#### RODAR SCRIPT DE TESTS:

- No mesmo nível da pasta root, rodar o seguinte comando no terminal: `bash tests.sh`

&nbsp;