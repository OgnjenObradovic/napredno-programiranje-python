# Nedjelja 6. Kako da znamo da ponuda hotela zaista radi?
# Pokreni: python -m pytest -q domaci_06.py
# Svaki test salje zahtjev i uporedjuje odgovor sa rezultatom poznatim unaprijed.
# Kod 200 znaci uspjeh, a 422 znaci da ulaz ne ispunjava pravila iz nedjelje 5.
#
# Rizici i mjere:
# 1. Negativan popust bi povecao racun. Pydantic provjerava granice.
# 2. Cijenu salje gost. Rezultat sluzi za ponudu. Za naplatu cijenu treba
#    uzeti iz hotelskog cjenovnika i provjeriti pravo korisnika na naplatu.
# 3. Privatni podaci mogu ostati u logovima. API koristi samo brojeve,
#    a tijelo zahtjeva se u nasem kodu ne upisuje u log.
# 4. Zavisnosti mogu imati poznate propuste. pip-audit provjerava verzije.
#
# Provjere za predaju: ruff check domaci_05.py domaci_06.py
# mypy --strict domaci_05.py
# bandit domaci_05.py
# pip-audit

import pytest  # parametrize ponavlja isti postupak za razlicite ulaze.
from fastapi.testclient import TestClient  # Salje zahtjeve direktno aplikaciji.

from domaci_05 import app  # Provjeravamo upravo kod iz petog domaceg.

klijent = TestClient(app)


def test_dostupnost():
    odgovor = klijent.get("/health")
    assert odgovor.status_code == 200
    assert odgovor.json() == {"status": "ok"}


def test_bez_popusta():
    zahtjev = {"noci": 3, "cijena_noci": 80}
    odgovor = klijent.post("/cijena", json=zahtjev)
    assert odgovor.status_code == 200
    assert odgovor.json() == {"iznos": 240}


def test_deset_posto():
    zahtjev = {"noci": 3, "cijena_noci": 80, "popust": 0.10}
    odgovor = klijent.post("/cijena", json=zahtjev)
    assert odgovor.json()["iznos"] == 216


def test_pun_popust():
    zahtjev = {"noci": 2, "cijena_noci": 50, "popust": 1}
    odgovor = klijent.post("/cijena", json=zahtjev)
    assert odgovor.json()["iznos"] == 0


# U svakom pokretanju pytest ubaci narednu vrijednost u parametar noci.
@pytest.mark.parametrize("noci", [1, 30])
def test_dozvoljene_granice(noci):
    zahtjev = {"noci": noci, "cijena_noci": 10}
    odgovor = klijent.post("/cijena", json=zahtjev)
    assert odgovor.json()["iznos"] == noci * 10


@pytest.mark.parametrize("noci", [-1, 0, 31, 1.5])
def test_neispravne_noci(noci):
    zahtjev = {"noci": noci, "cijena_noci": 80}
    odgovor = klijent.post("/cijena", json=zahtjev)
    assert odgovor.status_code == 422


@pytest.mark.parametrize("popust", [-0.01, 1.01])
def test_neispravan_popust(popust):
    zahtjev = {"noci": 1, "cijena_noci": 80, "popust": popust}
    odgovor = klijent.post("/cijena", json=zahtjev)
    assert odgovor.status_code == 422


@pytest.mark.parametrize("cijena", [0, -1, "abc"])
def test_neispravna_cijena(cijena):
    zahtjev = {"noci": 1, "cijena_noci": cijena}
    odgovor = klijent.post("/cijena", json=zahtjev)
    assert odgovor.status_code == 422


def test_nedostaje_cijena():
    odgovor = klijent.post("/cijena", json={"noci": 1})
    assert odgovor.status_code == 422


def test_decimalna_cijena():
    zahtjev = {"noci": 3, "cijena_noci": 12.34, "popust": 0.15}
    odgovor = klijent.post("/cijena", json=zahtjev)
    assert odgovor.json()["iznos"] == pytest.approx(31.467)


def test_pogresna_metoda():
    odgovor = klijent.get("/cijena")
    assert odgovor.status_code == 405
