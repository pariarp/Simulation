# Simulation

### Étape 1 : Modélisation et définition de l'architecture du simulateur
##### 1. Les Entités (Les Stations)
Nous avons N stations qui veulent émettre des paquets. Chaque station doit avoir :
- **Un état actuel (i)**: Initialement à 1. Cet état représente le nombre de collisions subies et va définir le temps d'attente.
- **Une file d'attente** : Pour stocker les paquets, avec une capacité maximale de K.
- **Un statut** : Est-ce qu'elle est en train d'émettre ? Est-elle en attente (backoff) ?

##### 2. Les Variables Globales (L'état du système)
Pour pouvoir tracer tes courbes plus tard, ton simulateur doit suivre certaines métriques :
- `horloge` : Le temps global t de la simulation.
- `canal_occupe` : Savoir si une transmission est en cours (et par combien de stations, pour détecter les collisions).
- `n_succes` : Le nombre de paquets transmis avec succès n(t).
- `n_perdus` : Le nombre de paquets rejetés car la file d'une station était pleine.
- `somme_clients` : Pour calculer le nombre moyen de clients au cours du temps.

##### 3. L'Échéancier (La file d'événements)
C'est le moteur de ton simulateur. Il doit contenir les événements futurs, triés par ordre chronologique. Quels sont les événements possibles dans notre système ?
- **Arrivée d'un paquet** : Un nouveau paquet arrive à une station. (La durée entre deux arrivées suit une loi exponentielle de paramètre λ ).
- **Début de transmission** : Une station tente d'envoyer un paquet sur le canal.
- **Fin de transmission** : Se produit 1 unité de temps après le début. C'est à ce moment qu'on vérifie si le paquet est passé (succès) ou s'il y a eu un chevauchement (collision).

# Simulation MAC — Exponential Backoff

### Étape 1 : Modélisation et définition de l'architecture du simulateur
##### 1. Les Entités (Les Stations)
Nous avons N stations qui veulent émettre des paquets. Chaque station doit avoir :
- **Un état actuel (i)**: Initialement à 1. Cet état représente le nombre de collisions subies et va définir le temps d'attente.
- **Une file d'attente** : Pour stocker les paquets, avec une capacité maximale de K.
- **Un statut** : Est-ce qu'elle est en train d'émettre ? Est-elle en attente (backoff) ?

##### 2. Les Variables Globales (L'état du système)
Pour pouvoir tracer les courbes, le simulateur doit suivre certaines métriques :
- `horloge` : Le temps global t de la simulation.
- `canal_occupe` : Savoir si une transmission est en cours (et par combien de stations, pour détecter les collisions).
- `n_succes` : Le nombre de paquets transmis avec succès n(t).
- `n_perdus` : Le nombre de paquets rejetés car la file d'une station était pleine.
- `somme_clients` : Pour calculer le nombre moyen de clients au cours du temps.

##### 3. L'Échéancier (La file d'événements)
C'est le moteur du simulateur. Il contient les événements futurs, triés par ordre chronologique. Les événements possibles dans notre système :
- **Arrivée d'un paquet** : Un nouveau paquet arrive à une station. (La durée entre deux arrivées suit une loi exponentielle de paramètre λ).
- **Début de transmission** : Une station tente d'envoyer un paquet sur le canal.
- **Fin de transmission** : Se produit 1 unité de temps après le début. C'est à ce moment qu'on vérifie si le paquet est passé (succès) ou s'il y a eu un chevauchement (collision).

---

### Étape 2 : Implémentation du simulateur

##### 1. Les 4 types d'événements
Chaque événement est un tuple `(date, type, id_station)` stocké dans l'échéancier :

| Événement | Déclencheur | Action principale |
|---|---|---|
| `arrivee` | Toutes les Exp(λ) secondes | Ajoute un paquet en file, planifie la prochaine arrivée |
| `debut_emission` | Station libre avec un paquet | Marque la station comme émettrice, planifie `fin_emission` dans 1 unité |
| `fin_emission` | 1 unité après `debut_emission` | Vérifie succès ou collision |
| `fin_backoff` | Après le délai de backoff | Relance une tentative d'émission |

##### 2. La boucle principale
La simulation démarre en planifiant une première arrivée pour chaque station. Ensuite, elle tourne en boucle : elle extrait toujours l'événement le plus proche dans le temps, met à jour l'horloge, et appelle la fonction de traitement correspondante.

##### 3. Traitement des événements

**`_traiter_arrivee(station)`**
- Planifie la prochaine arrivée sur cette station (Exp(λ))
- Si la file est pleine → paquet perdu (`n_perdus += 1`)
- Sinon → `nb_paquets += 1`
- Si la station est libre (pas en transmission, pas en backoff) → planifie `debut_emission` immédiatement

**`_traiter_debut_emission(station)`**
- Marque la station comme en transmission (`en_transmission = True`)
- Ajoute son ID dans `canal_occupe_par`
- Planifie `fin_emission` dans **1 unité de temps**

**`_traiter_fin_emission(station)`**
- Retire la station de `canal_occupe_par`
- Remet `en_transmission = False`
- **Si aucune autre station n'émettait en même temps → SUCCÈS** :
  - `n_succes += 1`
  - `nb_paquets -= 1`
  - `etat_i` remis à 1
  - Si des paquets restent en file → planifie `debut_emission`
- **Sinon → COLLISION** :
  - `etat_i += 1`
  - Calcul du backoff : Exp(1 / (2^i × τ))
  - `en_backoff = True`
  - Planifie `fin_backoff`

**`_traiter_fin_backoff(station)`**
- Remet `en_backoff = False`
- Si des paquets sont en attente → planifie `debut_emission`

##### 4. Hypothèses du modèle
- Le temps d'émission est fixe et vaut **1 unité de temps**
- Deux émissions qui se chevauchent même partiellement → **collision**
- Les paquets perdus par collision sont **définitivement perdus**
- L'état de backoff `i` n'a **pas de borne supérieure**
- Au démarrage, toutes les stations ont leur file **vide**

---
