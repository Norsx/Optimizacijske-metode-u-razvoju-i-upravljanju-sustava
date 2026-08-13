# Skripta — Optimizacijske metode u razvoju i upravljanju sustava

Samostalna skripta za učenje gradiva od nule, sastavljena **isključivo** iz
predavanja i vježbi u `data/sources/`. Svaka formula, izvod i postupak rješavanja
preuzeti su iz izvornika; ništa nije nadopunjeno iz drugih izvora.

## Redoslijed čitanja

| # | Datoteka | Izvor |
|---|---|---|
| 1 | [01-uvod.md](01-uvod.md) | `01_Uvod.pdf` |
| 2 | [02-definicije-klasifikacija-konveksnost.md](02-definicije-klasifikacija-konveksnost.md) | `02_Definicije_klasifikacija_konveksnost.pdf` + `Vjezbe_1.pdf` + `Vjezbe_2.pdf` |
| 3 | [03-uvjeti-optimalnosti.md](03-uvjeti-optimalnosti.md) | `03_Uvjeti_optimalnosti.pdf` |
| 4 | [04-lagrangeova-dualnost.md](04-lagrangeova-dualnost.md) | `04_Lagrangeova_dualnost.pdf` + `Vjezbe_3.pdf` |
| 5 | [05-lp-qp.md](05-lp-qp.md) | `05_LP_QP.pdf` + `Vjezbe_4.pdf` + `Vjezbe_5.pdf` (zad. 1) |
| 6 | [06-qcp-sdp.md](06-qcp-sdp.md) | `06_QCP_SDP.pdf` + `Vjezbe_4.pdf` (geometrijski problemi) |
| 7 | [07-dinamicki-sustavi-ljapunov-disipativnost.md](07-dinamicki-sustavi-ljapunov-disipativnost.md) | `07_Dinamicki_sustavi_Ljapunov_disipativnost.pdf` + `Vjezbe_5.pdf` (zad. 2) |
| 8 | [08-robusno-optimiranje.md](08-robusno-optimiranje.md) | `08_Robusno_optimiranje.pdf` |

## Mapiranje vježbi na poglavlja

Mapiranje je utvrđeno **čitanjem stvarnog sadržaja** svake vježbe, a ne prema
rednom broju. Zadaci su ugrađeni **inline**, odmah iza teorije koju koriste; zadaci
koji dodiruju više tema razlomljeni su po podzadacima.

| Vježba | Stvaran sadržaj | Ide u poglavlje |
|---|---|---|
| `Vjezbe_1.pdf` | vektori/matrice, funkcije, linearne i afine funkcije, nivo krivulje, skalarni produkt, hiperravnine i poluprostori, poliedar/politop, vektorske norme; zadaci 1–4 | 2 |
| `Vjezbe_2.pdf` | konveksan opt. problem, norme kao konveksne funkcije, minimizacija norme; Primjer 1 | 2 |
| `Vjezbe_3.pdf` | Primjer 1 — tržište i formiranje cijena; Primjer 2 — dualnost, KKT, osjetljivost | 4 (dijelovi KKT-a i u 3) |
| `Vjezbe_4.pdf` | aproksimacije, regularizirana aproksimacija, geometrijski problemi | 5 (aproks./regular.), 6 (geometrijski) |
| `Vjezbe_5.pdf` | Zad. 1 — optimiranje proizvodnje i tokova u mreži (LP); Zad. 2 — robusna stabilizacija | 5 (zad. 1), 7 (zad. 2) |

> Napomena: tablica se dopunjuje kako se vježbe obrađuju — konačno mapiranje po
> pojedinom zadatku upisano je u checklist niže.

## Checklist napretka

Legenda: ✅ obrađeno i zapisano · 🔄 u tijeku · ⬜ nije počelo

### Predavanja

| Izvor | Str. | Status | Bilješka |
|---|---|---|---|
| `01_Uvod.pdf` | 1–79 | ✅ | cijelo predavanje u `01-uvod.md` |
| `02_Definicije_klasifikacija_konveksnost.pdf` | 1–72 | ⬜ | |
| `03_Uvjeti_optimalnosti.pdf` | 1–68 | ⬜ | |
| `04_Lagrangeova_dualnost.pdf` | 1–34 | ⬜ | |
| `05_LP_QP.pdf` | 1–40 | ⬜ | |
| `06_QCP_SDP.pdf` | 1–31 | ⬜ | |
| `07_Dinamicki_sustavi_Ljapunov_disipativnost.pdf` | 1–55 | ⬜ | |
| `08_Robusno_optimiranje.pdf` | 1–21 | ⬜ | |

### Vježbe

| Izvor | Str. | Status | Bilješka |
|---|---|---|---|
| `Vjezbe_1.pdf` | 1–34 | ⬜ | |
| `Vjezbe_2.pdf` | 1–11 | ⬜ | |
| `Vjezbe_3.pdf` | 1–42 | ⬜ | |
| `Vjezbe_4.pdf` | 1–41 | ⬜ | |
| `Vjezbe_5.pdf` | 1–7 | ⬜ | |

### Detaljna evidencija po poglavlju 1

| Str. izvora | Tema | Gdje je u skripti |
|---|---|---|
| 1–7 | što je optimizacija, povijest, terminologija | 1.1 |
| 8–9 | standardna forma optimizacijskog problema | 1.2 |
| 10–15 | uvodni primjer + graf | 1.3 |
| 16–17 | gdje i zašto se optimira | 1.4 |
| 18–32 | sadržaj kolegija | 1.5 |
| 33–43 | motivacijski primjeri iz prakse | 1.6 |
| 44–45 | proizvodnja i distribucija robe (LP) | 1.7 |
| 46–52 | šest klasičnih ekstremalnih problema | 1.8 |
| 53–56 | vrste optimizacije konstrukcija | 1.9 |
| 57–58 | postavka problema, tri oblika ograde | 1.10 |
| 59–77 | projektiranje kao proces, projektni parametri | 1.11 |
| 78 | dozvoljeni skup | 1.2.5 |
| 79 | korisni „trikovi” | 1.12 |

## Izvan opsega

Ovi materijali **nisu** korišteni kao izvor sadržaja skripte:

- `referenca-rijeseni-seminar-Pongracic.pdf` — tuđe riješeno seminarsko rješenje
- `referenca-zadatak2.m`, `referenca-zadatak2_d.m` — pripadni MATLAB kod
- `data/raw/tekst-seminarskog-zadatka.pdf` — tekst seminarskog zadatka

## Direktoriji

- `figures/` — generirani grafovi (`.png`)
- `scripts/` — Python skripte koje generiraju grafove, plus pomoćne skripte za
  čitanje izvornika:
  - `extract_text.py <pdf> [prva] [zadnja]` — ispisuje tekstualni sloj po stranicama
  - `render_pages.py <pdf> <str> [<str> ...]` — renderira stranice u PNG (potrebno
    jer dio slajdova sadrži rješenja kao slike, koje tekstualni sloj ne vidi)
