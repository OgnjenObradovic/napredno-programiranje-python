# Druga nedjelja, mini projekat 1, slajdovi 17 i 20. Koliki je prihod hotela?
# Ranije bi jedna klasa ucitala rezervacije, izracunala cijenu i napisala izvjestaj.
# Ovdje svako ima po jedan posao. Probaj promijeniti izgled ispisa samo u klasi Ekran.
# Pokreni: python domaci_02.py
# Testovi: python -m pytest -q domaci_02.py

from dataclasses import dataclass  # Pravi konstruktor na osnovu navedenih polja.
from typing import Protocol  # Opisuje koje metode saradnik treba da ima.


@dataclass
class Rezervacija:
    noci: int
    cijena_noci: float


# Tri tacke znace da ovdje samo navodimo potpis metode.
class Izvor(Protocol):
    def ucitaj(self) -> list[Rezervacija]: ...


class Izvjestaj(Protocol):
    def prikazi(self, prihod: float) -> None: ...


def obradi(izvor: Izvor, izvjestaj: Izvjestaj) -> None:
    prihod = 0.0
    for gost in izvor.ucitaj():
        iznos = gost.noci * gost.cijena_noci
        prihod = prihod + iznos
    izvjestaj.prikazi(prihod)


class IzListe:
    def __init__(self, rezervacije: list[Rezervacija]):
        # self je ovaj konkretan objekat. Lista mu ostaje dostupna i u metodi ucitaj.
        self.rezervacije = rezervacije

    def ucitaj(self) -> list[Rezervacija]:
        return self.rezervacije


class Ekran:
    def prikazi(self, prihod: float) -> None:
        print("Prihod hotela:", prihod, "EUR")


ana = Rezervacija(2, 40)
ivo = Rezervacija(1, 100)
izvor = IzListe([ana, ivo])
obradi(izvor, Ekran())


# Test koristi listu umjesto stvarne hotelske evidencije. Rezultat citamo iz objekta umjesto sa ekrana. Oba izlaza imaju metodu prikazi, pa ista obrada radi sa oba.
class Biljeska:
    def __init__(self):
        self.prihod: float | None = None

    def prikazi(self, prihod: float) -> None:
        self.prihod = prihod


def test_prazan_hotel():
    zapis = Biljeska()
    obradi(IzListe([]), zapis)
    assert zapis.prihod == 0


def test_jedan_gost():
    zapis = Biljeska()
    gost = Rezervacija(2, 40)
    obradi(IzListe([gost]), zapis)
    assert zapis.prihod == 80


def test_dva_gosta():
    zapis = Biljeska()
    gosti = [Rezervacija(2, 40), Rezervacija(1, 100)]
    obradi(IzListe(gosti), zapis)
    assert zapis.prihod == 180
