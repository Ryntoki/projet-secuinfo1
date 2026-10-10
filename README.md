# Détection d'intrusions et gestion de logs

Mise en place d'un système qui **détecte des attaques réseau**, **collecte les logs**, les **affiche dans Kibana** et **prévient l'administrateur par e-mail**. Le système est testé sur **5 scénarios d'attaque**.

## Architecture

Le système repose sur deux machines virtuelles (VirtualBox) isolées communiquant via un réseau privé hôte (Host-Only) :
*   **VM Ubuntu 24.04 (Cible et Défense - 192.168.56.10)** : Héberge les services cibles (Serveur Web Apache avec DVWA, Serveur SSH) ainsi que toute la pile de sécurité :
    *   **Snort** (NIDS) configuré avec des règles personnalisées pour détecter les attaques.
    *   **syslog-ng** pour centraliser, filtrer et formater les journaux (logs web, SSH et alertes Snort).
    *   **Elasticsearch & Kibana** (Suite Elastic) pour l'indexation des logs en temps réel et la création de tableaux de bord visuels.
*   **VM Kali Linux (Attaquant - 192.168.56.20)** : Utilisée pour rejouer les scénarios d'attaque de manière contrôlée vers la VM Ubuntu.

## Contenu du dépôt

| Élément | Contenu |
|---|---|
| [INSTALLATION.md](INSTALLATION.md) | Installation pas à pas de tout le système |
| [UTILISATION.md](UTILISATION.md) | Comment lancer le système et rejouer les attaques |
| [scenarios/](scenarios/) | Une fiche par attaque |
| `config/` | Fichiers de configuration (syslog-ng, script d'alerte) |
| `screenshots/` | Captures d'écran |

## Les 5 scénarios

Le système est testé et validé face aux 5 vecteurs d'attaque suivants :
1.  **Scan de ports** : Reconnaissance réseau effectuée avec `nmap` pour identifier les services ouverts.
2.  **Brute force SSH** : Tentatives de connexion répétées sur le port réalisées avec `hydra` via une liste de mots de passe.
3.  **Injection SQL** : Exploitation d'une faille de base de données (extraction de tables/utilisateurs) via l'application web DVWA.
4.  **XSS et Directory Traversal ** : Injection de code JavaScript et tentative d'accès aux fichiers sensibles du système (`/etc/passwd`) via DVWA.
5.  **Déni de service (SYN Flood)** : Saturation de la cible par une inondation de requêtes incomplètes générées avec `hping3` sur le port 80.

## Équipe

 Membre : 
Landry Rayann
Calmels Nathan
Djokic Aleksandar
El Attari Kaouthar

## Analyse et conclusion

### Bilan

Ce projet a permis de mettre en œuvre un SIEM (Security Information and Event Management) fonctionnel et complet. La chaîne de traitement a été validée de bout en bout donc de la génération du trafic malveillant jusqu'à sa visualisation en temps réel. La configuration de règles Snort spécifiques (SID > 1000000) couplée au formatage JSON dans syslog-ng a permis de filtrer efficacement le bruit réseau pour ne faire ressortir que les véritables alertes que l'on a ciblé.

### Limites

*   **Consommation de ressources :** faire tourner Elasticsearch, Kibana, Snort, Apache et MariaDB sur une seule machine virtuelle est extrêmement gourmand et entraîne des instabilités au niveau de la RAM (comme l'erreur 137 traitée lors de l'installation).
*   **Détection passive (NIDS) :** Snort est ici configuré en mode détection uniquement (règles `alert`). Il génère des logs et prévient l'administrateur, mais ne bloque pas le trafic malveillant de l'attaquant.
*   **Absence de corrélation avancée :** le système centralise très bien les alertes individuelles, mais ne croise pas encore automatiquement les logs web d'Apache avec les alertes Snort pour reconstruire le parcours d'un attaquant.

### Améliorations possibles

*   **Passage en mode IPS (Intrusion Prevention System) :** Implémenter Fail2Ban ou configurer Snort en mode actif pour bloquer automatiquement au niveau du pare-feu les adresses IP (comme le 192.168.56.20 de Kali) identifiées comme malveillantes.
*   **Séparation des rôles (Architecture distribuée) :** Déporter la pile Elastic (Elasticsearch et Kibana) sur un serveur dédié pour alléger le serveur web cible. Cela éviterait aussi qu'une attaque par déni de service (comme le hping3) ne fasse tomber en même temps le système de supervision (ce qui est réellement arrivé lors des tests).
*   **Centralisation des alertes e-mail :** Remplacer le script d'alerte indépendant par les fonctionnalités natives de *Watcher/ElastAlert* directement intégrées à Kibana, afin de déclencher les e-mails uniquement lors de corrélations complexes.

### Veille technologique

L'architecture mise en place correspond à une approche SIEM traditionnelle (Collecte, indexation et détection par signature). Aujourd'hui, l'industrie de la cybersécurité s'oriente vers des solutions **XDR** qui assemblent de multiples sources de sécurité. Par ailleurs, la détection basée sur des règles écrites manuellement (comme nos fichiers Snort) montre ses limites face aux attaques inédites qu'on aurait pas prévu. Les solutions modernes intègrent désormais des algorithmes d'analyse comportementale et de **machine learning** capables de détecter des anomalies réseau de manière proactive sans nécessiter de base de signatures déjà faite.


