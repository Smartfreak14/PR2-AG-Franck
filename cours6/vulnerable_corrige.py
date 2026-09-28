"""
420-PR2-AG — Séance 6 — Micro-exercice 1 : CORRIGÉ

Extrait 1 : A03 — Injection.
  La saisie est collée dans la requête : "x' OR '1'='1" transforme la condition
  en une condition toujours vraie, et la connexion réussit sans mot de passe.

Extrait 2 : A01 — Contrôle d'accès défaillant.
  La fonction supprime la note dont l'identifiant est fourni, sans vérifier que
  la note appartient à l'utilisateur connecté. Changer le numéro dans l'URL
  suffit pour supprimer la note de quelqu'un d'autre.

Extrait 3 : A02 — Défaillances cryptographiques.
  La requête est bien paramétrée, mais le mot de passe est stocké en clair.
  Une fuite de la base donne tous les comptes, et ceux des autres sites où le
  même mot de passe a été réutilisé.

Bonus : même une fois l'injection corrigée, comparer le mot de passe DANS la
requête SQL reste une erreur. La base ne doit contenir que des empreintes : la
comparaison se fait en mémoire, après avoir rehaché la saisie avec le sel stocké.

Exécution :  python3 vulnerable_corrige.py
"""

import sqlite3
import hashlib
import hmac
import os

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE compte (nom TEXT, sel TEXT, empreinte TEXT)")
con.execute("CREATE TABLE note (id INTEGER, proprietaire TEXT, contenu TEXT)")
con.executemany("INSERT INTO note VALUES (?, ?, ?)",
                [(1, "ana", "Note privée d'Ana"),
                 (2, "luis", "Note privée de Luis")])


class AccesRefuse(Exception):
    """L'utilisateur n'a pas le droit d'effectuer cette opération."""


# ======================================================================
# Outils de hachage (extrait 3)
# ======================================================================
ITERATIONS = 200_000


def _hacher(mot_de_passe, sel):
    return hashlib.pbkdf2_hmac(
        "sha256", mot_de_passe.encode("utf-8"), sel, ITERATIONS).hex()


# ======================================================================
# EXTRAIT 1 — corrigé : requête paramétrée + comparaison en mémoire
# ======================================================================
def connexion(nom, mdp):
    ligne = con.execute(
        "SELECT sel, empreinte FROM compte WHERE nom = ?", (nom,)).fetchone()
    if ligne is None:
        return None                      # compte inconnu
    sel_hex, empreinte_attendue = ligne
    empreinte = _hacher(mdp, bytes.fromhex(sel_hex))
    if not hmac.compare_digest(empreinte, empreinte_attendue):
        return None                      # mot de passe incorrect
    return nom


# ======================================================================
# EXTRAIT 2 — corrigé : l'appartenance est vérifiée avant l'action
# ======================================================================
def supprimer_note(id_note, utilisateur_connecte):
    ligne = con.execute(
        "SELECT proprietaire FROM note WHERE id = ?", (id_note,)).fetchone()
    if ligne is None or ligne[0] != utilisateur_connecte:
        # Le même message dans les deux cas : ne pas révéler si la note existe.
        raise AccesRefuse("Note introuvable ou inaccessible.")
    con.execute("DELETE FROM note WHERE id = ?", (id_note,))
    con.commit()
    return f"Note {id_note} supprimée"


# ======================================================================
# EXTRAIT 3 — corrigé : seule l'empreinte est stockée
# ======================================================================
def creer_compte(nom, mdp):
    if len(mdp) < 8:
        raise ValueError("Mot de passe : 8 caractères minimum.")
    sel = os.urandom(16)
    con.execute("INSERT INTO compte VALUES (?, ?, ?)",
                (nom, sel.hex(), _hacher(mdp, sel)))
    con.commit()
    return f"Compte {nom} créé"


if __name__ == "__main__":
    creer_compte("ana", "abc12345")
    creer_compte("luis", "Motdepasse!")

    print("== Extrait 1 — connexion")
    print("  mot de passe correct :", connexion("ana", "abc12345"))
    print("  mot de passe inconnu :", connexion("ana", "mauvais"))
    print("  saisie forgée        :", connexion("ana", "x' OR '1'='1"))
    print("  -> seule la première ligne retourne un compte")

    print("\n== Extrait 2 — suppression")
    try:
        supprimer_note(2, "ana")
    except AccesRefuse as e:
        print("  Ana tente de supprimer la note de Luis ->", e)
    print(" ", supprimer_note(1, "ana"), "(sa propre note)")

    print("\n== Extrait 3 — création de compte")
    print("  contenu de la table :")
    for nom, sel, empreinte in con.execute("SELECT * FROM compte"):
        print(f"    {nom:6} sel={sel[:12]}...  empreinte={empreinte[:24]}...")
    print("  -> aucun mot de passe lisible")
