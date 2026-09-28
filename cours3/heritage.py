class Utilisateur:
    def __init__(self, nom, courriel):
        self.nom = nom
        self.courriel = courriel

    def se_connecter(self):
        return f"Nom: {self.nom}, Courriel: {self.courriel} s'est connecté."

class Administrateur(Utilisateur):
    def __init__(self, nom, courriel, niveau):
        super().__init__(nom, courriel)
        self.niveau = niveau

    def afficher_niveau(self):
        return f"Administrateur {self.nom} a le niveau {self.niveau}."
    def suprimer_utilisateur(self, utilisateur):
        return f"Administrateur {self.nom} a supprimé l'utilisateur {utilisateur.nom}."


a = Administrateur("Alice", "alice@example.com", 5)
print(a.se_connecter())
print(a.afficher_niveau())
print(a.suprimer_utilisateur(Utilisateur("Bob", "bob@example.com")))