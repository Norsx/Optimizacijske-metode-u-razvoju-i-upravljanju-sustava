%% Zadatak 3 - Optimalna aproksimacija s ogranicenjima (profil ceste)
%
% Trosak je proporcionalan kolicini premjestenog materijala, dakle odstupanju
% ceste od terena mjerenom u 1-normi:  min ||y - h||_1.  Prema vjezbama 2
% (str. 9) to se reformulira kao  min 1'*t  uz  -t <= y - h <= t, sto je uz
% linearna ogranicenja na nagib i promjenu nagiba LINEARNI PROGRAM.
%
% Ogranicenja:  |grad y_i|  <= b1,   grad y_i  = (y_i - y_{i-1})/dx,        i = 1..N
%               |grad2 y_i| <= b2,   grad2 y_i = (y_i - 2y_{i-1} + y_{i-2})/dx^2, i = 2..N
%               y_0 = a,  y_N = b
%
% Pokretanje:  matlab -batch "run('src/zadatak3.m')"

clear; clc; close all;

projRoot = fileparts(fileparts(mfilename('fullpath')));
figDir = fullfile(projRoot, 'docs', 'figures');
if ~exist(figDir, 'dir'); mkdir(figDir); end

L = 10;
h = @(x) 0.0053*x.^4 - 0.095*x.^3 + 0.48*x.^2 - 0.3*x + 1;
a = h(0);
b = h(L);
fprintf('Rubni uvjeti: a = h(0) = %.4f,  b = h(L) = %.4f\n\n', a, b);

cases = struct( ...
    'name', {'A', 'A', 'B', 'B'}, ...
    'b1',   {0.5, 0.5, 0.5, 0.5}, ...
    'b2',   {0.5, 0.5, 0.2, 0.2}, ...
    'N',    {20, 100, 20, 100});

res = cell(numel(cases), 1);

for k = 1:numel(cases)
    c = cases(k);
    [y, x, cost, flag] = solve_road(L, h, a, b, c.b1, c.b2, c.N);
    res{k} = struct('x', x, 'y', y, 'cost', cost, 'case', c);

    dx = L / c.N;
    g1 = (y(2:end) - y(1:end-1)) / dx;
    g2 = (y(3:end) - 2*y(2:end-1) + y(1:end-2)) / dx^2;

    fprintf('--- slucaj %s, N = %3d  (b1 = %.1f, b2 = %.1f) ---\n', c.name, c.N, c.b1, c.b2);
    fprintf('  exitflag = %d (%s)\n', flag, ternary(flag == 1, 'optimalno', 'PROBLEM'));
    fprintf('  J = ||y-h||_1 = sum|y_i-h_i| = %.6f\n', cost);
    fprintf('  kolicina materijala J*dx           = %.6f\n', cost*dx);
    fprintf('  max |nagib|        = %.6f  (granica %.2f)\n', max(abs(g1)), c.b1);
    fprintf('  max |promjena nag| = %.6f  (granica %.2f)\n', max(abs(g2)), c.b2);
    fprintf('  rubni uvjeti: y_0 = %.6f, y_N = %.6f\n', y(1), y(end));
    fprintf('  aktivnih ogr. nagiba: %d / %d,  zakrivljenosti: %d / %d\n\n', ...
        sum(abs(abs(g1) - c.b1) < 1e-7), numel(g1), ...
        sum(abs(abs(g2) - c.b2) < 1e-7), numel(g2));
end

%% Slika: sva 4 slucaja
fig = figure('Color', 'w', 'Position', [80 80 1000 720]);
xf = linspace(0, L, 600);
for k = 1:4
    subplot(2, 2, k); hold on; grid on; box on;
    plot(xf, h(xf), 'k-', 'LineWidth', 1.4);
    plot(res{k}.x, res{k}.y, 'r-o', 'LineWidth', 1.3, 'MarkerSize', ...
         ternary(res{k}.case.N <= 20, 4, 2), 'MarkerFaceColor', 'r');
    plot([0 L], [a b], 'ko', 'MarkerFaceColor', 'g', 'MarkerSize', 7);
    xlabel('x'); ylabel('visina');
    title(sprintf('slucaj %s, N = %d  (b_1 = %.1f, b_2 = %.1f),  J = %.3f', ...
        res{k}.case.name, res{k}.case.N, res{k}.case.b1, res{k}.case.b2, res{k}.cost));
    legend('teren h(x)', 'cesta y(x)', 'rubni uvjeti', 'Location', 'northwest');
    ylim([0 5]);
end
exportgraphics(fig, fullfile(figDir, 'zad3_cesta.pdf'), 'ContentType', 'vector');
fprintf('Slika spremljena: %s\n', fullfile(figDir, 'zad3_cesta.pdf'));

%% Funkcije
function [y, x, cost, exitflag] = solve_road(L, h, a, b, b1, b2, N)
% LP:  varijable z = [y_0..y_N , t_0..t_N],  min 1'*t
    dx = L / N;
    n = N + 1;                 % broj cvorova
    nz = 2*n;                  % y i t
    x = linspace(0, L, n)';
    hv = h(x);

    % Cilj je 1'*t = sum_i t_i, tocno kako vjezbe 2 (str. 9) propisuju za
    % min ||Ax+b||_1: bez tezine dx. Fizikalna kolicina materijala dobiva se
    % naknadnim mnozenjem s dx (vidi ispis), sto ne mijenja minimizator.
    f = [zeros(n,1); ones(n,1)];

    A = []; bineq = [];

    % |y_i - h_i| <= t_i   ->   y - t <= h   i   -y - t <= -h
    I = speye(n); Z = sparse(n, n);
    A = [A; I, -I];      bineq = [bineq; hv];
    A = [A; -I, -I];     bineq = [bineq; -hv];

    % |y_i - y_{i-1}| <= b1*dx,  i = 1..N
    D1 = spdiags([-ones(N,1), ones(N,1)], [0 1], N, n);
    A = [A; D1, sparse(N, n)];   bineq = [bineq; b1*dx*ones(N,1)];
    A = [A; -D1, sparse(N, n)];  bineq = [bineq; b1*dx*ones(N,1)];

    % |y_i - 2y_{i-1} + y_{i-2}| <= b2*dx^2,  i = 2..N
    m2 = N - 1;
    D2 = spdiags([ones(m2,1), -2*ones(m2,1), ones(m2,1)], [0 1 2], m2, n);
    A = [A; D2, sparse(m2, n)];   bineq = [bineq; b2*dx^2*ones(m2,1)];
    A = [A; -D2, sparse(m2, n)];  bineq = [bineq; b2*dx^2*ones(m2,1)];

    % rubni uvjeti y_0 = a, y_N = b
    Aeq = sparse(2, nz);
    Aeq(1, 1) = 1;
    Aeq(2, n) = 1;
    beq = [a; b];

    opts = optimoptions('linprog', 'Display', 'off');
    [z, fval, exitflag] = linprog(f, A, bineq, Aeq, beq, [], [], opts);
    y = z(1:n);
    cost = fval;
end

function out = ternary(cond, x, y)
    if cond; out = x; else; out = y; end
end
