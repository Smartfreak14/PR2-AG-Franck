class Configuration:
    """Singleton : une seule configuration partagee par toute l'application."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialiser()
        return cls._instance

    def _initialiser(self):
        self.valeurs = {
            "application": "Station meteo",
            "unite_temperature": "C",
            "intervalle_lecture": 5,
        }

    def obtenir(self, nom):
        return self.valeurs.get(nom)

    def modifier(self, nom, valeur):
        self.valeurs[nom] = valeur


def demo():
    configuration_1 = Configuration()
    configuration_2 = Configuration()

    print("=== Singleton : configuration partagee ===")
    print(f"Meme objet : {configuration_1 is configuration_2}")
    configuration_1.modifier("unite_temperature", "F")
    print(f"Valeur vue par configuration_2 : "
          f"{configuration_2.obtenir('unite_temperature')}")

    print("""
Le Singleton garantit qu'une classe ne possede qu'une seule instance.
Ici, Configuration centralise les reglages de l'application. Peu importe

le nombre de fois ou Configuration() est appele, on retrouve le meme objet.

Apport : tous les modules lisent et modifient les memes reglages.
Attention : ce patron introduit un etat global ; il faut donc l'utiliser
avec moderation, car il peut rendre les tests plus difficiles a isoler.
""")


if __name__ == "__main__":
    demo()