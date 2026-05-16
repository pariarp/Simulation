# Projet de Simulation - Medium Access Control (MAC)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?logo=plotly)

**Master 1 Informatique - DataScale | Université Paris-Saclay (2025-2026)**

**Auteurs :** Paria RAHMATPANAH [22503767] & Emmy MARIE-JOSEPH [22102295]

---

Ce projet implémente un simulateur à événements discrets d’un protocole MAC utilisant un mécanisme d’Exponential Backoff.

Le simulateur permet :
- de gérer plusieurs stations partageant un même canal,
- de simuler les collisions,
- d’implémenter le backoff exponentiel,
- de mesurer les performances du système :
  - débit,
  - nombre moyen de clients,
  - taux de pertes.

Le projet répond aux demandes du sujet de simulation MAC.

---

## Structure du projet

```text
├── main.py
├── mac_simulator.py
├── experiences.py
├── plots.py
├── README.md
└── rapport.pdf
```

---

## Description des fichiers

### `mac_simulator.py`

Contient :
- la classe `Station`,
- la classe `Simulateur`,
- la gestion des événements :
  - arrivée,
  - début d’émission,
  - fin d’émission,
  - fin de backoff.

Le simulateur utilise un échéancier basé sur `heapq`.

---

### `experiences.py`

Contient les expériences :
- simulation simple,
- variation de λ,
- variation de N,
- estimation des intervalles de confiance à 95%.

---

### `plots.py`

Contient les fonctions permettant de tracer les courbes avec Matplotlib :
- évolution temporelle du débit,
- nombre moyen de clients,
- taux de pertes,
- courbes débit/fonction de λ ou N.

---

### `main.py`

Programme principal :
- lance les simulations,
- exécute les expériences,
- affiche les résultats,
- génère les graphiques.

---

## Installation

Installer les bibliothèques nécessaires :

```bash
pip install numpy matplotlib
```

---

## Exécution

Lancer le programme avec :

```bash
python main.py
```

---

## Paramètres principaux

Dans `main.py` :

```python
N = 5
K = 10
lmbda = 0.3
tau = 1.0
temps_max = 1000
```

- `N` : nombre de stations
- `K` : capacité des files
- `lmbda` : taux d’arrivée des paquets
- `tau` : paramètre du backoff
- `temps_max` : durée de simulation

---

## Résultats produits

Le programme permet de :
- tracer le débit \(n(t)/t\),
- observer le nombre moyen de clients,
- mesurer le taux de pertes,
- étudier l’impact de λ et N,
- calculer des intervalles de confiance à 95%.
