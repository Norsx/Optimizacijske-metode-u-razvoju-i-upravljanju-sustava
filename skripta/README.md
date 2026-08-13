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
| `03_Uvjeti_optimalnosti.pdf` | 1–68 | ✅ | cijelo predavanje, poglavlje 3 |
| `04_Lagrangeova_dualnost.pdf` | 1–34 | ✅ | cijelo predavanje, poglavlje 4 |
| `05_LP_QP.pdf` | 1–40 | ✅ | cijelo predavanje, poglavlje 5 |
| `06_QCP_SDP.pdf` | 1–31 | ✅ | cijelo predavanje, poglavlje 6 |
| `07_Dinamicki_sustavi_Ljapunov_disipativnost.pdf` | 1–55 | ✅ | cijelo predavanje, poglavlje 7 |
| `08_Robusno_optimiranje.pdf` | 1–21 | ⬜ | |

### Vježbe

| Izvor | Str. | Status | Bilješka |
|---|---|---|---|
| `Vjezbe_1.pdf` | 1–34 | ✅ | ugrađeno inline u poglavlje 2 (zadaci 1–4) |
| `Vjezbe_2.pdf` | 1–11 | ✅ | ugrađeno inline u poglavlje 2 (Primjer 1 + norme) |
| `Vjezbe_3.pdf` | 1–42 | ✅ | ugrađeno inline u poglavlje 4 (Primjer 1 + Primjer 2 a–f) |
| `Vjezbe_4.pdf` | 1–41 | ✅ | str. 1–30 u poglavlju 5; str. 31–41 (geometrijski) u poglavlju 6 |
| `Vjezbe_5.pdf` | 1–7 | ✅ | Zad. 1 (str. 2–4) u poglavlju 5; Zad. 2 (str. 5–7) u poglavlju 7 |

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

### Detaljna evidencija — poglavlje 3

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 2 | postavka problema s ograničenjima | 3.1 |
| 3–8 | dozvoljeni smjerovi, smjerovi pada, nužni uvjeti 1. reda | 3.2 |
| 9–18 | primjer: sedlasta funkcija na disku (dva kandidata) | 3.3 |
| 19–32 | jedno ograničenje jednakosti, kolinearnost gradijenata | 3.4 |
| 33–34 | Lagrangeova funkcija | 3.5 |
| 35–39 | više ograničenja jednakosti, regularna točka, recept | 3.6 |
| 40 | primjer: paralelepiped upisan u kuglu | 3.6.4 |
| 41–51 | jedno ograničenje nejednakosti, aktivnost, komplementarnost | 3.7 |
| 52–57 | više ograničenja nejednakosti, geometrija, neregularna točka | 3.8 |
| 58–61 | **KKT uvjeti — opći slučaj** | 3.9 |
| 62–63 | fizikalna interpretacija množitelja (reakcija veze) | 3.10 |
| 64–68 | ravnotežni položaj: pet primjera (samo slike u izvorniku) | 3.11 |

> Slajdovi 64–68 u izvorniku nemaju ispisane formule (računi su rađeni na
> ploči), pa su u skripti opisani točno onako kako izgledaju, uz naznaku kojim
> se aparatom iz poglavlja rješavaju.

### Detaljna evidencija — poglavlje 4

Predavanje 04:

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 4–9 | donje granice, dualna funkcija, lanac nejednakosti | 4.1 |
| 10 | terminologija dualnosti | 4.2 |
| 11 | slaba dualnost, konkavnost duala | 4.3 |
| 12–13 | Primjer 1: dual LP-a u standardnoj formi | 4.4 |
| 14–15 | Primjer 2: optimalno particioniranje (SDP relaksacija) | 4.5 |
| 16–18 | jaka dualnost, Slaterovi uvjeti, LP s jakom dualnošću | 4.6 |
| 19–23 | KKT iz dualnosti; dovoljnost za konveksne probleme | 4.7 |
| 24–27 | dualna dekompozicija | 4.9 |
| 28–34 | analiza osjetljivosti (globalna i lokalna) | 4.11 |

Vježbe 3:

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 4–14 | **Primjer 1** — tržište i formiranje cijena | 4.10 |
| 15–18 | krivulje ponude/potražnje, APX podaci | 4.10.6 |
| 20 | **Primjer 2** — postavka i podzadaci a)–f) | 4.7.4 |
| 21–22 | a) konveksnost problema | 4.7.4 |
| 23–27 | b) rješavanje KKT uvjeta (tablica 16 slučajeva) | 4.7.4 |
| 28–33 | c) MATLAB: `quadprog` i YALMIP | 4.8.1 |
| 34–39 | d) postavljanje i rješavanje dualnog problema | 4.8.2 |
| 40–41 | e) osjetljivost | 4.11.4 |
| 42 | f) ponovljeno s promijenjenim ograničenjima | 4.11.4 |

### Detaljna evidencija — poglavlje 5

