"""
420-PR2-AG — Séance 6 — Micro-exercice 1 (12 minutes)

Trois extraits, trois défauts. Pour chacun :
  1. nommez la famille OWASP (A01, A02 ou A03) et justifiez en une phrase ;
  2. corrigez l'extrait ;
  3. exécutez ce fichier pour montrer que la correction fonctionne.

Le bloc de démonstration en bas de fichier montre le problème AVANT correction.
Après vos corrections, il doit afficher un résultat différent — c'est le but.

Exécution :  python3 vulnerable.py
"""

import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE compte (nom TEXT, mdp TEXT)")
con.execute("CREATE TABLE note (id INTEGER, proprietaire TEXT, contenu TEXT)")
con.executemany("INSERT INTO compte VALUES (?, ?)",
                [("ana", "abc123"), ("luis", "Motdepasse!"), ("carla", "xyz")])
con.executemany("INSERT INTO note VALUES (?, ?, ?)",
                [(1, "ana", "Note privée d'Ana"),
                 (2, "luis", "Note privée de Luis")])


# ======================================================================
# EXTRAIT 1
# Famille OWASP : ..............
# Justification : ..............
# ======================================================================
def connexion(nom, mdp):
    r = f"SELECT * FROM compte WHERE nom='{nom}' AND mdp='{mdp}'"
    return con.execute(r).fetchone()


# ======================================================================
# EXTRAIT 2
# Cette fonction est appelée depuis /note/supprimer?id=...
# L'utilisateur connecté est passé en paramètre mais n'est pas utilisé.
#
# Famille OWASP : ..............
# Justification : ..............
# ======================================================================
def supprimer_note(id_note, utilisateur_connecte):
    con.execute("DELETE FROM note WHERE id = ?", (id_note,))
    con.commit()
    return f"Note {id_note} supprimée"


# ======================================================================
# EXTRAIT 3
# La requête est correctement paramétrée. Le défaut est ailleurs.
#
# Famille OWASP : ..............
# Justification : ..............
# ======================================================================
def creer_compte(nom, mdp):
    con.execute("INSERT INTO compte VALUES (?, ?)", (nom, mdp))
    con.commit()
    return f"Compte {nom} créé"


# ======================================================================
# Démonstration — à exécuter avant, puis après vos corrections
# ======================================================================
if __name__ == "__main__":
    print("== Extrait 1 — connexion")
    print("  mot de passe correct :", connexion("ana", "abc123"))
    print("  mot de passe inconnu :", connexion("ana", "mauvais"))
    print("  saisie forgée        :", connexion("ana", "x' OR '1'='1"))
    print("  -> si la dernière ligne retourne un compte, l'extrait est vulnérable")

    print("\n== Extrait 2 — suppression")
    print(" ", supprimer_note(2, "ana"))
    print("  -> Ana vient de supprimer la note de Luis")

    print("\n== Extrait 3 — création de compte")
    print(" ", creer_compte("mallory", "secret123"))
    print("  contenu de la table :")
    for ligne in con.execute("SELECT * FROM compte"):
        print("   ", ligne)
    print("  -> les mots de passe sont lisibles tels quels")
