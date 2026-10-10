import smtplib
import time
import requests
import urllib3
from email.message import EmailMessage
from datetime import datetime, timedelta
from config import MAIL_FROM, MAIL_PASSWORD, MAIL_TO, ES_PASSWORD, ES_CA

urllib3.disable_warnings()

def conseil(attaque):
    if "SCAN" in attaque:
        return "Reconnaissance du serveur. Surveillez et bloquez l'IP si ça continue."
    if "SSH" in attaque:
        return "Attaque sur le mot de passe SSH. Bloquez l'IP est recommandé, changez également votre message dès que possible."
    if "SQL" in attaque:
        return "Injection SQL : risque de vol de la base. Corriger le code et bloquer l'IP, vérifiez si des données ont fuités."
    if "XSS" in attaque:
        return "Injection de script danger pour les visiteurs. Filtrez les entrees."
    if "Directory" in attaque:
        return "Tentative de lecture de fichiers du serveur. Verifiez les acces, vérifiez les permissions des fichiers."
    if "DOS" in attaque:
        return "Deni de service : le serveur est sature. Limitez l'IP qui attaque et surveillez la charge du serveur."
    return "Intrusion detectee. Bloquer l'IP source."

def envoyer_mail(attaque, src, dst, prio, date):
    message = EmailMessage()
    message["Subject"] = "[ALERTE IDS] " + attaque
    message["From"] = MAIL_FROM
    message["To"] = MAIL_TO
    message.set_content(
        "Une intrusion a ete detectee.\n\n"
        "Type d'attaque : " + attaque + "\n"
        "Priorite       : " + str(prio) + "\n"
        "Attaquant      : " + src + "\n"
        "Cible          : " + dst + "\n"
        "Date           : " + date + "\n\n"
        "Conseil : " + conseil(attaque)
    )
    serveur = smtplib.SMTP("smtp.gmail.com", 587)
    serveur.starttls()
    serveur.login(MAIL_FROM, MAIL_PASSWORD)
    serveur.send_message(message)
    serveur.quit()
    print("Mail envoye pour l'attaque " + attaque)

print("Surveillance demarree (Ctrl+C pour arreter)...")

derniers_mails = {}

while True:
    depuis = (datetime.utcnow() - timedelta(seconds=35)).strftime("%Y-%m-%dT%H:%M:%S")
    requete = {
        "query": {"bool": {"must": [
            {"range": {"snort.sid": {"gte": 1000002}}},
            {"range": {"@timestamp": {"gte": depuis}}}
        ]}},
        "size": 50
    }

    reponse = requests.get(
        "https://localhost:9200/projet-secu-*/_search",
        json=requete,
        auth=("elastic", ES_PASSWORD),
        verify=ES_CA,
        timeout=10
    )

    alertes = reponse.json()["hits"]["hits"]
    for alerte in alertes:
        donnees = alerte["_source"]
        snort = donnees.get("snort", {})
        attaque = snort.get("signature", "Attaque")
        src = snort.get("src_ip", "?")
        dst = snort.get("dest_ip", "?")
        prio = snort.get("priority", "?")
        date = donnees.get("@timestamp", "")

        if time.time() - derniers_mails.get(attaque, 0) > 120:
            envoyer_mail(attaque, src, dst, prio, date)
            derniers_mails[attaque] = time.time()

    time.sleep(30)
