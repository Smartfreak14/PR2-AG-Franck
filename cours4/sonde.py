from abc import ABC, abstractmethod


class Sonde(ABC):
    """Produit abstrait : toutes les sondes savent mesurer."""

    @abstractmethod
    def mesurer(self):
        pass


class SondeTemperature(Sonde):
    def mesurer(self):
        return {"type": "temperature", "valeur": 22.5, "unite": "C"}


class SondeHumidite(Sonde):
    def mesurer(self):
        return {"type": "humidite", "valeur": 48, "unite": "%"}


class SondePression(Sonde):
    def mesurer(self):
        return {"type": "pression", "valeur": 1013, "unite": "hPa"}


class FabriqueSonde:
    """Fabrique : cree la sonde demandee sans exposer sa construction."""

    _sondes = {
        "temperature": SondeTemperature,
        "humidite": SondeHumidite,
        "pression": SondePression,
    }

    @classmethod
    def creer(cls, type_sonde):
        classe_sonde = cls._sondes.get(type_sonde.lower())
        if classe_sonde is None:
            types_acceptes = ", ".join(cls._sondes)
            raise ValueError(f"Type inconnu. Choisissez : {types_acceptes}")
        return classe_sonde()


def demo():
    print("=== Factory : fabrication de sondes ===")
    for type_sonde in ("temperature", "humidite", "pression"):
        sonde = FabriqueSonde.creer(type_sonde)
        print(sonde.mesurer())

    print("""
La Factory centralise la creation des objets. Le client demande seulement
un type de sonde ; il ne doit pas connaitre le nom de la classe concrete.

Apport : la construction est centralisee, le code client est plus simple et
ajouter une nouvelle sonde se fait principalement dans la fabrique.
La Factory est utile quand la creation depend d'un choix, d'un parametre
ou d'une regle qui ne doit pas etre repete dans tout le programme.
""")


if __name__ == "__main__":
    demo()