class Facture:
    def __init__(self, numero):
        self.numero = numero
        self.lignes = []

    def ajouter(self,produit, quantite):
        self.lignes.append((Ligne(produit, quantite)))
        print(f"Facture n°{self.numero} : {quantite} x {produit} ajoutés à la facture.")

class Ligne:
    def __init__(self, produit, quantite):
        self.produit = produit
        self.quantite = quantite
    def __del__(self):
        print(f"Ligne supprimée : {self.quantite} x {self.produit}")

facture1 = Facture("001")
facture1.ajouter("Produit A", 2)

del facture1