# Prva nedjelja, slajdovi 19, 21 i 25. Prosjecna cijena jedne prodate noci.
# Ana: 2 noci po 40 EUR. Ivo: 1 noc po 100 EUR. Prosjek: 180 / 3 = 60 EUR.
# Primjer: python domaci_01.py
# Testovi: python -m pytest -q domaci_01.py

import csv  # DictReader cita kolone po imenu iz prvog reda CSV tabele.
from pathlib import Path  # Putanja govori funkciji koji fajl treba otvoriti.


def prosjecna_cijena(putanja: Path) -> float:
    prihod = 0.0
    broj_noci = 0

    # with zatvara fajl kada zavrsimo citanje. Jedan prolaz petlje je jedan gost
    with putanja.open(encoding="utf-8", newline="") as fajl:
        for red in csv.DictReader(fajl):
            if "noci" not in red or "cijena_noci" not in red:
                raise ValueError("Provjeri nazive kolona.")
            if not red["noci"] or not red["cijena_noci"]:
                raise ValueError("Nedostaje broj noci ili cijena.")
            # int i float prijavljuju ValueError ako tekst nije broj.
            noci = int(red["noci"])
            cijena = float(red["cijena_noci"])

            if noci < 1 or cijena < 0:
                raise ValueError("Provjeri broj noci i cijenu.")

            iznos = noci * cijena
            prihod = prihod + iznos
            broj_noci = broj_noci + noci

    if broj_noci == 0:
        raise ValueError("Nema nocenja za obracun.")
    return prihod / broj_noci


# Pokreni iz foldera u kojem se nalazi rezervacije.csv.
print("Prosjecna cijena noci:", prosjecna_cijena(Path("rezervacije.csv")), "EUR")


# tmp_path je folder koji pytest pripremi za test
def test_razlicita_trajanja(tmp_path: Path):
    fajl = tmp_path / "rezervacije.csv"
    fajl.write_text("gost,noci,cijena_noci\nAna,2,40\nIvo,1,100\n", encoding="utf-8")
    assert prosjecna_cijena(fajl) == 60


def test_prazan_fajl(tmp_path: Path):
    fajl = tmp_path / "prazan.csv"
    fajl.write_text("", encoding="utf-8")
    greska = False
    try:
        prosjecna_cijena(fajl)
    except ValueError:
        greska = True
    assert greska


def test_neispravan_broj(tmp_path: Path):
    fajl = tmp_path / "greska.csv"
    fajl.write_text("gost,noci,cijena_noci\nAna,dva,40\n", encoding="utf-8")
    greska = False
    try:
        prosjecna_cijena(fajl)
    except ValueError:
        greska = True
    assert greska
