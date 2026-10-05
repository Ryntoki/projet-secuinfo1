# Installation

Suivre les étapes dans l'ordre.

## 1. Machines virtuelles

Le projet utilise deux machines virtuelles dans VirtualBox :
- **une VM Ubuntu** : le serveur surveillé, avec ses cibles (site web Apache et accès SSH) et tous les outils de détection, de collecte et de visualisation ;
- **une VM Kali** : l'attaquant, utilisée pour lancer les 5 scénarios.

Les deux VM communiquent sur un réseau privé isolé. Les attaques ne sortiront jamais de ce réseau.

### Prérequis
- **VirtualBox 7.2 ou plus récent.** (La version 7.1 ne permet pas d'installer les Additions invité sur le noyau 7.0 d'Ubuntu 24.04.5 (voir « problèmes rencontrés »)).
- L'image **Ubuntu 24.04 LTS Desktop** : "ubuntu-24.04.5-desktop-amd64.iso" (ubuntu.com, rubrique "past releases"). On n'utilise pas Ubuntu 26.04 : trop récente, certains outils risquent de ne pas encore être compatibles donc on ne prend pas de risques.
- L'image **Kali pour VirtualBox** (kali.org, rubrique "Get Kali -> Virtual Machines").
- Un PC avec **16 Go de RAM** recommandés pour faire tourner les deux VM en même temps (moins c'est possible mais cela risque d'être plus long pour certains éléménts).

### Création de la VM Ubuntu
Dans VirtualBox : **Machine -> Nouvelle**, choisir l'ISO Ubuntu, puis les réglages suivants :

| Paramètre | Valeur | Pourquoi |
|---|---|---|
| Skip Unattended Installation | Coché | Garder la main sur l'installation et les droits administrateur |
| Mémoire vive | 8192 Mo | Elasticsearch et Kibana demandent beaucoup de mémoire |
| Processeurs | 4 | Suffisant pour faire tourner tous les outils |
| Disque | 50 Go, non pré-alloué | Le fichier n'occupe que l'espace réellement utilisé |
| Carte réseau 1 | NAT | Accès à Internet pour les téléchargements |
| Carte réseau 2 | Réseau privé hôte | Réseau isolé entre Ubuntu et Kali qui utilisé pour les attaques |

![Réglages de la VM Ubuntu](screenshots/reglagesubuntu.png)

Installation d'Ubuntu : "installer Ubuntu" -> installation interactive -> sélection par défaut -> "effacer le disque et installer Ubuntu" (cela n'efface que le disque virtuel de la VM).

### Mise à jour du système
```bash
sudo apt update && sudo apt upgrade -y
```
Si Ubuntu propose ensuite de passer à la version 26.04, il faut refuser
### Additions invité (copier-coller entre Windows et la VM ce qui facilitera la suite pour votre installation)
Menu VirtualBox : **périphériques -> insérer l'image CD des additions invité**, puis dans le terminal :
```bash
sudo apt install -y bzip2 gcc make perl linux-headers-$(uname -r) build-essential dkms
sudo sh /media/$USER/VBox_GAs_*/VBoxLinuxAdditions.run
sudo reboot
```
Enfin : **périphériques -> presse-papier partagé -> bidirectionnel**. Dans le Terminal on peut maintenant coller avec “Ctrl+Maj+V”.

### Import de la VM Kali
1. Extraire l'archive (en ".7z") (clic droit -> extraire tout) dans le dossier où sont rangées les VM.
2. Dans VirtualBox : **machine -> open…**, puis sélectionner le fichier ".vbox" de Kali.
3. Configuration : mémoire vive 2048 Mo, carte réseau 1 en NAT, carte réseau 2 en réseau privé hôte.
4. Démarrer Kali et utiliser les identifiants par défaut : “kali” / “kali”.

![Les deux VM dans VirtualBox](screenshots/vm-liste.png)

### Adresses IP fixes
Par défaut, la carte « Réseau privé hôte » reçoit une adresse automatique qui peut changer. On fixe l'adresse de chaque VM pour que Kali sache toujours où se trouve sa cible. On repère d'abord la carte et le nom de sa connexion :
```bash
ip -br a
nmcli con show
```
Sur **Ubuntu** (carte "enp0s8", connexion "netplan-enp0s8") :
```bash
sudo nmcli con mod "netplan-enp0s8" ipv4.addresses 192.168.56.10/24 ipv4.method manual
sudo nmcli con up "netplan-enp0s8"
```
Sur **Kali** (carte "eth1", connexion "Wired connection 2") :
```bash
sudo nmcli con mod "Wired connection 2" ipv4.addresses 192.168.56.20/24 ipv4.method manual
sudo nmcli con up "Wired connection 2"
```
La carte NAT ("enp0s3" / "eth0") n'est pas modifiée : elle sert à l'accès Internet.

### Test de communication
Depuis Kali :
```bash
ping -c 4 192.168.56.10
```
Résultat obtenu : 4 paquets envoyés, 4 reçus, 0 % de perte. Les deux VM communiquent.




## 2. Elasticsearch et Kibana 

**1 : Mise à jour de la machine**
```bash
sudo apt update && sudo apt upgrade -y
```

**2 : Autoriser l'installation**
```bash
sudo apt install curl apt-transport-https -y
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elastic.gpg
```

**3 : Ajout du dépôt Elastic**
```bash
echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
```

**4 : Installation de Kibana et Elasticsearch**
```bash
sudo apt update
sudo apt install elasticsearch kibana -y
```

**5 : Démarrer les services**
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now elasticsearch
sudo systemctl enable --now kibana
```

**6 : Vérification si Elastic est actif**
```bash
sudo systemctl status elasticsearch.service
```

Si Elastic ne se lance pas, possible erreur avec la RAM (status = 137).

<img width="705" height="234" alt="Erreur RAM" src="https://github.com/user-attachments/assets/6cda4043-90f2-4d80-ae4c-139feb3bbd5c" />

Alors copier ces commandes (on limite l'utilisation de la RAM à 512 Mo car il consomme beaucoup sinon) :
```bash
echo "-Xms512m" | sudo tee /etc/elasticsearch/jvm.options.d/heap.options
echo "-Xmx512m" | sudo tee -a /etc/elasticsearch/jvm.options.d/heap.options
```

Il faut alors relancer Elastic avec la commande :
```bash
sudo systemctl restart elasticsearch
```

**7 : Configurer la connexion à Elastic**
Lien web vers Elastic : `http://localhost:5601`

Vous arrivez ici : 

<img width="385" height="307" alt="token_elastic" src="https://github.com/user-attachments/assets/fae3d6ea-3a5a-42bb-91e2-65ccf277bc59" />

Commande pour générer le token d'enrôlement (expire en 30 minutes, à refaire en utilisant la même commande) :
```bash
sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```

Pour avoir le code de vérification, utiliser cette commande :
```bash
sudo /usr/share/kibana/bin/kibana-verification-code
```

Commande pour générer le mot de passe du compte admin elastic (à garder précieusement) :
```bash
sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
```

Les identifiants du compte sont donc :
* **Username** : `elastic`
* **Password** : *(mdp généré par la commande)*





## 3. Snort



## 4. syslog-ng



## 5. Alertes par e-mail



## Problèmes rencontrés et solutions

| Problème | Solution |
|---|---|
| | |
