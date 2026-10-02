# Installation

Suivre les étapes dans l'ordre.

## 1. Machines virtuelles



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
