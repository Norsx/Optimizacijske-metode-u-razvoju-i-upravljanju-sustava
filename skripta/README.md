# Skripta — Optimizacijske metode u razvoju i upravljanju sustava

Samostalna skripta za učenje gradiva od nule, sastavljena **isključivo** iz
predavanja i vježbi u `data/sources/`. Svaka formula, izvod i postupak rješavanja
preuzeti su iz izvornika; ništa nije nadopunjeno iz drugih izvora.

**Format: A4, za ispis.** Izvor je LaTeX, izlaz je `skripta/skripta.pdf` — tekst
teče preko cijele stranice (nisu slajdovi rastegnuti na A4).

## Kako izgraditi PDF

```powershell
.\skripta\build.ps1          # generira grafove pa prevodi skriptu
.\skripta\build.ps1 -Open    # + otvori PDF
```

Skripta se prevodi **Tectonicom**. Ako ga nemaš:

```powershell
$dest = "$env:LOCALAPPDATA\Programs\tectonic"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$url = "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.17.0/tectonic-0.17.0-x86_64-pc-windows-msvc.zip"
Invoke-WebRequest -Uri $url -OutFile "$env:TEMP\tectonic.zip" -UseBasicParsing
Expand-Archive "$env:TEMP\tectonic.zip" -DestinationPath $dest -Force
```

`build.ps1` sam pronalazi tectonic na PATH-u ili na toj lokaciji. Prvi prijevod
skida LaTeX pakete s interneta; kasniji su offline i brzi.

## Struktura

```
skripta/
├── skripta.tex        # glavni A4 dokument (naslovnica, sadržaj, \include poglavlja)
├── preambula.tex      # postavke stranice, okviri (Definicija/Teorem/Zadatak/…), kratice
├── poglavlja/         # jedno poglavlje po predavanju
├── figures/           # generirani grafovi (.png)
├── scripts/           # Python skripte: fig_*.py generiraju grafove
├── build.ps1          # generiranje grafova + prijevod u PDF
└── skripta.pdf        # rezultat
```

Pomoćne skripte za čitanje izvornika (u `scripts/`):

- `extract_text.py <pdf> [prva] [zadnja]` — ispisuje tekstualni sloj po stranicama
- `render_pages.py <pdf> <str> [<str> …]` — renderira stranice u PNG (potrebno jer
  dio slajdova sadrži rješenja kao slike, koje tekstualni sloj ne vidi)

## Redoslijed poglavlja

| # | Datoteka | Izvor |
|---|---|---|
| 1 | `poglavlja/01-uvod.tex` | `01_Uvod.pdf` |
| 2 | `poglavlja/02-definicije-klasifikacija-konveksnost.tex` | `02_Definicije…pdf` + `Vjezbe_1.pdf` + `Vjezbe_2.pdf` |
| 3 | `poglavlja/03-uvjeti-optimalnosti.tex` | `03_Uvjeti_optimalnosti.pdf` |
| 4 | `poglavlja/04-lagrangeova-dualnost.tex` | `04_Lagrangeova_dualnost.pdf` + `Vjezbe_3.pdf` |
| 5 | `poglavlja/05-lp-qp.tex` | `05_LP_QP.pdf` + `Vjezbe_4.pdf` + `Vjezbe_5.pdf` (zad. 1) |
| 6 | `poglavlja/06-qcp-sdp.tex` | `06_QCP_SDP.pdf` + `Vjezbe_4.pdf` (geometrijski problemi) |
| 7 | `poglavlja/07-dinamicki-sustavi-ljapunov-disipativnost.tex` | `07_Dinamicki…pdf` + `Vjezbe_5.pdf` (zad. 2) |
| 8 | `poglavlja/08-robusno-optimiranje.tex` | `08_Robusno_optimiranje.pdf` |

## Mapiranje vježbi na poglavlja

Mapiranje je utvrđeno **čitanjem stvarnog sadržaja** svake vježbe, a ne prema
rednom broju. Zadaci su ugrađeni **inline**, odmah iza teorije koju koriste;
zadaci koji dodiruju više tema razlomljeni su po podzadacima.

| Vježba | Stvaran sadržaj | Ide u poglavlje |
|---|---|---|
| `Vjezbe_1.pdf` | vektori/matrice, funkcije, linearne i afine funkcije, nivo krivulje, skalarni produkt, hiperravnine i poluprostori, poliedar/politop, vektorske norme; zadaci 1–4 | 2 |
| `Vjezbe_2.pdf` | konveksan opt. problem (Primjer 1), norme kao konveksne funkcije, minimizacija norme i reformulacije | 2 |
| `Vjezbe_3.pdf` | Primjer 1 — tržište i formiranje cijena; Primjer 2 — dualnost, KKT, osjetljivost | 4 |
| `Vjezbe_4.pdf` | aproksimacije, regularizirana aproksimacija, geometrijski problemi | 5 (aproks./regular.), 6 (geometrijski) |
| `Vjezbe_5.pdf` | Zad. 1 — optimiranje proizvodnje i tokova u mreži (LP); Zad. 2 — robusna stabilizacija | 5 (zad. 1), 7 (zad. 2) |

> Tablica se dopunjuje kako se vježbe obrađuju — konačno mapiranje po pojedinom
> zadatku vodi se u checklistu niže.

