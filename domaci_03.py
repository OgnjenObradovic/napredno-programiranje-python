# Treca nedjelja. Mini projekat 1 je u domaci_02.py. Ovdje radimo radionicu sa slajda 20.
# A. Factory stvara tarifu prema imenu iz podesavanja. Ima smisla kada biramo izmedju vise tarifa.
# B. Adapter pretvara cente starog sistema u eure koje ocekuje novi sistem.
# C. Facade nudi jedan poziv za dostupnost, obracun, naplatu i potvrdu sa pet mjesta u programu.
# D. Decorator dodaje popust ili taksu kad korisnik bira razlicite kombinacije.
# Skica odnosa: A Fabrika -> Tarifa; B Adapter -> StariCjenovnik;
# C Fasada -> Provjera, Obracun, Naplata, Potvrda; D SaPopustom -> Tarifa.
# Implementirani primjeri A i B. Za jednu jedinu konverziju dovoljna bi bila funkcija.
# Pokreni: python domaci_03.py
# Testovi: python -m pytest -q domaci_03.py

class Standardna:
    def cijena(self, osnovna: float) -> float:
        return osnovna


class Sezonska:
    def cijena(self, osnovna: float) -> float:
        return osnovna * 1.2


class Promotivna:
    def cijena(self, osnovna: float) -> float:
        return osnovna * 0.8


# Registar iz slajda 9. Uz ime cuvamo klasu koju fabrika treba da pozove.
tarife = {"standardna": Standardna, "sezonska": Sezonska, "promotivna": Promotivna}


def napravi_tarifu(naziv: str):
    if naziv not in tarife:
        raise ValueError("Nepoznata tarifa: " + naziv)
    klasa = tarife[naziv]
    return klasa()


class StariCjenovnik:
    def cijena_u_centima(self) -> int:
        return 7999


class AdapterCijene:
    def __init__(self, cjenovnik: StariCjenovnik):
        self.cjenovnik = cjenovnik

    def cijena_u_eurima(self) -> float:
        # Stari sistem moze nastaviti da koristi cente. Pretvaramo samo na izlazu.
        centi = self.cjenovnik.cijena_u_centima()
        return centi / 100


tarifa = napravi_tarifu("promotivna")
print("Promotivna tarifa:", tarifa.cijena(100), "EUR")
adapter = AdapterCijene(StariCjenovnik())
print("Cijena iz starog sistema:", adapter.cijena_u_eurima(), "EUR")


def test_tri_tarife():
    assert napravi_tarifu("standardna").cijena(100) == 100
    assert napravi_tarifu("sezonska").cijena(100) == 120
    assert napravi_tarifu("promotivna").cijena(100) == 80


def test_nepoznata_tarifa():
    poruka = ""
    try:
        napravi_tarifu("zimska")
    except ValueError as greska:
        poruka = str(greska)
    assert poruka == "Nepoznata tarifa: zimska"


def test_adapter():
    adapter = AdapterCijene(StariCjenovnik())
    assert adapter.cijena_u_eurima() == 79.99
