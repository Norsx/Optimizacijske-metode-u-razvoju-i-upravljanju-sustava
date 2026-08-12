%% Zadatak 4 - Robusna stabilizacija prekidackog (switching) sustava
%
%   xdot(t) = A(t)*x(t) + B*u(t),   A(t) = A_parno   kad je floor(t) paran
%                                          A_neparno kad je floor(t) neparan
%
% Pokretanje:  matlab -batch "run('src/zadatak4.m')"

clear; clc; close all;

projRoot = fileparts(fileparts(mfilename('fullpath')));
figDir = fullfile(projRoot, 'docs', 'figures');
if ~exist(figDir, 'dir'); mkdir(figDir); end

A_parno   = [-1, -pi/6; 3*pi/2, -1];
A_neparno = [-1, -3*pi/2; pi/6, -1];
B = [1; 0];
x0 = [1; 0];

Aof = @(t) A_parno*(mod(floor(t),2)==0) + A_neparno*(mod(floor(t),2)==1);

%% a) Jesu li oba moda Hurwitzova?
fprintf('=== a) Hurwitzovost pojedinih modova ===\n');
names = {'A_parno', 'A_neparno'};
mats  = {A_parno, A_neparno};
for k = 1:2
    ev = eig(mats{k});
    fprintf('%-10s: eig = %+.4f%+.4fi , %+.4f%+.4fi   max Re = %+.4f  -> Hurwitz: %d\n', ...
        names{k}, real(ev(1)), imag(ev(1)), real(ev(2)), imag(ev(2)), max(real(ev)), all(real(ev) < 0));
end
fprintf('Oba moda imaju svojstvene vrijednosti -1 +- i*pi/2 (jer je produkt\n');
fprintf('izvandijagonalnih elemenata u oba slucaja (pi/6)*(3pi/2) = pi^2/4).\n\n');

%% b) Simulacija prekidackog sustava u otvorenom krugu
fprintf('=== b) Prekidacki sustav (otvoreni krug) ===\n');
% Monodromijska matrica preko jednog perioda (2 s: 1 s parno + 1 s neparno)
Phi = expm(A_neparno*1) * expm(A_parno*1);
rho = max(abs(eig(Phi)));
fprintf('monodromijska matrica Phi = expm(A_neparno)*expm(A_parno)\n');
fprintf('eig(Phi) = %.6f, %.6f\n', real(eig(Phi)));
fprintf('spektralni radijus rho = %.6f  -> %s\n', rho, ternary(rho > 1, 'NESTABILAN', 'stabilan'));
fprintf('Floquetov eksponent = %+.6f  (rast e^{%.4f t})\n\n', log(rho)/2, log(rho)/2);

[t_ol, X_ol] = simulate_switched(Aof, zeros(2,1), x0, 12);

%% c) Sinteza statickog regulatora u = K*x
% Trazi se zajednicka kvadratna Ljapunovljeva funkcija V = x'Px za OBA moda:
%     (A_i + B*K)'*P + P*(A_i + B*K) < 0,  i = parno, neparno,  P > 0.
% Postojanje takvog P jamci eksponencijalnu stabilnost za PROIZVOLJNO
% prekapcanje, ne samo za ovo periodicno.
%
% Uvjet je bilinearan u (P,K), pa se "konveksificira" supstitucijom
% Q = P^-1 i Y = K*Q (predavanje 07, "Od analize do sinteze"):
%
%     A_i*Q + Q*A_i' + B*Y + Y'*B' < 0,   Q > 0,   K = Y*Q^-1.
%
% To je sustav linearnih matricnih nejednakosti, dakle SDP, i rjesava se
% YALMIP-om uz SeDuMi.
fprintf('=== c) Sinteza regulatora (LMI / SDP) ===\n');

n = 2;
epsi = 1e-4;
Q = sdpvar(n, n, 'symmetric');
Y = sdpvar(1, n, 'full');

