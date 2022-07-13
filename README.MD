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
  "w8_confirmation": true
    }
```
&nbsp;

#### MODELO DE RESPOSTA:

```
{
    "result": null,
    "message": "update_w8_form_confirmation::sent_to_persephone:false",
    "success": false,
    "code": 60
}
```
&nbsp;
#### RODAR SCRIPT DE TESTS:

- No mesmo nível da pasta root, rodar o seguinte comando no terminal: `bash tests.sh`

&nbsp;