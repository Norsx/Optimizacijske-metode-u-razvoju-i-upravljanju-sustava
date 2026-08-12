%% Zadatak 1 - QP, konveksnost, KKT uvjeti i Lagrangeova dualnost
%
% min  x1^2 + 2*x2^2 - 0.3*x1*x2 + 2*x1 - 3*x2
%  x
% uz   a11*x1 + a12*x2 <= -10
%      a21*x1 + a22*x2 <=   3
%      a11 = -1, a12 = -1, a21 = 1, a22 = -1
%
% Pokretanje:  matlab -batch "run('src/zadatak1.m')"

clear; clc; close all;

% Putanje se razrjesavaju relativno na ovu skriptu: MATLAB-ov `run` mijenja
% radni direktorij u mapu skripte, pa relativni 'docs/figures' promasi cilj.
projRoot = fileparts(fileparts(mfilename('fullpath')));
figDir = fullfile(projRoot, 'docs', 'figures');
if ~exist(figDir, 'dir'); mkdir(figDir); end

%% Podaci u standardnom QP obliku:  f(x) = 1/2*x'*H*x + c'*x,  A*x <= b
H = [ 2.0, -0.3;
     -0.3,  4.0];
c = [ 2.0; -3.0];

a11 = -1; a12 = -1; a21 = 1; a22 = -1;
A = [a11, a12;
     a21, a22];
b = [-10; 3];

f = @(x) 0.5*x'*H*x + c'*x;

%% a) Konveksnost
lam_H = eig(H);
fprintf('=== a) Konveksnost ===\n');
fprintf('Svojstvene vrijednosti H: %.6f, %.6f\n', lam_H(1), lam_H(2));
fprintf('H pozitivno definitna: %d  -> strogo konveksan QP\n', all(lam_H > 0));
fprintf('Ogranicenja su linearna -> dozvoljeni skup je konveksan poliedar.\n\n');

%% b) KKT uvjeti - sustavno nabrajanje slucajeva aktivnih ogranicenja
% Postupak iz vjezbi 3 (Primjer 2): zbog komplementarnosti svako ogranicenje je
% ili aktivno (g_i = 0, lambda_i >= 0) ili neaktivno (g_i < 0, lambda_i = 0),
% pa se prolazi kroz svih 2^m kombinacija i trazi ona koja zadovolji SVE
% KKT uvjete. Uz m = 2 ogranicenja to su 4 slucaja.
fprintf('=== b) KKT - nabrajanje slucajeva ===\n');
fprintf('%-28s %-22s %-20s %s\n', 'aktivni skup', 'x', 'lambda', 'status');

