import matplotlib.pyplot as plt


# -------------------------------
# Courbes d'évolution temporelle
# -------------------------------

def tracer_evolution(sim):
    """
    trace les courbes demandées pour une simulation :
    - débit n(t)/t
    - nombre moyen de clients
    - taux de pertes
    """

    # courbe du débit au cours du temps
    plt.figure()
    plt.plot(sim.temps, sim.debits)
    plt.xlabel("Temps")
    plt.ylabel("Débit n(t)/t")
    plt.title("Évolution du débit au cours du temps")
    plt.grid()
    plt.show()

    # courbe du nombre moyen de clients au cours du temps
    plt.figure()
    plt.plot(sim.temps, sim.clients_moyens)
    plt.xlabel("Temps")
    plt.ylabel("Nombre moyen de clients")
    plt.title("Évolution du nombre moyen de clients")
    plt.grid()
    plt.show()

    # courbe du taux de pertes au cours du temps
    plt.figure()
    plt.plot(sim.temps, sim.taux_pertes)
    plt.xlabel("Temps")
    plt.ylabel("Taux de pertes")
    plt.title("Évolution du taux de pertes")
    plt.grid()
    plt.show()


# -------------------------------
# Courbe générique
# -------------------------------

def tracer_courbe(x, y, xlabel, ylabel, titre):
    """
    trace une courbe simple y = f(x)
    utilisée pour :
    - débit en fonction de lambda
    - débit en fonction de N
    """

    plt.figure()
    plt.plot(x, y, marker="o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titre)
    plt.grid()
    plt.show()