LMI = [Q >= epsi*eye(n)];
for k = 1:2
    LMI = [LMI, mats{k}*Q + Q*mats{k}' + B*Y + Y'*B' <= -epsi*eye(n)];
end

sol = optimize(LMI, [], sdpsettings('verbose', 0, 'solver', 'sedumi'));
fprintf('SDP status: %s\n', yalmiperror(sol.problem));

Qv = value(Q);
Yv = value(Y);
K  = Yv / Qv;                 % K = Y*Q^-1
P  = inv(Qv);                 % P = Q^-1

fprintf('Q =\n'); disp(Qv);
fprintf('Y = [%.6f, %.6f]\n', Yv(1), Yv(2));
fprintf('K = [%.6f, %.6f]\n', K(1), K(2));
fprintf('P = Q^-1 =\n'); disp(P);
fprintf('eig(P) = %.6f, %.6f  -> P > 0: %d\n', min(eig(P)), max(eig(P)), all(eig(P) > 0));

minEigNegM = inf;
for k = 1:2
    Acl = mats{k} + B*K;
    M = Acl'*P + P*Acl;
    ev_cl = eig(Acl);
    fprintf('%-10s + BK: eig = %+.4f, %+.4f | eig(Acl''P+PAcl) = %+.4f, %+.4f -> ND: %d\n', ...
        names{k}, real(ev_cl(1)), real(ev_cl(2)), min(eig(M)), max(eig(M)), max(eig(M)) < 0);
    minEigNegM = min(minEigNegM, -max(eig(M)));
end
Phi_cl = expm((A_neparno + B*K)*1) * expm((A_parno + B*K)*1);
fprintf('spektralni radijus zatvorenog kruga = %.6e  (<< 1)\n', max(abs(eig(Phi_cl))));

% Eksponencijalna ocjena uz V = x'Px. Iz Vdot <= -lambda_min(-M)*|x|^2 i
% V >= lambda_min(P)*|x|^2 slijedi Vdot <= -alpha*V uz alpha = lambda_min(-M)/lambda_max(P),
% pa je |x(t)| <= sqrt(cond(P))*|x(0)|*exp(-alpha*t/2). Faktor sqrt(cond(P))
% nestaje samo za P = I; uz opci P iz SDP-a mora se navesti.
alpha = minEigNegM / max(eig(P));
condP = cond(P);
fprintf('jamceni pad: Vdot <= -%.4f V  =>  |x(t)| <= %.3f*|x(0)|*exp(-%.4f t)\n\n', ...
    alpha, sqrt(condP), alpha/2);

[t_cl, X_cl] = simulate_switched(Aof, B*K, x0, 12);

%% Slike
fig = figure('Color', 'w', 'Position', [80 80 980 720]);

subplot(2,2,1);
plot(t_ol, X_ol(:,1), 'LineWidth', 1.4); hold on;
plot(t_ol, X_ol(:,2), 'LineWidth', 1.4); grid on; box on;
xlabel('t [s]'); ylabel('x_i(t)');
title('(b) Otvoreni krug: stanja rastu');
legend('x_1', 'x_2', 'Location', 'northwest');

subplot(2,2,2);
plot(X_ol(:,1), X_ol(:,2), 'LineWidth', 1.2); hold on;
plot(x0(1), x0(2), 'ko', 'MarkerFaceColor', 'g', 'MarkerSize', 7);
grid on; box on; axis equal;
xlabel('x_1'); ylabel('x_2');
title('(b) Trajektorija u prostoru stanja');

subplot(2,2,3);
plot(t_cl, X_cl(:,1), 'LineWidth', 1.4); hold on;
plot(t_cl, X_cl(:,2), 'LineWidth', 1.4); grid on; box on;
xlabel('t [s]'); ylabel('x_i(t)');
title('(c) Zatvoreni krug: eksponencijalno gasenje');
legend('x_1', 'x_2', 'Location', 'northeast');

subplot(2,2,4);
plot(X_cl(:,1), X_cl(:,2), 'LineWidth', 1.2); hold on;
plot(x0(1), x0(2), 'ko', 'MarkerFaceColor', 'g', 'MarkerSize', 7);
plot(0, 0, 'kx', 'MarkerSize', 10, 'LineWidth', 1.5);
grid on; box on; axis equal;
xlabel('x_1'); ylabel('x_2');
title('(c) Trajektorija zatvorenog kruga');

exportgraphics(fig, fullfile(figDir, 'zad4_switching.pdf'), 'ContentType', 'vector');
fprintf('Slika spremljena: %s\n', fullfile(figDir, 'zad4_switching.pdf'));

%% Pomocne funkcije
function [T, X] = simulate_switched(Aof, BK, x0, Tend)
% Integrira xdot = (A(t) + BK)x po jednosekundnim intervalima na kojima je
% sustav vremenski invarijantan; ode45 se ne pusta preko tocke prekapcanja.
    T = []; X = []; x = x0;
    opts = odeset('RelTol', 1e-9, 'AbsTol', 1e-11);
    for k = 0:(Tend-1)
        A = Aof(k + 0.5) + BK;
        [tt, xx] = ode45(@(t, z) A*z, [k, k+1], x, opts);
        if ~isempty(T); tt = tt(2:end); xx = xx(2:end, :); end
        T = [T; tt]; X = [X; xx];
        x = xx(end, :)';
    end
end

function out = ternary(cond, a, b)
    if cond; out = a; else; out = b; end
end
