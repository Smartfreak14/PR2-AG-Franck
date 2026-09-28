"""
420-PR2-AG — Séance 6 — Démonstration 2
Valider, assainir, échapper : trois opérations, trois moments.

Exécution :  python3 02_demo_valider_echapper.py
"""

import html
import os
import re
import hashlib
import hmac
import urllib.parse


# ======================================================================
# 1. VALIDER — à l'entrée. On accepte ou on refuse, on ne modifie rien.
# ======================================================================
MATRICULE = re.compile(r"\d{7}")


def valider_matricule(saisie):
    # fullmatch, et non match : match s'arrêterait au 7e caractère et
    # accepterait "1234567abc".
    if not MATRICULE.fullmatch(saisie):
        raise ValueError("Matricule : 7 chiffres attendus.")
    return saisie


# ======================================================================
# 2. LISTE NOIRE contre LISTE BLANCHE
# ======================================================================
INTERDITS = ["DROP", "DELETE", "--", "'"]


def liste_noire(saisie):
    for mot in INTERDITS:
        if mot in saisie.upper():
            raise ValueError("Saisie refusée")
    return saisie


ROLES_AUTORISES = {"lecteur", "editeur", "admin"}


def liste_blanche(saisie):
    if saisie not in ROLES_AUTORISES:
        raise ValueError(f"Rôle inconnu : {saisie}")
    return saisie


# ======================================================================
# 3. ÉCHAPPER — à la sortie, selon la destination
# ======================================================================
def vers_page_html(commentaire):
    return html.escape(commentaire)


def vers_url(parametre):
    return urllib.parse.quote(parametre, safe="")


def vers_nom_de_fichier(nom):
    # basename retire tout chemin : "../../etc/passwd" devient "passwd"
    return os.path.basename(nom)


# ======================================================================
# 4. HACHAGE d'un mot de passe (A02)
# ======================================================================
def hacher(mot_de_passe):
    sel = os.urandom(16)
    empreinte = hashlib.pbkdf2_hmac(
        "sha256", mot_de_passe.encode("utf-8"), sel, 200_000)
    return sel.hex(), empreinte.hex()


def verifier(mot_de_passe, sel_hex, empreinte_hex):
    empreinte = hashlib.pbkdf2_hmac(
        "sha256", mot_de_passe.encode("utf-8"), bytes.fromhex(sel_hex), 200_000)
    # hmac.compare_digest évite de révéler la position du premier octet différent
    return hmac.compare_digest(empreinte.hex(), empreinte_hex)


if __name__ == "__main__":
    print("== Validation")
    for saisie in ["2026001", "20260", "1234567abc", "abcdefg"]:
        try:
            valider_matricule(saisie)
        except ValueError as e:
            print(f"  {saisie!r:15} refusé  — {e}")
        else:
            print(f"  {saisie!r:15} accepté")

    print("\n== Liste noire : contournée par une variante d'écriture")
    for saisie in ["DROP TABLE", "DrOp TaBlE", "DR/**/OP"]:
        try:
            liste_noire(saisie)
        except ValueError:
            print(f"  {saisie!r:15} refusé")
        else:
            print(f"  {saisie!r:15} ACCEPTÉ — la liste noire a laissé passer")

    print("\n== Liste blanche : tout ce qui n'est pas prévu est refusé")
    for saisie in ["admin", "administrateur", "AdMiN"]:
        try:
            liste_blanche(saisie)
        except ValueError as e:
            print(f"  {saisie!r:18} refusé — {e}")
        else:
            print(f"  {saisie!r:18} accepté")

    print("\n== Échappement selon la destination")
    donnee = "<script>alert(1)</script>"
    print("  HTML :", vers_page_html(donnee))
    print("  URL  :", vers_url("salle A/101"))
    print("  Nom de fichier :", vers_nom_de_fichier("../../etc/passwd"))

    print("\n== Hachage d'un mot de passe")
    sel, empreinte = hacher("MotDePasse1")
    print("  sel       :", sel)
    print("  empreinte :", empreinte[:40], "...")
    print("  vérification, bon mot de passe     :",
          verifier("MotDePasse1", sel, empreinte))
    print("  vérification, mauvais mot de passe :",
          verifier("MotDePasse2", sel, empreinte))
