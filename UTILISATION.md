# Utilisation

## Démarrer le système (routine complète)

### 1. Démarrer les deux VM
Dans VirtualBox : démarrer la VM **Ubuntu**, puis la VM **Kali**.

### 2. Vérifier les services (sur Ubuntu)
Elasticsearch, Kibana et syslog-ng démarrent automatiquement. Mais on vérifie au cas où :
```bash
sudo systemctl status elasticsearch kibana syslog-ng
```
Les trois doivent être `active (running)`. Sinon :
```bash
sudo systemctl start elasticsearch kibana syslog-ng
```
Kibana est accessible sur `http://localhost:5601` (patienter 1-2 minutes après le démarrage ça peut prendre plus ou moins de temps selon votre machine donc pas de panique).

### 3. Lancer Snort en mode console (sur Ubuntu)
C'est le mode qui alimente la collecte. Laisser ce terminal ouvert pendant toute la démonstration :
```bash
sudo systemctl stop snort
sudo snort -A fast -q -c /etc/snort/snort.conf -i enp0s8 -l /var/log/snort
```

### 4. Lancer les alertes e-mail (sur Ubuntu, 2e terminal)
```bash
cd ~/alertes && python3 alerte.py
```
Le message « Surveillance démarrée... » s'affiche.

### 5. Préparer DVWA (depuis Kali)
Pour les scénarios 3 et 4, ouvrir `http://192.168.56.10/login.php` (identifiants `admin` / `password`), puis menu **DVWA Security -> Low -> Submit** (à refaire à chaque session).

### Vérifier la connexion entre les VM (depuis Kali)
```bash
ping -c 3 192.168.56.10
```

---

## Rejouer les attaques (depuis Kali)

> Snort doit tourner en mode console (étape 3) pendant chaque attaque.
> Pour vérifier une détection, sur Ubuntu : `sudo tail -20 /var/log/snort/alert`

### Scénario 1 — Scan de ports (nmap)
```bash
nmap -sS 192.168.56.10
```

### Scénario 2 — Brute force SSH (hydra)
```bash
hydra -l vboxuser -P /home/kali/petite-liste.txt -t 4 ssh://192.168.56.10
```
*(`petite-liste.txt` : liste réduite de mots de passe. Voir `scenarios/02-ssh-bruteforce.md` pour la générer. Le mot de passe du compte `vboxuser` y est ajouté pour démontrer l'intrusion réussie.)*

### Scénario 3 — Injection SQL (DVWA)
Sur DVWA, page **SQL Injection**, dans le champ **User ID** :
```
1' UNION SELECT user, password FROM users-- -
```
DVWA affiche la liste des utilisateurs et leurs mots de passe hashés.

### Scénario 4a — XSS (DVWA)
Sur DVWA, page **XSS (Reflected)**, dans le champ :
```
<script>alert('XSS')</script>
```

### Scénario 4b — Directory traversal
Depuis le terminal Kali (le navigateur nettoie les `../`, il faut `curl`) :
```bash
curl -g --path-as-is "http://192.168.56.10/vulnerabilities/fi/?page=../../../../etc/passwd"
```

### Scénario 5 — SYN flood (hping3)
```bash
sudo hping3 -S --flood -p 80 192.168.56.10
```
Laisser tourner **5 secondes maximum**, puis **Ctrl+C**.
La raison est que cette attaque sature volontairement la VM Ubuntu et peut faire ralentir Kibana. Ne pas la laisser tourner trop longtemps. (Des tests ont même fait complètement stoppé Ubuntu au point où il fallait redémarrer la VM ainsi que Kibana)

---

## Voir les résultats dans Kibana

Ouvrir `http://localhost:5601` -> menu **Discover** -> Data View **Projet Secu** -> période **Last 15 minutes**.

Filtrer par attaque dans la barre de recherche :

| Scénario | Filtre |
|---|---|
| 1 — Scan | `snort.signature : "SCAN Possible nmap scan detecte"` |
| 2 — Brute force SSH | `snort.signature : "SSH Brute Force attempt"` |
| 3 — Injection SQL | `snort.signature : "SQL Injection attempt detecte"` |
| 4a — XSS | `snort.signature : "XSS attempt detecte"` |
| 4b — Directory traversal | `snort.signature : "Directory Traversal attempt detecte"` |
| 5 — SYN flood | `snort.signature : "DOS SYN Flood attempt detecte"` |

Pour voir toutes les attaques d'un coup (sans le bruit réseau) : `snort.sid >= 1000002`.
