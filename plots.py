import matplotlib.pyplot as plt

def appliquer_style():
    """Applique un style graphique unifié pour toutes les figures générées."""
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

def tracer_evolution(sim):
    """Génère les courbes suivi temporel du système (régime transitoire/stationnaire)."""
    # Débit au cours du temps
    plt.figure()
    plt.plot(sim.temps, sim.debits)
    plt.xlabel("Temps")
    plt.ylabel("Débit n(t)/t")
    plt.title("Évolution du débit au cours du temps")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/debit_temps.png", dpi=300)
    plt.show()

    # Nombre moyen de cliens au cours du temps
    plt.figure()
    plt.plot(sim.temps, sim.clients_moyens)
    plt.xlabel("Temps")
    plt.ylabel("Nombre moyen de clients")
    plt.title("Évolution du nombre moyen de clients")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/clients_moyens_temps.png", dpi=300)
    plt.show()

    # Taux de pertes au cours du temps
    plt.figure()
    plt.plot(sim.temps, sim.taux_pertes)
    plt.xlabel("Temps")
    plt.ylabel("Taux de pertes")
    plt.title("Évolution du taux de pertes")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/taux_pertes_temps.png", dpi=300)
    plt.show()

def tracer_courbe(x, y, xlabel, ylabel, titre, nom_fichier=None):
    """Génère une courbe standard bidimensionnelle y = f(x)."""
    plt.figure()
    plt.plot(x, y, marker="o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titre)
    plt.grid()
    if nom_fichier is not None:
        plt.savefig(f"images/{nom_fichier}.png", dpi=300)
    plt.show()

def tracer_courbe_IC95(x, moyennes, bornes_inf, bornes_sup, xlabel, ylabel, titre, nom_fichier=None):
    """Génère une courbe avec barres d'erreur (intervalles de confiance à 95%)."""
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

    # Zone optimale identifiée empiriquement
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