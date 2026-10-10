# Scénario 4 : XSS (reflected) et parcours de répertoires

## Description
Deux failles testées sur le même site DVWA :
- **XSS réfléchi** : l'attaquant injecte un script `<script>alert('XSS')</script>`
  dans un paramètre d'URL, exécuté par le navigateur de la victime qui clique dessus.
- **Directory traversal** : l'attaquant manipule un paramètre de fichier
  (`../../../../etc/passwd`) pour lire des fichiers du serveur en dehors du
  répertoire web normal.

## Pourquoi ce scénario
Deux failles web très courantes, complémentaires à l'injection SQL : l'une cible
les utilisateurs du site (XSS), l'autre le système de fichiers du serveur
(traversal). Montre la diversité des attaques applicatives détectables par l'IDS.

## Commandes lancées (depuis le navigateur, sur Kali)

XSS :
http://192.168.56.10/vulnerabilities/xss_r/?name=<script>alert(‘XSS’)</script>

Directory traversal :
http://192.168.56.10/vulnerabilities/fi/?page=../../../../etc/passwd

## Règles de détection (Snort)

alert tcp any any -> $HOME_NET 80 (msg:“XSS attempt detecte”; content:”<script”;
nocase; http_uri; sid:1000005; rev:1;)

alert tcp any any -> $HOME_NET 80 (msg:“Directory Traversal attempt detecte”;
content:”../”; http_uri; sid:1000006; rev:1;)

## Logs collectés (/var/log/snort/alert)

XSS :

<img width="1695" height="57" alt="image" src="https://github.com/user-attachments/assets/15bc9e48-4aa6-4310-bf3f-22817629dae5" />

Directory transversal :

<img width="1844" height="52" alt="image" src="https://github.com/user-attachments/assets/7144a8e8-3d76-49f5-9a30-fa32785639ed" />


## Capture Kibana
(P1?)

## E-mail reçu
(P4?)
