# -*- coding: UTF-8 -*-

"""
- Ticket 79638
Script faisant suite a la demande de la societe generale pour avoir un envoi automatique de mail
quotidien precisant si il y a des arretes comptables en attente de validation
Commande pour lancer le script (pas de configuration supplémentaire)
python "C:/Users/guetec/OneDrive - CSB/Documents/projets/BCI_ON_US/bci_on_us/bin/mail.py" TO=colin.guetemme@live.fr CC=guetec@csb.nc,colin.guetemme@live.fr CODEBANQUE=18319 USER_DB=bob PASSWORD_DB=**** PASSWORD_SMAILS=****
python /csb/bin/envoi_mail_arretes_comptables.py TO=pole-monetique@sgcb.nc CC=mnpexploitation@csb.nc CODEBANQUE=18319 USER_DB=bob PASSWORD_DB=**** PASSWORD_SMAILS=****


Prérequis:
- le chemin "/csb/tmp/" doit exister
"""

import datetime
from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import json

from time import strftime

import cx_Oracle
import sys
import subprocess
import logging
import os

import requests
import yaml
import first_table
import second_table
import outro

#---------------------#
# CONFIGURATION #
#---------------------#

dirname = os.path.dirname(__file__)
config_file = os.path.join(dirname, '../cfg/config.yml')

with open(config_file, 'r', encoding='utf-8') as file:
    config = json.load(file)


# Serveur sur python donc pas besoin de préciser le path
cx_Oracle.init_oracle_client(lib_dir=r"C:/oracle/instantclient_21_6")

repScript = os.path.abspath(os.path.split(__file__)[0])
nomScript = os.path.splitext(os.path.split(__file__)[1])[0]

## CONFIG LOG ##
logging.basicConfig(filename=repScript+'/../log/envoi_mail_arretes_comptables.log',
                    format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)
# never worked on the dev server so replace it by print

## SQL REQUESTS ##

today = datetime.datetime.now().strftime("%d/%m/%y")
heure = datetime.datetime.now().strftime("%H:%M")


# CONF MAIL #

for unArgv in sys.argv:
    if unArgv.split('=')[0] == 'TO':
        receiver = unArgv.split('=')[1]
    if unArgv.split('=')[0] == 'CC':
        cc = unArgv.split('=')[1]
    elif unArgv.split('=')[0] == 'CODEBANQUE':
        code_banque = unArgv.split('=')[1]
    elif unArgv.split('=')[0] == 'USER_DB':
        user = unArgv.split('=')[1]
    elif unArgv.split('=')[0] == 'PASSWORD_DB':
        password = unArgv.split('=')[1]
    elif unArgv.split('=')[0] == 'PASSWORD_SMAILS':
        password_smails = unArgv.split('=')[1]

path_eml = config["path"] + "/tmp/mail_to_BCI.eml"
path_tmp_html = config["path"] + "/tmp/mail_to_BCI.html"


config = {

    "sender": "MNP@csb.nc",
    "receiver": receiver.split(","),  # pole-monetique@sgcb.nc
    "cc": cc.split(","),  # mnpexploitation@csb.nc
    "code_banque": code_banque,  # 18319 correspond au code banque de la SG en NC


    # TODO passer sur l'env de prod
    "path_eml": "C:/Users/guetec/OneDrive - CSB/Documents/projets/BCI_ON_US/bci_on_us/tmp/last_mail_AC_SG.eml",
    # "path_eml": "/csb/tmp/last_mail_AC_SG.eml",

    # "dsn": "192.168.141.112:2328/BOB",
    "dsn": "192.168.202.17:1521/BOB",  # env de dev
    "user": user,
    "password": password,
    "port": 25,

    # "SMAILS_Serveur": "172.19.45.42",
    "SMAILS_Serveur": "192.168.201.242",  # env de dev
    "SMAILS_Client": "CSB",
    "SMAILS_Service": "MAIL_TECHNIQUE",
    "SMAILS_mdp": password_smails,
}


connexion = None

os.environ['ORACLE_HOME'] = '/csb/app/oracle/product/12.1.0/db_1/'


#---------------------#
# DEFINITIONS DES FONCTIONS
#---------------------#

def request_to_bob(request, config):
    """
    Recupère les données à envoyer à la BCI
    """

    try:
        with cx_Oracle.connect(config["user"], config["password"], config["dsn"]) as connexion:
            print("Connexion a la base de donnee BOB reussi")
            with connexion.cursor() as curseur:
                # Recuperation des arretes comptables en attente de la validation par SG
                curseur.execute(request)
                print("executed")
                return curseur.fetchall()

    except cx_Oracle.Error as error:
        print("Erreur Oracle : %s", error)
        print("Fin traitement.")
        sys.exit(1)


def get_html_message(params):
    """
    Formate les resultats de la recuperation des AC en attente

    Parameters
    -------

    """

    first_table_var = first_table.first_table(
        params["processus"], params["activite"], params["date"], params["heure"])
    second_table_var = second_table.second_table(
        str(params["code_banque"]), params["date_traitement"], str(params["bci"]), str(params["hors_bci"]), str(params["etranger"]))
    outro_var = outro.outro()

    html_msg = first_table_var + second_table_var + outro_var
    with open("C:/Users/guetec/OneDrive - CSB/Documents/projets/BCI_ON_US/bci_on_us/bin/my_data.html", "w") as file:
        file.write(html_msg)
    message = MIMEText(html_msg, 'html')
    return message


def send_mail(subject_mail, message_mail, config):
    """
    Envoie un mail en passant par le serveur Smails
    Commence par créer un fichier au format eml (mail)
    Puis envoie une requete CURL a smails
    """
    mail = MIMEMultipart('alternative')
    mail['Subject'] = subject_mail
    mail['From'] = config["sender"]
    mail['To'] = ", ".join(config["receiver"])
    mail['Cc'] = ", ".join(config["cc"])
    mail['Date'] = formatdate(localtime=True)
    mail.attach(message_mail)

    fichierEML = config["path_eml"]
    with open(fichierEML, 'w') as outfile:
        gen = generator.Generator(outfile)
        gen.flatten(mail)

    cmd = "curl --request POST --data-binary \"@"+fichierEML+"\" -H \"Content-Type: application/json\"  http://" + \
        config["SMAILS_Serveur"]+":8080/v1/smails/mailMessage/" + \
        config["SMAILS_Client"]+"/" + \
        config["SMAILS_Service"]+"/" + config["SMAILS_mdp"]

    retourCurl = subprocess.check_output(cmd, shell=True)
    retourCurl


if __name__ == "__main__":
    print("\n - Debut du script - \n")
    results = "test"

    result_sql_request_bci = request_to_bob(
        requests.sql_request_bci, config)[0][0]
    # request_to_bob(requests.sql_request_hors_bci, config)[0][0]
    result_sql_request_hors_bci = 2
    # request_to_bob(requests.sql_request_etranger, config)[0][0]
    result_sql_request_etranger = 3

    results_requests = {"date": today, "heure": heure, "date_traitement": today, "processus": "Monétique", "activite": "Précompensation",
                        "bci": result_sql_request_bci, "hors_bci": result_sql_request_hors_bci, "etranger": result_sql_request_etranger, "code_banque": 17499}

    if results_requests["bci"] == 0 and results_requests["hors_bci"] == 0 and results_requests["etranger"] == 0:
        print("Pas de rapport à envoyer")
        exit(0)

    else:
        message = get_html_message(results_requests)
        # send_mail('Rapport', message, config) #TODO uncomment
        print(" - Fin du script - \n ----- \n ")
        exit(0)
