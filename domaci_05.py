# Nedjelja 5. Predlog zavrsnog projekta: hotelski asistent za gosta.
# Gost na telefonu moze da procita hotelska pravila i izracuna ponudu.
# Za tri programera biramo modularni monolit: jedna aplikacija sa dijelom
# za hotelske dokumente i dijelom za racunanje. Budzet je 100 EUR mjesecno.
# Radionica u folderu iznad projekta opisuje dokumente i pretragu na dva jezika.
# Ovdje pravimo prvi izvrsivi dio: ponudu za boravak.
#
# Pokreni: python -m uvicorn domaci_05:app
# Otvori http://127.0.0.1:8000/docs i probaj POST /cijena sa ovim podacima:
# {"noci": 3, "cijena_noci": 80, "popust": 0.10}
# Na papiru: 3 * 80 = 240, popust je 24, gost dobija ponudu od 216 EUR.

from fastapi import FastAPI  # Povezuje adresu i Python funkciju.
from pydantic import BaseModel, Field  # Opisuju polja i granice pri unosu.

app = FastAPI(title="Ponuda za boravak")


class Zahtjev(BaseModel):
    # ge znaci vece ili jednako, le manje ili jednako, a gt strogo vece.
    noci: int = Field(ge=1, le=30)
    cijena_noci: float = Field(gt=0)
    popust: float = Field(default=0, ge=0, le=1)


class Ponuda(BaseModel):
    iznos: float


@app.post("/cijena", response_model=Ponuda)
def cijena(zahtjev: Zahtjev) -> Ponuda:
    # Za sva polja koja je poslao gost koristimo isti objekat zahtjev.
    puna_cijena = zahtjev.noci * zahtjev.cijena_noci
    iznos_popusta = puna_cijena * zahtjev.popust
    za_placanje = puna_cijena - iznos_popusta
    return Ponuda(iznos=za_placanje)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
