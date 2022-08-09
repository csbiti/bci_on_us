# mail_BCI_ON_US

**ticket:** 78590 (https://glpi.csb.nc/front/ticket.form.php?id=78590)<br />
**Git:** https://github.com/csbiti/bci_on_us <br />
**version:** 0.0.1 <br />
**is on:** SRVOEM41 () <br />
**SRV:** SMAILS (192.168.201.242) <br />
**DB:** BOB12 (192.168.201.242:2328/BOB) <br />
**docker_img:** None <br />
**github_actions:** 0 <br />
**testing:** None

## Summary

Envoi un rapport par mail quotidien à la BCI contenant:<br />
retrait porteur bci<br />
Retraits porteurs francais hors bci <br />
Retraits porteurs étrangers <br />

## Requirements
cx_Oracle installé sur le serveur https://oracle.github.io/python-cx_Oracle/

## Quick start

    python mail_to_BCI_main.py TO=xxx@xx.xx CC=xxx@xx.xx,xxx@xx.xx PASSWORD_DB=**** PASSWORD_SMAILS=**** CONFIG=local-test
    
**TO** pour les adresses mail de récéptions sparés par une virgule <br />
**CC** pour les adresses en copie (séparées par une virgule) <br />
**PASSWORD_DB** le mdp à la BDD BOB12 <br />
**PASSWORD_SMAILS** le mdp au serveur SMAILS <br /> 
**CONFIG** le type de configuration, trois options (local-test, SRV-test, SRV-prod) <br /> 

## Doc

Pour plus de lisibilité, le projet garde dans des scripts séparés les modèles pour la construction du mail en html (first_table.py, second_table.py et outro.py dans l'ordre du html) et les requetes SQL pour récupérer les donnéees (request.py) le script principal étant mail_to_BCI

## TODO 
- change the contact mail to the true one <br /> 

