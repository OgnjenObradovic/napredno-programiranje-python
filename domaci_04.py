# Nedjelja 4. Prepoznaj vrstu cvijeta na osnovu duzine latice.
# Pokretanje: python domaci_04.py
# Provjera: python -m pytest -q domaci_04.py
# Provjera na papiru:
# od tri vrste [0, 1, 2] pogodjene su dvije ako je prognoza [0, 0, 2].

import csv  # Iz skupa Iris citamo duzinu latice i oznaku vrste (0, 1 ili 2).
from abc import ABC, abstractmethod  # Podklasa popunjava korak za ucitavanje podataka.
from time import perf_counter  # Razlika dva ocitavanja daje trajanje treninga.


class NajbliziCvijet:
    def uci(self, mjerenja, vrste):
        self.mjerenja = mjerenja
        self.vrste = vrste

    def predvidi(self, duzina):
        # Svaku laticu uporedimo sa primjerima za ucenje. Kvadrat razlike
        # daje isti rezultat ako smo jednako udaljeni lijevo ili desno.
        najbolji = 0
        for i, poznata in enumerate(self.mjerenja):
            razlika = (poznata - duzina) ** 2
            najbolja_razlika = (self.mjerenja[najbolji] - duzina) ** 2
            if razlika < najbolja_razlika:
                najbolji = i
        return self.vrste[najbolji]


class NajcescaVrsta:
    def uci(self, mjerenja, vrste):
        broj = [0, 0, 0]
        for vrsta in vrste:
            broj[vrsta] += 1
        self.vrsta = 0
        for vrsta in range(3):
            if broj[vrsta] > broj[self.vrsta]:
                self.vrsta = vrsta

    def predvidi(self, duzina):
        # Ovaj jednostavni model uvijek bira najcescu vrstu iz treninga.
        return self.vrsta


def napravi_model(naziv):
    if naziv == "najblizi":
        return NajbliziCvijet()
    if naziv == "najcesci":
        return NajcescaVrsta()
    raise ValueError("Izaberi najblizi ili najcesci.")


# Strategy. Obje funkcije primaju iste podatke. Prva vraca broj, druga udio.
def broj_pogodaka(stvarne_vrste, prognoze):
    pogodaka = 0
    for stvarna, prognoza in zip(stvarne_vrste, prognoze):
        if stvarna == prognoza:
            pogodaka += 1
    return pogodaka


def tacnost(stvarne_vrste, prognoze):
    return broj_pogodaka(stvarne_vrste, prognoze) / len(stvarne_vrste)


# Decorator. Metoda koju mjerimo prima samo self, pa i omotac prima samo self.
def mjeri_vrijeme(metoda):
    def izmjerena(self):
        pocetak = perf_counter()
        ocjena = metoda(self)
        trajanje = perf_counter() - pocetak
        print(f"Trajanje eksperimenta: {trajanje:.3f} s")
        return ocjena

    return izmjerena


class Eksperiment(ABC):
    def __init__(self, naziv, metrika):
        self.model = napravi_model(naziv)
        self.metrika = metrika
        self.slusaoci = []

    # Observer. Slusalac je funkcija koju pozivamo kada se desi promjena.
    def pretplati(self, slusalac):
        self.slusaoci.append(slusalac)

    def obavijesti(self, poruka):
        for slusalac in self.slusaoci:
            slusalac(poruka)

    @abstractmethod
    def podaci(self): ...

    # Template Method. Isti koraci vaze za svaki skup podataka.
    @mjeri_vrijeme
    def pokreni(self):
        mjerenja, vrste = self.podaci()
        # Svaki peti cvijet ide u provjeru. Ostale koristimo za ucenje.
        # Tako medju 30 izdvojenih cvjetova imamo primjere sve tri vrste.
        ucenje = []
        provjera = []
        vrste_ucenje = []
        vrste_provjera = []
        for indeks, cvijet in enumerate(mjerenja):
            if (indeks + 1) % 5 == 0:
                provjera.append(cvijet)
                vrste_provjera.append(vrste[indeks])
            else:
                ucenje.append(cvijet)
                vrste_ucenje.append(vrste[indeks])
        self.obavijesti("Pocetak treninga")
        self.model.uci(ucenje, vrste_ucenje)
        self.obavijesti("Kraj treninga")
        prognoze = [self.model.predvidi(duzina) for duzina in provjera]
        return self.metrika(vrste_provjera, prognoze)


class IrisEksperiment(Eksperiment):
    def podaci(self):
        duzine = []
        vrste = []
        with open("iris.csv", newline="", encoding="utf-8") as fajl:
            for red in csv.DictReader(fajl):
                duzine.append(float(red["duzina"]))
                vrste.append(int(red["vrsta"]))
        return duzine, vrste


# Mermaid dijagram za opis projekta:
# classDiagram
#     IrisEksperiment --|> Eksperiment
#     Eksperiment ..> Fabrika : bira model
#     Eksperiment ..> Metrika : ocjenjuje
#     Eksperiment ..> Slusalac : javlja promjenu
# Fabrika, metrika i slusalac u nasem kodu su funkcije.

ogled = IrisEksperiment("najblizi", broj_pogodaka)
ogled.pretplati(print)
print("Pogodjeno od 30 cvjetova:", ogled.pokreni())


def test_broj_pogodaka():
    assert broj_pogodaka([0, 1, 2], [0, 0, 2]) == 2


def test_tacnost():
    assert tacnost([0, 1], [1, 1]) == 0.5


def test_najblizi():
    model = napravi_model("najblizi")
    model.uci([1, 5], [0, 2])
    assert model.predvidi(4) == 2


def test_najcesci():
    model = napravi_model("najcesci")
    model.uci([1, 4, 5], [0, 2, 2])
    assert model.predvidi(1) == 2


def test_nepoznat_naziv():
    poruka = ""
    try:
        napravi_model("nepoznat")
    except ValueError as greska:
        poruka = str(greska)
    assert poruka == "Izaberi najblizi ili najcesci."


def test_tok_eksperimenta():
    poruke = []
    ogled = IrisEksperiment("najblizi", tacnost)
    ogled.pretplati(poruke.append)
    rezultat = ogled.pokreni()
    assert poruke == ["Pocetak treninga", "Kraj treninga"]
    assert 0.8 < rezultat <= 1
