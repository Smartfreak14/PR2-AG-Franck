"""
420-PR2-AG — Séance 5 — Démonstration 3
StringVar : le pont entre les champs de saisie et le code.

Le lien fonctionne dans les deux sens :
  - l'utilisateur tape       -> la variable change
  - le code appelle .set()   -> le champ affiché change

Exécution :  python3 03_variables.py
"""

import tkinter as tk
from tkinter import ttk

f = tk.Tk()
f.title("StringVar — le lien dans les deux sens")

date = tk.StringVar()
duree = tk.StringVar(value="60")          # valeur initiale


def lire():
    """Lit les champs sans jamais interroger les widgets eux-mêmes."""
    print("date  :", repr(date.get()))
    print("durée :", repr(duree.get()))


def prefixer():
    """Écrit dans le champ depuis le code."""
    date.set("2026-09-21")


def basculer_bouton():
    """state(["disabled"]) grise un widget, state(["!disabled"]) le réactive."""
    if "disabled" in bouton_lire.state():
        bouton_lire.state(["!disabled"])
    else:
        bouton_lire.state(["disabled"])


ttk.Label(f, text="Date").grid(row=0, column=0, sticky="w", padx=8, pady=4)
ttk.Entry(f, textvariable=date, width=20).grid(row=0, column=1, padx=8, pady=4)

ttk.Label(f, text="Durée (min)").grid(row=1, column=0, sticky="w", padx=8, pady=4)
ttk.Entry(f, textvariable=duree, width=20).grid(row=1, column=1, padx=8, pady=4)

bouton_lire = ttk.Button(f, text="Lire les champs", command=lire)
bouton_lire.grid(row=2, column=0, columnspan=2, sticky="we", padx=8, pady=4)

ttk.Button(f, text="Remplir la date depuis le code", command=prefixer
           ).grid(row=3, column=0, columnspan=2, sticky="we", padx=8, pady=4)

ttk.Button(f, text="Activer / désactiver le premier bouton", command=basculer_bouton
           ).grid(row=4, column=0, columnspan=2, sticky="we", padx=8, pady=(4, 12))

f.mainloop()
