"""
420-PR2-AG — Séance 6 — Démonstration 1
Injection SQL : la même saisie, deux façons d'écrire la requête.

Base de données en mémoire : rien n'est écrit sur le disque, et le programme
ne se connecte à aucun serveur. Tout se passe dans ce fichier.

Exécution :  python3 01_demo_injection.py
"""

import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE utilisateur (nom TEXT, role TEXT)")
con.executemany("INSERT INTO utilisateur VALUES (?, ?)",
                [("ana", "lecteur"), ("luis", "admin"), ("carla", "editeur")])


# ----------------------------------------------------------------------
# Version vulnérable : la donnée est collée dans la requête
# ----------------------------------------------------------------------
def chercher_vulnerable(nom):
    requete = f"SELECT * FROM utilisateur WHERE nom = '{nom}'"
    print("   requête envoyée :", requete)
    return con.execute(requete).fetchall()


# ----------------------------------------------------------------------
# Version sûre : la donnée voyage séparément de la requête
# ----------------------------------------------------------------------
def chercher_sur(nom):
    return con.execute(
        "SELECT * FROM utilisateur WHERE nom = ?", (nom,)).fetchall()


# ----------------------------------------------------------------------
# Le cas du nom de colonne : un paramètre ne peut pas le remplacer
# ----------------------------------------------------------------------
TRIS_AUTORISES = {"nom", "role"}


def trier(colonne):
    if colonne not in TRIS_AUTORISES:
        raise ValueError(f"Colonne de tri non autorisée : {colonne}")
    return con.execute(
        f"SELECT * FROM utilisateur ORDER BY {colonne}").fetchall()


if __name__ == "__main__":
    saisie_normale = "ana"
    saisie_forgee = "x' OR '1'='1"

    print("== Version vulnérable, saisie normale")
    print("  ->", chercher_vulnerable(saisie_normale))

    print("\n== Version vulnérable, saisie forgée")
    print("  ->", chercher_vulnerable(saisie_forgee))
    print("  Toute la table est retournée : la condition est toujours vraie.")

    print("\n== Version paramétrée, saisie forgée")
    print("  ->", chercher_sur(saisie_forgee))
    print("  La chaîne est cherchée telle quelle : aucun résultat, aucune fuite.")

    print("\n== Nom de colonne : la liste blanche")
    print("  trier('nom')  ->", trier("nom"))
    try:
        trier("nom; DROP TABLE utilisateur")
    except ValueError as e:
        print("  refusé :", e)
