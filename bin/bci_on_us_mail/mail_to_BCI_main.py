# -*- coding: UTF-8 -*-

# Git: https://github.com/csbiti/bci_on_us

"""
- Ticket 78590
Envoi un rapport par mail quotidien à la BCI contenant:
retrait porteur bci
Retraits porteurs francais hors bci
Retraits porteurs étrangers

python "C:/Users/guetec/OneDrive - CSB/Documents/projets/BCI_ON_US/bin/mail.py" TO=colin.guetemme@live.fr CC=guetec@csb.nc,colin.guetemme@live.fr CODEBANQUE=18319 USER_DB=bob PASSWORD_DB=**** PASSWORD_SMAILS=****
python "/csb/bin/mail_to_BCI_main.py" TO= CC= USER_DB=bob PASSWORD_DB=**** PASSWORD_SMAILS=**** config=SRV-prod
"""

from time import strftime
import cx_Oracle
import datetime
import json
import os
import sys
import subprocess

from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

# FILES #
import requests_bci
import first_table
import second_table
import outro

#---------------------#
# CONFIGURATION #
#---------------------#

DIRNAME = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(DIRNAME, '../../cfg/bci_on_us_mail.json')

with open(CONFIG_FILE, 'r') as file:
    CONFIG = json.load(file)

REPSCRIPT = os.path.abspath(os.path.split(__file__)[0])
NOM_SCRIPT = os.path.splitext(os.path.split(__file__)[1])[0]

TODAY = datetime.datetime.now().strftime("%d/%m/%y")
HEURE = datetime.datetime.now().strftime("%H:%M")

for unArgv in sys.argv:
    if unArgv.split('=')[0] == 'TO':
        to = unArgv.split('=')[1]
    elif unArgv.split('=')[0] == 'CC':
        cc = unArgv.split('=')[1]
    elif unArgv.split('=')[0] == 'PASSWORD_DB':
        password_db = unArgv.split('=')[1]
    elif unArgv.split('=')[0] == 'PASSWORD_SMAILS':
        password_smails = unArgv.split('=')[1]
    elif unArgv.split('=')[0] == 'CONFIG':
        # Choose the config setup here (local-test; SRV-test; SRV-prod)
        config_name = unArgv.split('=')[1]

CONFIG = CONFIG[config_name]

# CONF MAIL #
PATH_EML = CONFIG["path"] + "/tmp/mail_to_BCI.eml"
PATH_TMP_HTML = CONFIG["path"] + "/tmp/mail_to_BCI.html"
USER = "bob"
SUBJECT = "BCI " + strftime("%Y%m%d") + \
    " Information retraits GAB"
FROM = "MNP@csb.nc"
TO = to.split(",")
CC = cc.split(",")

# Serveur sur python donc pas besoin de préciser le path
if CONFIG["on_what"] == "local":
    cx_Oracle.init_oracle_client(lib_dir=r"C:/oracle/instantclient_21_6")
else:
    os.environ['ORACLE_HOME'] = '/csb/app/oracle/product/12.1.0/db_1/'

connexion = None


#---------------------#
# DEFINITIONS DES FONCTIONS
#---------------------#

def request_to_bob(request):
    """
    Recupère les données à envoyer à la BCI
    les requetes se trouvent dans le fichier request_bci.py
    """

    try:
        with cx_Oracle.connect(USER, password_db, CONFIG["dsn"]) as connexion:
            with connexion.cursor() as curseur:
                # Recuperation des arretes comptables en attente de la validation par SG
                curseur.execute(request)
                results = curseur.fetchall()
                try:
                    if results[0][0] == None:
                        return 0
                except:
                    True
                if len(results) == 0:
                    return 0
                elif len(results) == 1:
                    return results[0][0]
                else:
                    print("Invalid request, return more than one output")
                    exit(1)

    except cx_Oracle.Error as error:
        print("Erreur Oracle : %s", error)
        print("Fin traitement.")
        sys.exit(1)


