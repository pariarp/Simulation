import matplotlib.pyplot as plt

def appliquer_style():
    plt.rcParams.update({
        "figure.figsize": (8, 5),
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.fontsize": 11,
        "lines.linewidth": 2,
        "lines.markersize": 6,
        "grid.alpha": 0.35,
    })


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
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/debit_temps.png", dpi=300)
    plt.show()

    # courbe du nombre moyen de clients au cours du temps
    plt.figure()
    plt.plot(sim.temps, sim.clients_moyens)
    plt.xlabel("Temps")
    plt.ylabel("Nombre moyen de clients")
    plt.title("Évolution du nombre moyen de clients")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/clients_moyens_temps.png", dpi=300)
    plt.show()

    # courbe du taux de pertes au cours du temps
    plt.figure()
    plt.plot(sim.temps, sim.taux_pertes)
    plt.xlabel("Temps")
    plt.ylabel("Taux de pertes")
    plt.title("Évolution du taux de pertes")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/taux_pertes_temps.png", dpi=300)
    plt.show()


# -------------------------------
# Courbe générique
# -------------------------------

def tracer_courbe(x, y, xlabel, ylabel, titre, nom_fichier=None):
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

def tracer_courbe_IC95(x, moyennes, bornes_inf, bornes_sup, xlabel, ylabel, titre, nom_fichier=None):
    appliquer_style()

    erreurs_inf = [m - b for m, b in zip(moyennes, bornes_inf)]
    erreurs_sup = [h - m for m, h in zip(moyennes, bornes_sup)]

    plt.figure()
    plt.errorbar(
        x,
        moyennes,
        yerr=[erreurs_inf, erreurs_sup],
        marker="o",
        capsize=5,
        linewidth=2
    )

    # Mettre en évidence la zone optimale N = 7 à 9
    plt.axvspan(7, 9, alpha=0.15, label="Zone optimale estimée")

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titre)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if nom_fichier is not None:
        plt.savefig(f"images/{nom_fichier}.png", dpi=300)

    plt.show()