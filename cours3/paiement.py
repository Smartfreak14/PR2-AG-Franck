from abc import ABC, abstractmethod


class MoyenPaiement(ABC):
    """Interface commune : tout moyen de paiement doit pouvoir payer."""

    @abstractmethod
    def payer(self, montant):
        """Effectue un paiement et retourne un message de confirmation."""
        pass


class Carte(MoyenPaiement):
    def payer(self, montant):
        return f"Paiement de {montant:.2f} $ effectué par carte."


class Interac(MoyenPaiement):
    def payer(self, montant):
        return f"Paiement de {montant:.2f} $ effectué par Interac."


class Comptant(MoyenPaiement):
    def payer(self, montant):
        return f"Paiement comptant de {montant:.2f} $ effectué."


print("=== Démonstration du polymorphisme ===")
moyens_de_paiement = [Carte(), Interac(), Comptant()]

for m in moyens_de_paiement:
    print(m.payer(50))


print("""
Les trois concepts
------------------
1. Classe abstraite : MoyenPaiement ne sert pas à créer directement un objet.
   Elle impose la méthode payer aux classes enfants.

2. Interface : MoyenPaiement définit le contrat commun payer(montant).
   Le code qui utilise un moyen de paiement n'a pas besoin de connaître
   les détails de Carte, Interac ou Comptant.

3. Polymorphisme : la même instruction m.payer(50) fonctionne avec chaque
   objet, mais son comportement dépend de la classe réelle de m.

Apport : on peut ajouter un nouveau moyen de paiement sans modifier la boucle
qui utilise payer. Le code est donc plus flexible, réutilisable et maintenable.
""")