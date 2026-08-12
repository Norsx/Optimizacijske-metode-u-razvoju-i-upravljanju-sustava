%% Kvadratni program u YALMIP-u
% min (x1-3)^2 + (x2-2)^2
% uz:
%   g1: -x1 <= 0
%   g2:  x1 - 2 <= 0
%   g3: -x2 <= 0
%   g4:  x2 - 1 <= 0

clear
clc
yalmip('clear')

% Varijable
x = sdpvar(2,1);   % x(1)=x1, x(2)=x2

% Ogranicenja (svako posebno da dobijemo pojedinacne dualne varijable)
g1 = (-x(1)   <= 0);
g2 = ( x(1)-2 <= 0);
g3 = (-x(2)   <= 0);
g4 = ( x(2)-1 <= 0);

Constraints = [g1, g2, g3, g4];

% Funkcija cilja
Objective = (x(1)-3)^2 + (x(2)-2)^2;

% Opcije: ako imas quadprog, mozes staviti solver 'quadprog',
% inace izostavi pa ce YALMIP sam izabrati solver.
ops = sdpsettings('verbose',0);  % ili: sdpsettings('solver','quadprog','verbose',0);

% Rjesavanje
sol = optimize(Constraints, Objective, ops);

if sol.problem ~= 0
    error('Problem nije uspjesno rijesen. Kod: %d, poruka: %s', sol.problem, sol.info);
end

% Primarne varijable
x_opt = value(x);
fval  = value(Objective);

disp('Optimalno rjesenje (primarne varijable):');
disp(x_opt);

disp('Minimalna vrijednost funkcije:');
disp(fval);

% Dualne varijable za svako ogranicenje
lambda_g1 = dual(g1);
lambda_g2 = dual(g2);
lambda_g3 = dual(g3);
lambda_g4 = dual(g4);

fprintf('\nDualne varijable (Lagrangeovi multiplikatori):\n');
fprintf('lambda_g1 ( -x1 <= 0 )   = %g\n', lambda_g1);
fprintf('lambda_g2 ( x1-2 <= 0 )  = %g\n', lambda_g2);
fprintf('lambda_g3 ( -x2 <= 0 )   = %g\n', lambda_g3);
fprintf('lambda_g4 ( x2-1 <= 0 )  = %g\n', lambda_g4);


%% Rucno rjesavanje primarnog i dualnog QP problema (bez toolboxa)
% Problem:
%   min f(x) = (x1-3)^2 + (x2-2)^2
%   uz ogr.:
%       g1: -x1 <= 0
%       g2:  x1 - 2 <= 0
%       g3: -x2 <= 0
%       g4:  x2 - 1 <= 0
%
% U QP-obliku (bez konstante 13):
%   min  1/2 x' Q x + c' x
%   s.t. G x - h <= 0
% [file:52]

clear
clc

% 1) Parametri primarnog problema
Q = [2 0;
     0 2];
c = [-6; -4];

G = [-1  0;
      1  0;
      0 -1;
      0  1];
h = [0; 2; 0; 1];

% 2) Neograniceni minimum (bez ogranicenja)
% gradijent: Q x + c = 0  ->  x_free = -Q^{-1} c
x_free = -inv(Q)*c;       % = [3; 2]
fprintf('Neograniceni minimum (bez ogranicenja): x_free = [%g; %g]\n', x_free);

% 3) Optimalna tocka u ogranicenom skupu [0,2]x[0,1]
x_opt = [min(max(x_free(1),0),2);
         min(max(x_free(2),0),1)];
fprintf('Optimalna tocka (projekcija na [0,2]x[0,1]): x* = [%g; %g]\n', x_opt);

% PRIMALNA VRIJEDNOST BEZ KONSTANTE:
f_tilde_opt = 0.5*x_opt.'*Q*x_opt + c.'*x_opt;
fprintf('~f(x*) = 1/2 x''Qx + c''x = %g\n', f_tilde_opt);

% ORIGINALNA FUNKCIJA S KONSTANTOM 13:
f_orig_opt = f_tilde_opt + 13;
fprintf('Originalna funkcija f(x*) = ~f(x*) + 13 = %g\n', f_orig_opt);

% 4) Dualne varijable iz KKT uvjeta
% L(x,mu) = 1/2 x'Qx + c'x + mu'(Gx - h)
% Stacionarnost: Q x_opt + c + G' mu = 0
% Komplementarna slackness: mu_i * (Gx_opt - h)_i = 0, mu >= 0

% Vrijednosti ogranicenja u optimumu
g_val = G*x_opt - h;
fprintf('\nVrijednosti g_i(x*) = Gx* - h:\n');
disp(g_val);

% g2 i g4 su aktivna (0), g1 i g3 strogo negativna -> mu1 = mu3 = 0
mu1 = 0;
mu3 = 0;

% Stacionarnost
Hx_f = Q*x_opt + c;
fprintf('Vektor Q*x_opt + c:\n');
disp(Hx_f);

% G' mu uz mu1 = mu3 = 0:
% G' = [-1  1  0  0;
%        0  0 -1  1]
% => (Qx* + c) + [mu2; mu4] = 0
mu2 = -Hx_f(1);
mu4 = -Hx_f(2);

mu_opt = [mu1; mu2; mu3; mu4];

fprintf('\nOptimalne dualne varijable mu* (iz KKT):\n');
disp(mu_opt);

% Provjera komplementarne slackness i nenegativnosti
comp = mu_opt .* g_val;
fprintf('mu_i * g_i(x*):\n');
disp(comp);

fprintf('Jesu li sve mu_i >= 0 ? %d (1 = da, 0 = ne)\n', all(mu_opt >= -1e-10));

% 5) Dualna funkcija (za tilde f) i strong duality
% Prema prezentaciji:
% l(mu) = -1/2 mu' G Q^{-1} G' mu + (-c' Q^{-1} G' - h') mu - 1/2 c' Q^{-1} c
% [file:52]
Qinv = inv(Q);
M = -0.5 * (G * Qinv * G.');          % kvadratni dio u mu
q_dual = (-c.' * Qinv * G.' - h.');   % linearni dio
const_dual = -0.5 * c.' * Qinv * c;   % konstanta

l_mu = mu_opt.' * M * mu_opt + q_dual * mu_opt + const_dual;

fprintf('\nDualna funkcija l(mu*) (za ~f) = %g\n', l_mu);
fprintf('Primal-dual razlika (~f(x*) - l(mu*)) = %g (treba biti ~0)\n', ...
        f_tilde_opt - l_mu);
