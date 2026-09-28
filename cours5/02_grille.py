"""
420-PR2-AG — Séance 5 — Démonstration 2
Le gestionnaire grid : row, column, sticky, padx/pady, columnspan.

À essayer en direct :
  - retirer sticky="w"      -> les libellés se centrent dans leur case
  - retirer padx et pady    -> tout se colle, l'interface devient illisible
  - retirer columnspan      -> le bouton se range dans la seule colonne 0
  - retirer columnconfigure -> les champs ne s'élargissent plus au redimensionnement

Exécution :  python3 02_grille.py
"""

import tkinter as tk
from tkinter import ttk

f = tk.Tk()
f.title("grid — les cinq options")

# --- ligne 0
ttk.Label(f, text="Salle").grid(row=0, column=0, sticky="w", padx=8, pady=4)
ttk.Entry(f).grid(row=0, column=1, sticky="we", padx=8, pady=4)

# --- ligne 1
ttk.Label(f, text="Date").grid(row=1, column=0, sticky="w", padx=8, pady=4)
ttk.Entry(f).grid(row=1, column=1, sticky="we", padx=8, pady=4)

# --- ligne 2 : le bouton occupe les deux colonnes
ttk.Button(f, text="Réserver").grid(row=2, column=0, columnspan=2, pady=8)

# La colonne 1 absorbe l'espace supplémentaire quand la fenêtre s'agrandit.
f.columnconfigure(1, weight=1)

# --- démonstration du « devinez le rendu » de la diapositive 15
#     La ligne 4 est volontairement vide : elle n'occupe aucune place,
#     sauf si on lui donne explicitement une hauteur minimale.
ttk.Label(f, text="A").grid(row=3, column=0)
ttk.Label(f, text="B").grid(row=3, column=1)
ttk.Label(f, text="C").grid(row=4, column=0, columnspan=2)
ttk.Label(f, text="D").grid(row=6, column=1)
# f.rowconfigure(5, minsize=20)   # décommenter pour faire apparaître l'espace

f.mainloop()
