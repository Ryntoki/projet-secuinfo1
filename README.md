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
| `config/` | Fichiers de configuration (Docker, Suricata, syslog-ng, script d'alerte) |
| `screenshots/` | Captures d'écran |

## Les 5 scénarios



## Équipe

 Membre : 
Landry Rayann
Calmels Nathan
Djokic Aleksandar
El Attari Kaouthar

## Analyse et conclusion

### Bilan


### Limites


### Améliorations possibles

### Veille technologique


