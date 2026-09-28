"""
420-PR2-AG — Séance 5 — Démonstration 1
Anatomie d'une fenêtre Tkinter : trois étapes, rien de plus.

Exécution :  python3 01_fenetre_minimale.py
"""

import tkinter as tk
from tkinter import ttk

# 1. La fenêtre racine — il n'y en a qu'une seule par application.
fenetre = tk.Tk()
fenetre.title("Réservation de salles")

# 2. Les widgets — chacun reçoit son conteneur en premier argument.
ttk.Label(fenetre, text="Salle").pack(padx=20, pady=20)

# 3. La boucle principale — le programme attend les actions de l'utilisateur.
#    Toute ligne écrite après mainloop() ne s'exécute qu'à la fermeture.
fenetre.mainloop()

print("Cette ligne ne s'affiche qu'après la fermeture de la fenêtre.")
