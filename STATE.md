# STATE

## Projekt

- **Naziv**: Optimizacijske metode u razvoju i upravljanju sustava — seminarski rad
- **Tip**: Seminar
- **Kolegij**: Optimizacijske metode u razvoju i upravljanju sustava (FSB, ak. god. 2025./26.)
- **Mentor**: Prof. dr. sc. Andrej Jokić
- **Student**: Ivan Noršić
- **LaTeX format**: FSB Seminar
- **Zadatak zadan**: siječanj 2026. · **Rok predaje**: lipanj 2027.

## Trenutni fokus

- Repozitorij postavljen; materijali kolegija i tekst zadatka smješteni u `data/`.
- Sljedeći korak: `latex_architect` postavlja `docs/` (reci "počni pisati").

## Zadatak (4 cjeline)

Izvorni tekst: `data/raw/tekst-seminarskog-zadatka.pdf` (read-only).

1. **QP, konveksnost, KKT, dualnost** — konveksnost problema, KKT uvjeti, grafički
   prikaz dozvoljenog skupa i gradijenata, rješenje u MATLAB-u (`quadprog`/YALMIP),
   Lagrangeov dualni problem, osjetljivost `p*` na perturbacije `b1`, `b2`.
2. **Robustan QP** — koeficijenti `a_ij` nesigurni u intervalu ±15 %; riješiti robusnu
   formulaciju i skicirati dozvoljene skupove za slučajne realizacije koeficijenata.
3. **Formulacija opt. problema — optimalna aproksimacija s ograničenjima** — visina
   ceste `y(x)` na neravnom terenu `h(x)`, diskretizacija s `N+1` točaka, ograničenja
   na nagib (`b1`) i promjenu nagiba (`b2`), rubni uvjeti. Slučajevi A/B × N = 20/100.
4. **Robusna stabilizacija** — prekidački (switching) sustav s dva moda
   `A_parno` / `A_neparno`; provjera Hurwitzovosti, simulacija, dizajn statičkog
   regulatora `u = Kx` uz eksponencijalnu stabilnost zatvorenog kruga.

## Bilješke

- Materijali kolegija (predavanja 01–08, vježbe 1–5) su u `data/sources/` i indeksirani
  za RAG — koristi `rag query` umjesto memorije za definicije i teoreme.
- Numerički dio zadataka radi se u MATLAB-u; kod ide u `src/`, listinzi u `docs/code/`.

---

## Obavezno prije pozivanja agenta

`.ai/config/project.yaml` je popunjen — sva 4 obavezna polja (`author_name`,
`course_name`, `seminar_title`, `professor_name`) su postavljena.