combos = {[], 1, 2, [1 2]};
x_kkt = []; lam_kkt = [];
for k = 1:numel(combos)
    S = combos{k};
    nS = numel(S);
    % Rjesava se [H A_S'; A_S 0][x; lambda_S] = [-c; b_S]
    KKTmat = [H, A(S,:)'; A(S,:), zeros(nS)];
    rhs = [-c; b(S)];
    sol = KKTmat \ rhs;
    xk = sol(1:2);
    lamS = sol(3:end);
    lam = zeros(2,1); lam(S) = lamS;

    primal = all(A*xk - b <= 1e-9);      % dopustivost
    dualok = all(lam >= -1e-9);          % lambda >= 0
    ok = primal && dualok;

    if isempty(S)
        nameS = '{} (nijedno aktivno)';
    else
        nameS = ['{' strjoin(arrayfun(@(i) sprintf('g%d', i), S, 'UniformOutput', false), ', ') '}'];
    end
    if ~primal
        st = 'ODBACEN: nedopustiv';
    elseif ~dualok
        st = 'ODBACEN: lambda < 0';
    else
        st = 'ZADOVOLJAVA SVE KKT UVJETE';
        x_kkt = xk; lam_kkt = lam;
    end
    fprintf('%-28s [%7.4f %7.4f]  [%7.4f %7.4f]  %s\n', nameS, xk(1), xk(2), lam(1), lam(2), st);
end
lambda1 = lam_kkt(1);
fprintf('\n');

fprintf('=== b) Rjesenje ===\n');
fprintf('x*      = [%.6f; %.6f]   (tocno: [190/33; 140/33])\n', x_kkt(1), x_kkt(2));
fprintf('lambda1 = %.6f   (tocno: 404/33)\n', lambda1);
fprintf('lambda2 = 0 (g2 neaktivno)\n');
fprintf('provjera g2 = %.6f  (< 0 => neaktivno, u skladu s lambda2 = 0)\n', A(2,:)*x_kkt - b(2));
fprintf('dualna dopustivost: lambda1 = %.6f >= 0\n', lambda1);
fprintf('rezidual stacionarnosti: %.3e\n', norm(H*x_kkt + c + lambda1*A(1,:)'));
fprintf('p* = %.6f   (tocno: 2000/33)\n\n', f(x_kkt));

%% d) Rjesenje u MATLAB-u: quadprog
opts = optimoptions('quadprog', 'Display', 'off', 'Algorithm', 'interior-point-convex');
[x_qp, fval_qp, exitflag, ~, lambda_qp] = quadprog(H, c, A, b, [], [], [], [], [], opts);

fprintf('=== d) quadprog ===\n');
fprintf('exitflag = %d\n', exitflag);
fprintf('x*      = [%.6f; %.6f]\n', x_qp(1), x_qp(2));
fprintf('p*      = %.6f\n', fval_qp);
fprintf('lambda  = [%.6f; %.6f]\n', lambda_qp.ineqlin(1), lambda_qp.ineqlin(2));
fprintf('max |x_quadprog - x_KKT| = %.3e\n\n', max(abs(x_qp - x_kkt)));

%% d') Isto preko YALMIP-a (ako je dostupan)
if exist('sdpvar', 'file') == 2
    x = sdpvar(2, 1);
    con = [A*x <= b];
    obj = 0.5*x'*H*x + c'*x;
    diagn = optimize(con, obj, sdpsettings('verbose', 0));
    x_yal = value(x);
    lam_yal = dual(con);
    fprintf('=== d) YALMIP ===\n');
    fprintf('status  = %s\n', yalmiperror(diagn.problem));
    fprintf('x*      = [%.6f; %.6f]\n', x_yal(1), x_yal(2));
    fprintf('lambda  = [%.6f; %.6f]\n', lam_yal(1), lam_yal(2));
    fprintf('max |x_yalmip - x_KKT| = %.3e\n\n', max(abs(x_yal - x_kkt)));
else
    fprintf('=== d) YALMIP nije dostupan - preskoceno ===\n\n');
end

%% e) Lagrangeov dualni problem
% g(lambda) = min_x L(x,lambda) = -1/2*(c + A'*lambda)'*inv(H)*(c + A'*lambda) - lambda'*b
Hinv = inv(H);
gdual = @(lam) -0.5*(c + A'*lam)' * Hinv * (c + A'*lam) - lam'*b;

% max g(lambda) uz lambda >= 0  <=>  min -g(lambda) uz lambda >= 0
negg = @(lam) -gdual(lam);
opts_fmin = optimoptions('fmincon', 'Display', 'off', ...
    'OptimalityTolerance', 1e-12, 'StepTolerance', 1e-14);
lam_star = fmincon(negg, [0; 0], [], [], [], [], [0; 0], [], [], opts_fmin);
d_star = gdual(lam_star);

fprintf('=== e) Dualni problem ===\n');
fprintf('lambda* = [%.6f; %.6f]\n', lam_star(1), lam_star(2));
fprintf('d*      = %.6f\n', d_star);
fprintf('p*      = %.6f\n', f(x_kkt));
fprintf('dualni jaz p* - d* = %.3e  -> jaka dualnost\n\n', f(x_kkt) - d_star);

%% f) Osjetljivost p* na perturbacije b1 i b2
% Teorija: dp*/db_i = -lambda_i
eps = 1e-6;
dnum = zeros(2,1);
for i = 1:2
    bp = b; bp(i) = bp(i) + eps;
    bm = b; bm(i) = bm(i) - eps;
    [~, fp] = quadprog(H, c, A, bp, [], [], [], [], [], opts);
    [~, fm] = quadprog(H, c, A, bm, [], [], [], [], [], opts);
    dnum(i) = (fp - fm) / (2*eps);
end
fprintf('=== f) Osjetljivost ===\n');
fprintf('dp*/db1: numericki %+.6f   -lambda1 = %+.6f\n', dnum(1), -lambda1);
fprintf('dp*/db2: numericki %+.6f   -lambda2 = %+.6f\n\n', dnum(2), 0);

%% c) Graficki prikaz: dozvoljeni skup, nivo krivulje, gradijenti
fig = figure('Color', 'w', 'Position', [100 100 760 620]);
hold on; box on;

x1 = linspace(0, 12, 400);
x2 = linspace(0, 12, 400);
[X1, X2] = meshgrid(x1, x2);
Fv = X1.^2 + 2*X2.^2 - 0.3*X1.*X2 + 2*X1 - 3*X2;

% Dozvoljeni skup: x1 + x2 >= 10  i  x1 - x2 <= 3, unutar prozora [0,12]^2.
% Crta se kao poligon (patch), ne kao rasterska maska - pouzdanije u vektorskom PDF-u.
Pverts = [6.5 3.5; 0 10; 0 12; 12 12; 12 9];
hFeas = patch(Pverts(:,1), Pverts(:,2), [0.30 0.55 0.85], ...
      'FaceAlpha', 0.18, 'EdgeColor', 'none');

% nivo krivulje funkcije cilja
lvl = [40 50 75 95 120 150];
[Cc, hc] = contour(X1, X2, Fv, lvl, 'LineColor', [0.45 0.45 0.45], 'LineWidth', 0.7);
clabel(Cc, hc, 'FontSize', 8, 'Color', [0.45 0.45 0.45], 'LabelSpacing', 400);
contour(X1, X2, Fv, [f(x_kkt) f(x_kkt)], 'LineColor', [0.85 0.2 0.2], 'LineWidth', 1.8);

% rubovi ogranicenja
plot(x1, 10 - x1, 'k-', 'LineWidth', 1.6);
plot(x1, x1 - 3,  'k--', 'LineWidth', 1.6);

% Gradijenti u KKT tocki. Zadatak trazi gradijente ogranicenja (oba) i
% funkcije cilja, pa se crta i gradijent neaktivnog ogranicenja g2.
gf  = H*x_kkt + c;          % gradijent funkcije cilja
g1  = A(1,:)';              % gradijent aktivnog ogranicenja g1
g2  = A(2,:)';              % gradijent neaktivnog ogranicenja g2
sc  = 1.6;
fprintf('=== c) Gradijenti u KKT tocki ===\n');
fprintf('grad f(x*)  = [%+.6f; %+.6f]\n', gf(1), gf(2));
fprintf('grad g1(x*) = [%+.6f; %+.6f]  (aktivno)\n', g1(1), g1(2));
fprintf('grad g2(x*) = [%+.6f; %+.6f]  (neaktivno, lambda2 = 0)\n', g2(1), g2(2));
fprintf('provjera: grad f + lambda1*grad g1 = [%.2e; %.2e]\n\n', ...
        gf(1)+lambda1*g1(1), gf(2)+lambda1*g1(2));

q1 = quiver(x_kkt(1), x_kkt(2), sc*gf(1)/norm(gf), sc*gf(2)/norm(gf), 0, ...
     'Color', [0.85 0.2 0.2], 'LineWidth', 2, 'MaxHeadSize', 0.9);
q2 = quiver(x_kkt(1), x_kkt(2), sc*g1(1)/norm(g1), sc*g1(2)/norm(g1), 0, ...
     'Color', [0.1 0.4 0.1], 'LineWidth', 2, 'MaxHeadSize', 0.9);
q3 = quiver(x_kkt(1), x_kkt(2), sc*g2(1)/norm(g2), sc*g2(2)/norm(g2), 0, ...
     'Color', [0.85 0.45 0.05], 'LineWidth', 2, 'MaxHeadSize', 0.9, ...
     'LineStyle', '--');

plot(x_kkt(1), x_kkt(2), 'ko', 'MarkerFaceColor', 'y', 'MarkerSize', 9);
text(x_kkt(1)+0.30, x_kkt(2)-0.55, 'x^*', 'FontSize', 12, 'FontWeight', 'bold');

xlabel('x_1'); ylabel('x_2');
title('Dozvoljeni skup, nivo krivulje i gradijenti u KKT tocki');
legend([hFeas q1 q2 q3], {'dozvoljeni skup', '\nabla f(x^*)', ...
       '\nabla g_1(x^*) (aktivno)', '\nabla g_2(x^*) (neaktivno)'}, ...
       'Location', 'northeast');
axis([0 12 0 12]); axis square;

exportgraphics(fig, fullfile(figDir, 'zad1_kkt.pdf'), 'ContentType', 'vector');
fprintf('Slika spremljena: %s\n', fullfile(figDir, 'zad1_kkt.pdf'));
