%% Zadatak 2 - Robustan QP (intervalna nesigurnost koeficijenata +-15 %)
%
% Isti QP kao u Zadatku 1, ali koeficijenti a_ij nisu tocno poznati:
% stvarna vrijednost lezi u intervalu [0.85*a_ij, 1.15*a_ij].
%
% Robusna protuformulacija: ogranicenje mora vrijediti za SVE realizacije,
% dakle za najgori slucaj. Kako a_ij ulaze linearno i nezavisno, za
% a in [a_lo, a_hi] vrijedi
%       max_a  a*x = abar*x + r*|x|,   abar = (a_lo+a_hi)/2,  r = (a_hi-a_lo)/2,
% pa ogranicenje postaje  abar'*x + r'*|x| <= b.  Clan r'*|x| je konveksan i
% stoji na lijevoj strani nejednakosti, pa je robusni problem i dalje konveksan.
% Uvodenjem u_i >= |x_i| dobiva se obican QP s linearnim ogranicenjima.
%
% Pokretanje:  matlab -batch "run('src/zadatak2.m')"

clear; clc; close all;
rng(0);

projRoot = fileparts(fileparts(mfilename('fullpath')));
figDir = fullfile(projRoot, 'docs', 'figures');
if ~exist(figDir, 'dir'); mkdir(figDir); end

H = [2.0, -0.3; -0.3, 4.0];
c = [2.0; -3.0];
Anom = [-1, -1; 1, -1];
bvec = [-10; 3];

f = @(x) 0.5*x'*H*x + c'*x;

%% Intervali koeficijenata
Alo = min(0.85*Anom, 1.15*Anom);   % element-wise donja granica
Ahi = max(0.85*Anom, 1.15*Anom);   % element-wise gornja granica
Abar = (Alo + Ahi)/2;              % sredina = nominalna vrijednost
R    = (Ahi - Alo)/2;              % polumjer = 0.15*|a_ij|

fprintf('=== Intervali koeficijenata ===\n');
for i = 1:2
    for j = 1:2
        fprintf('a%d%d in [%+.4f, %+.4f]  (sredina %+.2f, polumjer %.2f)\n', ...
            i, j, Alo(i,j), Ahi(i,j), Abar(i,j), R(i,j));
    end
end
fprintf('\n');

%% Nominalno rjesenje (Zadatak 1)
opts = optimoptions('quadprog', 'Display', 'off');
x_nom = quadprog(H, c, Anom, bvec, [], [], [], [], [], opts);
fprintf('=== Nominalno rjesenje ===\n');
fprintf('x_nom = [%.6f; %.6f],  f = %.6f\n\n', x_nom(1), x_nom(2), f(x_nom));

%% Robusno rjesenje: varijable z = [x1; x2; u1; u2],  u >= |x|
Hz = blkdiag(H, zeros(2));
cz = [c; 0; 0];
% Abar*x + R*u <= b
Az = [Abar, R;
      % u >= x   ->   x - u <= 0
       1, 0, -1,  0;
       0, 1,  0, -1;
      % u >= -x  ->  -x - u <= 0
      -1, 0, -1,  0;
       0,-1,  0, -1];
bz = [bvec; 0; 0; 0; 0];

[z, ~, flag, ~, lam] = quadprog(Hz, cz, Az, bz, [], [], [], [], [], opts);
x_rob = z(1:2);
fprintf('=== Robusno rjesenje ===\n');
fprintf('exitflag = %d\n', flag);
fprintf('x_rob = [%.6f; %.6f]\n', x_rob(1), x_rob(2));
fprintf('f(x_rob) = %.6f   (nominalno %.6f, cijena robusnosti %.6f)\n', ...
    f(x_rob), f(x_nom), f(x_rob) - f(x_nom));
fprintf('multiplikatori robusnih ogranicenja: [%.6f, %.6f]\n', lam.ineqlin(1), lam.ineqlin(2));

% Buduci da je x_rob > 0, |x| = x, pa se robusna ogranicenja svode na
%   -0.85*(x1+x2) <= -10   i   1.15*x1 - 0.85*x2 <= 3
fprintf('\nprovjera (x > 0 pa je |x| = x):\n');
fprintf('  -0.85*(x1+x2) = %+.6f  <= -10 ? %d\n', -0.85*sum(x_rob), -0.85*sum(x_rob) <= -10 + 1e-9);
fprintf('   1.15*x1 - 0.85*x2 = %+.6f  <= 3 ? %d\n', 1.15*x_rob(1) - 0.85*x_rob(2), ...
        1.15*x_rob(1) - 0.85*x_rob(2) <= 3 + 1e-9);