def get_html_message(params):
    """
    Creer un html à partir des modèles fournies dans les scripts (first_table.py, second_table.py et outro.py)
    """
    first_table_var = first_table.first_table(
        params["processus"], params["activite"], params["date"], params["heure"])
    second_table_var = second_table.second_table(
        str(params["code_banque"]), params["date_traitement"], str(params["bci"]), str(params["hors_bci"]), str(params["etranger"]))
    outro_var = outro.outro()

    html_msg = first_table_var + second_table_var + outro_var
    with open(PATH_TMP_HTML, "w") as file:
        file.write(html_msg)
    message = MIMEText(html_msg, 'html')
    return message


def send_mail(subject_mail, message_mail):
    """
    Envoie un mail en passant par le serveur Smails
    Commence par créer un fichier au format eml (mail)
    Puis envoie une requete CURL a smails
    """
    # MAIL CONFIGURATION
    mail = MIMEMultipart('alternative')
    mail['Subject'] = subject_mail
    mail['From'] = FROM
    mail['To'] = ", ".join(TO)
    mail['Cc'] = ", ".join(CC)
    mail['Date'] = formatdate(localtime=True)
    mail.attach(message_mail)

    # CREATE THE MAIL OBJECT
    fichierEML = PATH_EML
    with open(fichierEML, 'w') as outfile:
        gen = generator.Generator(outfile)
        gen.flatten(mail)

    # SEND THE MAIL
    cmd = "curl --request POST --data-binary \"@"+fichierEML+"\" -H \"Content-Type: application/json\"  http://" + \
        CONFIG["SMAILS_Serveur"]+":8080/v1/smails/mailMessage/" + \
        CONFIG["SMAILS_Client"]+"/" + \
        CONFIG["SMAILS_Service"]+"/" + password_smails

    retourCurl = subprocess.check_output(cmd, shell=True)

    # FORMATE LE RETOUR CURL POUR CHARGER EN JSON
    retourCurl = str(retourCurl)[2:]  # enlève les deux premiers char
    retourCurl = retourCurl[:(len(retourCurl)-1)]  # enlève le dernier char
    # enlève les backslash, pose pbs dans certaines erreurs, checker si marche ss linux
    retourCurl = retourCurl.replace("\\", "")

    # Le retour de la commande curl est au format JSON. Il convient d'en extraire le statut pour connaitre le code retour de la requete CURL.

    retourJson = json.loads(str(retourCurl))

    if "status" in retourJson:
        print(str(retourJson))
        sys.exit(1)


if __name__ == "__main__":
    print("\n - Debut du script - \n")

    # REQUESTS TO BOB12
    result_sql_request_bci = request_to_bob(
        requests_bci.sql_request_bci)

    result_sql_request_hors_bci = request_to_bob(
        requests_bci.sql_request_hors_bci)

    result_sql_request_etranger = request_to_bob(
        requests_bci.sql_request_etranger)

    print("Récupération des données sur BOB réussies \n\n")

    # FORMATING RESULTS
    results_requests = {"date": TODAY, "heure": HEURE, "date_traitement": TODAY, "processus": "Monétique", "activite": "Précompensation",
                        "bci": result_sql_request_bci, "hors_bci": result_sql_request_hors_bci, "etranger": result_sql_request_etranger, "code_banque": 17499}

    # SEND MAIL TO BCI
    if (results_requests["bci"] == 0
        and results_requests["hors_bci"] == 0
        and results_requests["etranger"] == 0
            and CONFIG["send_mail_anyway"] == "False"):
        print("Pas de rapport à envoyer")

    else:
        message = get_html_message(results_requests)
        send_mail(SUBJECT, message)

    if CONFIG["delete_tmp_files"] == "True":
        try:
            os.remove(PATH_EML)
            print("tmp mail deleted")
            os.remove(PATH_TMP_HTML)
            print("tmp html deleted")
        except:
            print("no mail to delete")
            print("no html to delete")

    print("\n - Fin du script - \n")
    exit(0)
