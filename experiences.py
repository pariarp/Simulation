import numpy as np
from mac_simulator import Simulateur

def simulation_simple(N=5, K=10, lmbda=0.3, tau=1.0, temps_max=1000):
    """
    Lance une simulation avec des paramètres fixes et
    retourne l'instance du simulateur
    """
    sim = Simulateur(N, K, lmbda, tau)
    sim.executer(temps_max)
    return sim

def varier_lambda(lambdas, N=5, K=10, tau=1.0, temps_max=1000):
    """
    Evalue l'évolution du débit en fonction du taux d'arrivée (lambda)
    """
    debits = []

    for lmbda in lambdas:
        sim = Simulateur(N, K, lmbda, tau)
        sim.executer(temps_max)
        res = sim.resultats_finaux(temps_max)
        debits.append(res["debit"])
    return debits

def varier_N(Ns, K=10, lmbda=0.3, tau=1.0, temps_max=1000):
    """
    Evalue l'évolution du débit pour différentes valeurs de stations N.
    """
    debits = []
    for N in Ns:
        sim = Simulateur(N, K, lmbda, tau)
        sim.executer(temps_max)
        res = sim.resultats_finaux(temps_max)
        debits.append(res["debit"])
    return debits

def estimer_debit_IC95(N, K, lmbda, tau, temps_max=1000, repetitions=30):
    """
    Calcule le débit moyen et son intervalle de confiance à 95%
    via des réplications indépendantes (méthode de Monte-Carlo).
    """
    valeurs_debits = []

    for i in range(repetitions):
        sim = Simulateur(N, K, lmbda, tau)
        sim.executer(temps_max)
        debit = sim.resultats_finaux(temps_max)["debit"]
        valeurs_debits.append(debit)

    moyenne = np.mean(valeurs_debits)
    ecart_type = np.std(valeurs_debits, ddof=1)

    demi_largeur = 1.96 * ecart_type / np.sqrt(repetitions)
    borne_inf = moyenne - demi_largeur
    borne_sup = moyenne + demi_largeur

    return moyenne, borne_inf, borne_sup