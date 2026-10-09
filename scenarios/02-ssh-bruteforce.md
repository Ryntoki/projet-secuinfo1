# Scénario 2 — Brute force SSH (hydra)

## Description
L'attaquant teste automatiquement une liste de mots de passe contre le compte
`vboxuser` sur le service SSH (port 22) de la cible, dans l'espoir de deviner le
bon mot de passe et d'obtenir un accès à distance.

## Pourquoi ce scénario
Attaque très répandue contre tout service exposé sur Internet. Montre la capacité
de l'IDS à détecter un grand nombre de tentatives de connexion rapprochées venant
de la même source.

## Commande lancée (depuis Kali)

<img width="654" height="40" alt="image" src="https://github.com/user-attachments/assets/3e46fa12-d8f9-40cc-ad6b-ffabe57c0085" />

Cependant, le brute force étant une méthode exaustive et longue, on utilise un .txt plus alléger histoire que l'attaque ne dure pas une éternité : 

<img width="648" height="118" alt="image" src="https://github.com/user-attachments/assets/a24a3090-f21b-425e-b9ee-47c8318f64d3" />

## Règle de détection (Snort)

alert tcp any any -> $HOME_NET 22 (msg:“SSH Brute Force attempt”;
flow:to_server,established; threshold: type threshold, track by_src,
count 5, seconds 10; sid:1000003; rev:1;)

Se déclenche dès que 5 connexions établies ou plus vers le port 22 arrivent de la
même source en 10 secondes.

## Logs collectés (/var/log/snort/alert)

<img width="1332" height="70" alt="image" src="https://github.com/user-attachments/assets/c2703c74-64c9-4adb-884f-730c94944eb5" />

Complété côté cible par le journal `auth.log` (connexions SSH échouées), géré par P2.

## Capture Kibana
(P1?)

## E-mail reçu
(P4?)
