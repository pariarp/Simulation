import numpy as np
from mac_simulator import Simulateur


# -------------------------------
# Simulation simple
# -------------------------------

def simulation_simple(N=5, K=10, lmbda=0.3, tau=1.0, temps_max=1000):
    """
    Lance une simulation avec des paramètres fixes
    retourne l'objet simulateur (pour accéder aux courbes et stats)
    """

    sim = Simulateur(N, K, lmbda, tau)
    sim.executer(temps_max)

    return sim


# -------------------------------
# Variation de lambda
# -------------------------------

def varier_lambda(lambdas, N=5, K=10, tau=1.0, temps_max=1000):
    """
    fait varier lambda et retourne le débit final pour chaque valeur

    lambdas : liste ou tableau de valeurs de lambda
    """

    debits = []

    # on parcourt toutes les valeurs de lambda
    for lmbda in lambdas:

        # on crée un nouveau simulateur pour chaque lambda
        sim = Simulateur(N, K, lmbda, tau)
        # on lance la simulation
        sim.executer(temps_max)
        # on récupère le débit final
        res = sim.resultats_finaux(temps_max)
        debits.append(res["debit"])

    return debits


# -------------------------------
# Variation du nombre de stations N
# -------------------------------

def varier_N(Ns, K=10, lmbda=0.3, tau=1.0, temps_max=1000):
    """
    fait varier le nombre de stations N
    retourne le débit pour chaque N
    """

    debits = []

    # pour chaque valeur de N
    for N in Ns:
        sim = Simulateur(N, K, lmbda, tau)
        sim.executer(temps_max)
        res = sim.resultats_finaux(temps_max)
        debits.append(res["debit"])
    return debits


# -------------------------------
# Intervalle de confiance 95%
# -------------------------------

def estimer_debit_IC95(N, K, lmbda, tau, temps_max=1000, repetitions=30):
    """
    estime le débit moyen et l'intervalle de confiance à 95%

    repetitions : nombre de simulations indépendantes
    """

    valeurs_debits = []

    # on répète la simulation plusieurs fois
    for i in range(repetitions):
        sim = Simulateur(N, K, lmbda, tau)
        sim.executer(temps_max)
        # on stocke le débit final de chaque simulation
        debit = sim.resultats_finaux(temps_max)["debit"]
        valeurs_debits.append(debit)

    # calcul de la moyenne
    moyenne = np.mean(valeurs_debits)

    # écart-type mesure si les valeurs sont dispersées ou concentrées autour de la moyenne, plus il est grand, plus les valeurs sont dispersées
    ecart_type = np.std(valeurs_debits, ddof=1)

    # formule IC 95%
    # 1.96 est la valeur critique pour une distribution normale à 95% (z-score)
    demi_largeur = 1.96 * ecart_type / np.sqrt(repetitions)

    borne_inf = moyenne - demi_largeur
    borne_sup = moyenne + demi_largeur

    return moyenne, borne_inf, borne_sup