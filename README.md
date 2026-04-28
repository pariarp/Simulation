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