## Checklist napretka

Legenda: ✅ obrađeno i zapisano · 🔄 u tijeku · ⬜ nije počelo

### Predavanja

| Izvor | Str. | Status | Bilješka |
|---|---|---|---|
| `01_Uvod.pdf` | 1–79 | ✅ | cijelo predavanje, poglavlje 1 |
| `02_Definicije_klasifikacija_konveksnost.pdf` | 1–72 | ✅ | cijelo predavanje, poglavlje 2 |
| `03_Uvjeti_optimalnosti.pdf` | 1–68 | ⬜ | |
| `04_Lagrangeova_dualnost.pdf` | 1–34 | ⬜ | |
| `05_LP_QP.pdf` | 1–40 | ⬜ | |
| `06_QCP_SDP.pdf` | 1–31 | ⬜ | |
| `07_Dinamicki_sustavi_Ljapunov_disipativnost.pdf` | 1–55 | ⬜ | |
| `08_Robusno_optimiranje.pdf` | 1–21 | ⬜ | |

### Vježbe

| Izvor | Str. | Status | Bilješka |
|---|---|---|---|
| `Vjezbe_1.pdf` | 1–34 | ✅ | ugrađeno inline u poglavlje 2 (zadaci 1–4) |
| `Vjezbe_2.pdf` | 1–11 | ✅ | ugrađeno inline u poglavlje 2 (Primjer 1 + norme) |
| `Vjezbe_3.pdf` | 1–42 | ⬜ | |
| `Vjezbe_4.pdf` | 1–41 | ⬜ | |
| `Vjezbe_5.pdf` | 1–7 | ⬜ | |

### Detaljna evidencija — poglavlje 1

| Str. izvora | Tema | Odjeljak skripte |
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

### Detaljna evidencija — poglavlje 2

Predavanje 02:

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 3–5 | podsjetnik: standardna forma, trikovi | 2.1 |
| 6–11 | klasifikacije opt. problema; stara i moderna podjela | 2.5 |
| 12–21 | primjeri I–IV (diskretan, kontinuiran, cjelobrojni, MILP) | 2.6 |
| 22–27 | lokalni/globalni minimizator, infimum i supremum | 2.7 |
| 29–32 | Jakobijan, linearizacija, primjer | 2.8 |
| 33–40 | gradijent, smjer pada, okomitost na nivo krivulju | 2.9 |
| 41–42 | Hessian, Taylorovi teoremi | 2.10 |
| 43–45 | uvjeti optimalnosti bez ograničenja | 2.11 |
| 46–50 | definitnost matrica, primjeri, kriterij determinanti | 2.12 |
| 51–60 | afin skup, konveksan skup, konveksna ljuska | 2.13 |
| 61–64 | konveksne i konkavne funkcije | 2.16 |
| 65–66 | hiperravnine i poluprostori | 2.14 |
| 67–70 | svojstva konv. funkcija, kvazikonveksnost, uvjeti 1./2. reda | 2.18 |
| 71–72 | konveksan optimizacijski problem | 2.19 |

Vježbe 1:

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 2–3 | vektori, matrice, transponiranje | 2.2.1 |
| 4–6 | funkcije (skalarne i vektorske) | 2.2.2 |
| 7–9 | linearnost, prepoznavanje linearnih funkcija | 2.2.3 |
| 10–17 | matrični zapis $Ax$ / $a^\top x$ | 2.2.4 |
| 18–19 | afine funkcije, slika linearno vs. afino | 2.2.5 |
| 20 | **Zadatak 1** — superpozicija (progib) | 2.2.5 |
| 21 | nivo krivulje | 2.3 |
| 22, 27 | **Zadatak 2** — nivo krivulje linearne funkcije | 2.3 |
| 23–25 | skalarni produkt, okomitost, predznak | 2.4 |
| 26, 28 | hiperravnine i poluprostori | 2.14 |
| 29 | **Zadatak 3** — poluprostor | 2.14 |
| 30 | poliedar i politop | 2.15 |
| 31 | **Zadatak 4** — politop | 2.15 |
| 32–34 | vektorske norme, jedinične kugle | 2.17 |

Vježbe 2:

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 2–3 | konveksan optimizacijski problem | 2.19 |
| 4–5 | **Primjer 1** — prepoznavanje konveksnih problema | 2.19 |
| 6–8 | norme kao konveksne funkcije (plohe i nivo krivulje) | 2.20.1 |
| 9–11 | reformulacije minimizacije norme (1-, 2-, ∞-norma) | 2.20.2 |

> Zadaci 1–4 iz Vježbi 1 u izvorniku nemaju zapisano rješenje („na ploči”);
> u skripti su riješeni isključivo pomoću definicija s istih vježbi, uz
> izričitu oznaku. Zadaci 3 i 4 u izvorniku nemaju ni sliku na koju se
> pozivaju, pa je uzet konkretan primjer istog tipa.

## Izvan opsega

Ovi materijali **nisu** korišteni kao izvor sadržaja skripte:

- `referenca-rijeseni-seminar-Pongracic.pdf` — tuđe riješeno seminarsko rješenje
- `referenca-zadatak2.m`, `referenca-zadatak2_d.m` — pripadni MATLAB kod
- `data/raw/tekst-seminarskog-zadatka.pdf` — tekst seminarskog zadatka
