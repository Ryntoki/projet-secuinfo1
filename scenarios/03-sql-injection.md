# Scénario 3 — Injection SQL

## Description
L'attaquant exploite un formulaire vulnérable du site web (DVWA) pour injecter du
code SQL dans le champ « User ID ». Avec une requête UNION, il récupère la liste
des utilisateurs et leurs mots de passe hashés directement depuis la base de données.

## Pourquoi ce scénario
C'est l'exemple donné dans l'énoncé du projet. Montre une attaque applicative visant
le vol de données, bien plus dangereuse qu'un scan ou un brute force puisqu'elle
touche directement le contenu de la base.

## Commande lancée (depuis le navigateur, sur Kali)

http://192.168.56.102/vulnerabilities/sqli/ dans "SQL Injection"
Champ User ID : 1' UNION SELECT user, password FROM users-- -

## Règle de détection (Snort)

alert tcp any any -> $HOME_NET 80 (msg:“SQL Injection attempt detecte”;
content:“UNION”; nocase; http_uri; sid:1000004; rev:1;)

Se déclenche quand le mot-clé `UNION` apparaît dans l'URL d'une requête HTTP vers
le port 80 — signature classique d'une injection SQL par UNION.

## Logs collectés (/var/log/snort/alert)

<img width="1399" height="36" alt="image" src="https://github.com/user-attachments/assets/e2d5d724-6854-4996-a8b6-4460bea4ea24" />

## Capture Kibana
(P1?)

## E-mail reçu
(P4?)
