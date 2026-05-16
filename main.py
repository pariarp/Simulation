"""
Point d'entrée principal du projet.
Exécute les différentes expériences demandées (simulation unitaire, variation 
de la charge lambda, variation de N et calculs d'intervalles de confiance).
"""

import numpy as np

from experiences import (
    simulation_simple,
    varier_lambda,
    varier_N,
    estimer_debit_IC95
)

from plots import (
    tracer_evolution,
    tracer_courbe,
    tracer_courbe_IC95
)

if __name__ == "__main__":

    # Paramètres de base
    N = 5
    K = 10
    lmbda = 0.3
    tau = 1.0
    temps_max = 1000

    # -------------------------------
    # 1. Simulation unitaire
    # -------------------------------
    print("===== Simulation simple =====")

    sim = simulation_simple(N, K, lmbda, tau, temps_max)
    res = sim.resultats_finaux(temps_max)

    print("Débit :", res["debit"])
    print("Clients moyens :", res["clients_moyens"])
    print("Taux de pertes :", res["taux_pertes"])

    tracer_evolution(sim)

    # -------------------------------
    # 2. Impact de la charge (lambda)
    # -------------------------------
    print("\n===== Variation de lambda =====")

    lambdas = np.linspace(0.05, 1.0, 10)
    debits_lambda = varier_lambda(lambdas, N, K, tau, temps_max)

    tracer_courbe(
        lambdas,
        debits_lambda,
        "Lambda",
        "Débit",
        "Débit en fonction de lambda", 
        "debit_lambda"
    )

    # -------------------------------
    # 3. Impact de la densité (N)
    # -------------------------------
    print("\n===== Variation de N =====")

    Ns = list(range(1, 21))
    debits_N = varier_N(Ns, K, lmbda, tau, temps_max)

    tracer_courbe(
        Ns,
        debits_N,
        "Nombre de stations N",
        "Débit",
        "Débit en fonction de N",
        "debit_N"
    )

    # -------------------------------
    # 4. Etude statistique (IC à 95%)
    # -------------------------------
    print("\n===== Intervalle de confiance (95%) =====")

    moyennes = []
    bornes_inf = []
    bornes_sup = []

    for N_test in Ns:
        moyenne, bas, haut = estimer_debit_IC95(
            N_test, K, lmbda, tau, temps_max
        )

        moyennes.append(moyenne)
        bornes_inf.append(bas)
        bornes_sup.append(haut)

        print(
            f"N={N_test} -> débit moyen={moyenne:.4f}, "
            f"Intervalle de confiance 95%=[{bas:.4f}, {haut:.4f}]"
        )
        
    tracer_courbe_IC95(
        Ns,
        moyennes,
        bornes_inf,
        bornes_sup,
        "Nombre de stations N",
        "Débit moyen",
        "Débit moyen en fonction de N avec IC95%",
        "debit_N_IC95"
    )