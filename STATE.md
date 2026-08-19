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

- **Skripta za učenje (`skripta/`) je gotova i spremna za ispis** — 234 stranice
  A4, sva predavanja (01–08) i sve vježbe (1–5) obrađeni u cijelosti.
  Kontrolna lista provjera: `skripta/README.md` → „Provjera spremnosti za ispis”.
- Repozitorij postavljen; materijali kolegija i tekst zadatka smješteni u `data/`.
- Sljedeći korak: **seminarski rad** — `latex_architect` postavlja `docs/`
  (reci „počni pisati”). Skripta je za učenje i odvojena je od seminara.

## Zadatak (4 cjeline)

Izvorni tekst: `data/raw/tekst-seminarskog-zadatka.pdf` (read-only). Podaci niže su
prepisani s renderiranih stranica izvornika — tekstualni sloj tog PDF-a je neispravan
i izvlači se izobličeno, pa se **ne smije** koristiti za prepisivanje formula.

### Zadatak 1 — QP, konveksnost, KKT, dualnost

$$\min_x\; x_1^2 + 2x_2^2 - 0.3x_1x_2 + 2x_1 - 3x_2$$

uz ograničenja $a_{11}x_1 + a_{12}x_2 \le -10$ i $a_{21}x_1 + a_{22}x_2 \le 3$,
gdje je $a_{11}=-1,\; a_{12}=-1,\; a_{21}=1,\; a_{22}=-1$.

Dakle: $-x_1-x_2 \le -10$ (tj. $x_1+x_2 \ge 10$) i $x_1-x_2 \le 3$.

Podzadaci: a) konveksnost; b) KKT uvjeti i njihovo rješenje; c) crtež dozvoljenog
skupa, nivo krivulja i gradijenata u KKT točki; d) MATLAB (`quadprog` i/ili YALMIP),
usporedba dualnih varijabli s (b); e) Lagrangeov dualni problem numerički, usporedba
s (d) i (b); f) osjetljivost $p^\star$ na perturbacije $b_1$ i $b_2$.

### Zadatak 2 — robustan QP

Koeficijenti $a_{ij}$ nesigurni: stvarna vrijednost leži u $[0.85a_{ij},\,1.15a_{ij}]$
(±15 % od vrijednosti iz Zadatka 1). Riješiti robusni problem; nacrtati dozvoljene
skupove za niz slučajno izabranih koeficijenata i označiti optimum.

### Zadatak 3 — optimalna aproksimacija s ograničenjima

$L = 10$, $h(x) = 0.0053x^4 - 0.095x^3 + 0.48x^2 - 0.3x + 1$,
$a = h(0) = 1$, $b = h(L) = 4$.

- slučaj A: $b_1 = 0.5,\; b_2 = 0.5$
- slučaj B: $b_1 = 0.5,\; b_2 = 0.2$

Diskretizacija: $N+1$ točaka, $\Delta x = L/N$, $x_0=0$, $x_N=L$.
Nagib: $\nabla y_i := \frac{1}{\Delta x}(y_i - y_{i-1})$;
promjena nagiba: $\nabla^2 y_i := \frac{1}{\Delta x}(\nabla y_i - \nabla y_{i-1})$.

Ograničenja: $|\nabla y_i| \le b_1$, $|\nabla^2 y_i| \le b_2$, $y_0 = a$, $y_N = b$.
Riješiti za 4 slučaja: A/N=20, A/N=100, B/N=20, B/N=100.

### Zadatak 4 — robusna stabilizacija

$\dot x(t) = A(t)x(t) + Bu(t)$, gdje je $A(t) = A_{\text{parno}}$ kad je
$\lfloor t \rfloor$ paran, inače $A_{\text{neparno}}$:

$$A_{\text{parno}} = \begin{bmatrix} -1 & -\tfrac{1}{6}\pi \\ \tfrac{3}{2}\pi & -1 \end{bmatrix}, \qquad
A_{\text{neparno}} = \begin{bmatrix} -1 & -\tfrac{3}{2}\pi \\ \tfrac{1}{6}\pi & -1 \end{bmatrix}$$

a) jesu li oba moda Hurwitzova (svojstvene vrijednosti); b) simulacija s $x(0)=[1,0]^T$,
graf $x(t)$ i trajektorija u prostoru stanja, je li sustav stabilan; c) uz
$B = [1, 0]^T$ dizajnirati statički $u = Kx$ tako da je $\dot x = (A(t)+BK)x$
eksponencijalno stabilan, pa simulirati s istim početnim uvjetom.

## Bilješke

- Materijali kolegija (predavanja 01–08, vježbe 1–5) su u `data/sources/` i indeksirani
  za RAG — koristi `rag query` umjesto memorije za definicije i teoreme.
- Numerički dio zadataka radi se u MATLAB-u; kod ide u `src/`, listinzi u `docs/code/`.

---

## Obavezno prije pozivanja agenta

`.ai/config/project.yaml` je popunjen — sva 4 obavezna polja (`author_name`,
`course_name`, `seminar_title`, `professor_name`) su postavljena.