Predavanje 05:

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 4–5 | LP problem, eliminacija jednakosti | 5.1 |
| 6–7 | primjer proizvodnje i distribucije | 5.1.2 |
| 8–9 | geometrija LP-a | 5.2 |
| 10–13 | standardni oblik i transformacija | 5.3 |
| 14–19 | ekstremne točke, bazna dozvoljena rješenja | 5.4 |
| 20 | simpleks algoritam | 5.4.5 |
| 21 | primjer ekstremnih točaka (samo slika u izvorniku) | 5.4.6 |
| 22–27 | Primjer 1: po dijelovima afine funkcije kao LP | 5.5.1 |
| 28–29 | Primjer 2: Chebyshevljev centar poliedra | 5.5.2 |
| 31–32 | kvadratne funkcije, simetrija matrice Q | 5.6.1 |
| 33–34 | QP problem i njegova geometrija | 5.6.2 |
| 35–36 | Primjer 1: najmanji kvadrati | 5.7.1 |
| 37–38 | Primjer 2: udaljenost između poliedara | 5.7.2 |
| 39–40 | Primjer 3: LP sa slučajnim c (rizik) | 5.7.3 |

Vježbe 4 (str. 1–30):

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 4–5 | aproksimacija u zadanoj normi, tri formulacije | 5.8 |
| 6–13 | **Primjer 1** — aproksimacija baznim funkcijama + MATLAB | 5.9 |
| 14 | aproksimacije s ograničenjima | 5.9.5 |
| 15–17 | **Primjer 2** — sinteza filtra | 5.10 |
| 19–20 | regularizirana aproksimacija, Pareto fronta | 5.11 |
| 21–25 | **Primjer 3** — optimiranje trajektorije ulaza | 5.12 |
| 26–30 | **Primjer 4** — rekonstrukcija signala | 5.13 |

Vježbe 5 (Zadatak 1):

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 2–4 | **Zadatak 1** — proizvodnja i tokovi u mreži | 5.14 |

> `Vjezbe_5.pdf` sadrži samo tekst Zadatka 1, bez rješenja. U skripti je riješen
> kao QP aparatom poglavlja 5, a odgovor na pitanje o investiciji očitan je iz
> dualnih varijabli (poglavlje 4). Brojevi su dobiveni skriptom
> `scripts/solve_vj5_mreza.py`, koja je dio repozitorija.

### Detaljna evidencija — poglavlje 6

Predavanje 06:

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 4–5 | podsjetnik: definitnost matrica | 6.1 |
| 6–9 | konveksni konusi, pravilan konus, generalizirane nejednakosti | 6.2 |
| 11–13 | CQP, konus drugog stupnja, QCQP | 6.3 |
| 14–15 | robusni LP s elipsoidnom nesigurnošću kao CQP | 6.3.3 |
| 17–22 | linearne matrične nejednakosti (LMI) | 6.4 |
| 23–25 | SDP, blok-dijagonalno slaganje LMN-ova | 6.5 |
| 26 | transformacija kongruencije | 6.6 |
| 27–28 | Schurov komplement | 6.7 |
| 29 | minimizacija norme matrice kao SDP | 6.8 |
| 30–31 | LP i CQP kao podskupovi SDP-a | 6.9 |

Vježbe 4 (str. 31–41):

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 32 | linearna klasifikacija kao LP | 6.10.1 |
| 33–38 | robusna klasifikacija: margina izvedena dualnošću | 6.10.2–6.10.3 |
| 39 | konačna QP formulacija (maksimizacija margine) | 6.10.4 |
| 40–41 | aproksimativna klasifikacija (support vector classifier) | 6.10.5 |

### Detaljna evidencija — poglavlje 7

Predavanje 07:

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 4 | eksponencijalna stabilnost, prostor stanja | 7.1 |
| 5–6 | Ljapunovljev LMI uvjet za LTI sustave | 7.2 |
| 7–10 | dokaz 1 („putem trajektorija”) | 7.2.1 |
| 11–13 | invarijantnost nivo skupova + brojčani primjer | 7.2.2 |
| 14–22 | dokaz 2 (algebarski, oba smjera, Jordanova forma) | 7.2.3 |
| 23 | diskretno vrijeme | 7.2.4 |
| 25–26 | kvadratna stabilnost, redukcija na vrhove politopa | 7.3 |
| 28–33 | sinteza regulatora: konveksifikacija (Q, Y supstitucija) | 7.4 |
| 36–43 | disipativnost, funkcije dobave i pohrane, fizikalni primjeri | 7.6 |
| 44–51 | LMI karakterizacija disipativnosti (puni izvod) | 7.7 |
| 52–55 | frekvencijska domena, KYP lema, sažeti teoremi | 7.8 |

Vježbe 5 (Zadatak 2):

| Str. izvora | Tema | Odjeljak skripte |
|---|---|---|
| 5–7 | **Zadatak 2** — robusna stabilizacija obrnutog njihala | 7.5 |

> `Vjezbe_5.pdf` daje samo tekst Zadatka 2. U skripti je riješen politopskim
> opisom nesigurnosti (dva vrha) i LMI sintezom iz predavanja 07; brojevi su
> dobiveni skriptom `scripts/solve_vj5_robusna.py`, uz g = 9,81 m/s²
> (slajd ne navodi brojčanu vrijednost).

## Izvan opsega

Ovi materijali **nisu** korišteni kao izvor sadržaja skripte:

- `referenca-rijeseni-seminar-Pongracic.pdf` — tuđe riješeno seminarsko rješenje
- `referenca-zadatak2.m`, `referenca-zadatak2_d.m` — pripadni MATLAB kod
- `data/raw/tekst-seminarskog-zadatka.pdf` — tekst seminarskog zadatka
