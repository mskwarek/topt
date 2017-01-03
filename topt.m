clear all;
close all;

n = 1.42;
nc = 1.5;
lambda = 1.55 * 1e-6;
a = 1e-6;

k = 2* pi./lambda;

u = a.*sqrt(k.^2 * nc.^2 - beta.^2);
w = a.*sqrt(beta.^2 - k.^2 * n.^2);
v = a .* k .* sqrt(nc.^2 - n.^2);

m = 1
eq1 = u.*besselj(m-1, u)./besselj(m, u) + w.* besselh(m-1, w)./besselh(m,w) == 0;
eq2 = w^2 + u^2 - v^2 == 0;
beta0 = 0;




fsolve(eq1, beta0)
