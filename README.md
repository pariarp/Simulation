# Simulation MAC — Exponential Backoff

## Phase 1 : Squelette et Moteur de Base (Terminée)

### Étape 1 : Modélisation et définition de l'architecture du simulateur

##### 1. Les Entités (Les Stations)
Nous avons N stations qui veulent émettre des paquets. Chaque station doit avoir :
- **Un état actuel (i)** : Initialement à 1. Cet état représente le nombre de collisions subies et va définir le temps d'attente.
- **Une file d'attente** : Pour stocker les paquets, avec une capacité maximale de K.
- **Un statut** : Est-ce qu'elle est en train d'émettre ? Est-elle en attente (backoff) ?

##### 2. Les Variables Globales (L'état du système)
Pour pouvoir tracer les courbes, le simulateur doit suivre certaines métriques :
- `horloge` : Le temps global t de la simulation.
- `canal_occupe_par` : Liste des stations en train d'émettre (pour détecter les collisions).
- `n_succes` : Le nombre de paquets transmis avec succès n(t).
- `n_perdus` : Le nombre de paquets rejetés car la file d'une station était pleine.
- `somme_clients` : Pour calculer le nombre moyen de clients au cours du temps.

##### 3. L'Échéancier (La file d'événements)
C'est le moteur du simulateur. Il contient les événements futurs, triés par ordre chronologique. Les événements possibles dans notre système :
- **Arrivée d'un paquet** : Un nouveau paquet arrive à une station. (La durée entre deux arrivées suit une loi exponentielle de paramètre λ).
- **Début de transmission** : Une station tente d'envoyer un paquet sur le canal.
- **Fin de transmission** : Se produit 1 unité de temps après le début. C'est à ce moment qu'on vérifie si le paquet est passé (succès) ou s'il y a eu un chevauchement (collision).

---

### Étape 2 : Moteur à événements discrets
- Initialisation du simulateur via `initialisation()` : on programme la première arrivée de paquet pour chaque station via `random.expovariate(λ)`.
- Boucle principale dans `executer()` : on extrait toujours l'événement le plus proche dans le temps, on met à jour l'horloge, et on met à jour `somme_clients` (aire sous la courbe).
- Un dispatcher redirige chaque événement vers la bonne fonction de traitement.

### Étape 3 : Arrivée des paquets (`_traiter_arrivee`)
- On génère le prochain délai d'arrivée via `random.expovariate(λ)` et on le planifie dans l'échéancier.
- Si la file est pleine (capacité K atteinte) → le paquet est marqué comme perdu (`n_perdus += 1`).
- Sinon, il entre dans la file (`nb_paquets += 1`). Si la station était inactive (pas en transmission, pas en backoff) → elle tente de transmettre immédiatement.

---

## Phase 2 : Cœur du Protocole MAC (Terminée)

### Étape 4 : Début de Transmission (`_traiter_debut_emission`)
- La station est marquée comme en transmission (`en_transmission = True`).
- Son ID est ajouté dans `canal_occupe_par`.
- La fin de l'émission est planifiée dans **1 unité de temps** exactement.

### Étape 5 : Fin de Transmission — Succès ou Collision (`_traiter_fin_emission`)
- La station est retirée de `canal_occupe_par` et `en_transmission` repasse à False.
- **SUCCÈS** si aucune autre station n'émettait en même temps :
  - `n_succes += 1`, `nb_paquets -= 1`, `etat_i` remis à 1.
  - Si des paquets restent en file → on planifie un nouveau `debut_emission`.
- **COLLISION** sinon :
  - `etat_i += 1`.
  - Temps de backoff calculé : `Exp(1 / (2^i × τ))`.
  - `en_backoff = True`, on planifie `fin_backoff`.

### Étape 6 : Fin du Backoff (`_traiter_fin_backoff`)
- `en_backoff` repasse à False.
- Si des paquets sont en attente → on planifie un nouveau `debut_emission`.

---

## Phase 3 : Mesures et Statistiques (À venir)

### Étape 7 : Collecte des métriques
### Étape 8 : Génération des courbes et Analyse