fprintf('  oba ogranicenja aktivna -> x_rob = (13/2, 179/34)\n\n');

%% Provjera robusnosti nad slucajnim realizacijama
M = 20000;
viol_nom = 0; viol_rob = 0;
for k = 1:M
    Ak = Alo + (Ahi - Alo).*rand(2,2);
    if any(Ak*x_nom > bvec + 1e-12); viol_nom = viol_nom + 1; end
    if any(Ak*x_rob > bvec + 1e-12); viol_rob = viol_rob + 1; end
end
fprintf('=== Provjera na %d slucajnih realizacija ===\n', M);
fprintf('nominalno rjesenje krsi ogranicenja: %d / %d  (%.1f %%)\n', viol_nom, M, 100*viol_nom/M);
fprintf('robusno rjesenje krsi ogranicenja:   %d / %d  (%.1f %%)\n\n', viol_rob, M, 100*viol_rob/M);

%% Slika: dozvoljeni skupovi za slucajne koeficijente + optimumi
fig = figure('Color', 'w', 'Position', [100 100 780 660]);
hold on; box on;
xs = linspace(0, 14, 300);

% Dozvoljeni skupovi za niz slucajnih realizacija. Umjesto samih granicnih
% pravaca crta se koliki UDIO realizacija proglasava svaku tocku dopustivom:
% tamnije podrucje = dopustivo za vise realizacija, a podrucje s udjelom 1
% je presjek svih skupova, tj. robusni dozvoljeni skup.
ng = 420;
gv = linspace(0, 14, ng);
[G1, G2] = meshgrid(gv, gv);
acc = zeros(ng);
Msets = 300;
for k = 1:Msets
    Ak = Alo + (Ahi - Alo).*rand(2,2);
    feas = (Ak(1,1)*G1 + Ak(1,2)*G2 <= bvec(1)) & ...
           (Ak(2,1)*G1 + Ak(2,2)*G2 <= bvec(2));
    acc = acc + feas;
end
frac = acc / Msets;
hImg = imagesc(gv, gv, frac);
set(gca, 'YDir', 'normal');
colormap(flipud(gray(256).^0.6));
cb = colorbar; cb.Label.String = 'udio realizacija za koje je tocka dopustiva';
caxis([0 1]);

% obris robusnog skupa (udio = 1)
contour(G1, G2, frac, [0.999 0.999], 'LineColor', [0 0.5 0], 'LineWidth', 1.6);

% nekoliko pojedinacnih granica radi citljivosti
hSample = gobjects(1);
for k = 1:25
    Ak = Alo + (Ahi - Alo).*rand(2,2);
    y1 = (bvec(1) - Ak(1,1)*xs) / Ak(1,2);
    y2 = (bvec(2) - Ak(2,1)*xs) / Ak(2,2);
    hS1 = plot(xs, y1, '-', 'Color', [0.35 0.55 0.85 0.35], 'LineWidth', 0.5);
    plot(xs, y2, '-', 'Color', [0.90 0.60 0.25 0.35], 'LineWidth', 0.5);
    if k == 1; hSample = hS1; end
end

% nominalne granice
hNom = plot(xs, 10 - xs, 'b-', 'LineWidth', 2);
plot(xs, xs - 3, 'b--', 'LineWidth', 2);

% robusne (najgori slucaj) granice, za x > 0
hRob = plot(xs, 10/0.85 - xs, 'k-', 'LineWidth', 2);
plot(xs, (1.15*xs - 3)/0.85, 'k--', 'LineWidth', 2);

hN = plot(x_nom(1), x_nom(2), 'o', 'MarkerFaceColor', [0.2 0.4 0.9], ...
     'MarkerEdgeColor', 'k', 'MarkerSize', 10);
hR = plot(x_rob(1), x_rob(2), 'p', 'MarkerFaceColor', 'r', ...
     'MarkerEdgeColor', 'k', 'MarkerSize', 15);

xlabel('x_1'); ylabel('x_2');
title('Zadatak 2: dozvoljeni skupovi za slucajne koeficijente (\pm15 %)');
legend([hSample hNom hRob hN hR], ...
    {'slucajne realizacije', 'nominalne granice', 'robusne (najgori slucaj)', ...
     'x_{nom}', 'x_{rob}'}, 'Location', 'northeast');
axis([0 14 0 14]); axis square; grid on;

exportgraphics(fig, fullfile(figDir, 'zad2_robustni.pdf'), 'ContentType', 'vector');
fprintf('Slika spremljena: %s\n', fullfile(figDir, 'zad2_robustni.pdf'));
