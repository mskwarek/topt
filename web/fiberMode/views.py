import math
import numpy as np
import itertools
import scipy
from scipy.optimize import fsolve
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib
from pylab import *

# n = 1.42
# nc = 1.5
# lam = 1.55 * 10**(-6)
# a = 10**(-6)

# a=a1*1e-6;
# lamb=lambda1.*1e-9;
# if n>=nc:
#    print zle dane wejsciowe


class Mod(object):
    def __init__(self, m, p):
        self.m = m
        self.p = p


class Fiber(object):
    def __init__(self, a, nc, n):
        self.a = a
        self.nc = nc
        self.n = n


class Config(object):
    def __init__(self, lam, fiber, mod):
        self.lam = lam
        self.fiber = fiber
        self.mod = mod


def get_test_data():
    lam = 5 * 10 ** (-6)  # dlugosc fali
    fiber_data = Fiber(5 * 10 ** (-6), 1.46, 1.45)
    mod = Mod(0, 1)
    return Config(lam, fiber_data, mod)


def get_normalized_freq(config):
    return ((2 * math.pi * config.fiber.a) / config.lam) * math.sqrt(config.fiber.nc ** 2 - config.fiber.n ** 2)


def cart2pol(a1, b1):
    rho = np.sqrt(a1 ** 2 + b1 ** 2)
    phi = np.arctan2(b1, a1)
    return phi, rho


def pol2cart(rho, phi):
    a1 = rho * np.cos(phi)
    b1 = rho * np.sin(phi)
    return a1, b1


class Equations(object):
    def __init__(self, config):
        self.config = config

    def fun(self, x1):
        a1 = (x1[0] * (scipy.special.jv(self.config.mod.m - 1, x1[0]) / scipy.special.jv(self.config.mod.m, x1[0]))) + \
             (x1[1] * (scipy.special.kv(self.config.mod.m - 1, x1[1]) / scipy.special.kv(self.config.mod.m, x1[1])))
        b1 = get_normalized_freq(self.config) ** 2 - x1[0] ** 2 - x1[1] ** 2
        return [a1, b1]


def get_equations(config):
    normalized_freq = get_normalized_freq(config)
    u = np.linspace(1e-3 * normalized_freq, normalized_freq - 1e-3 * normalized_freq, np.ceil(normalized_freq))
    w = np.sqrt(normalized_freq ** 2 - u ** 2)
    return u, w


def resolve_equations(config):
    x1 = []
    n = 0
    u0, w0 = get_equations(config)
    for i in range(0, len(u0)-1):
        eq = Equations(config)
        x_prim = fsolve(eq.fun, [u0[i], w0[i]])
        print x_prim
        if np.imag(x_prim[0]) == 0 and np.imag(x_prim[1]) == 0 and x_prim[0] >= 0 and x_prim[1] >= 0:
            x1.append(x_prim)
            n += 1
    return x1


def determine_electric_field(config, x):
    return None


def get_linspace_args(config_data):
    return np.linspace(-2 * config_data.fiber.a, 2 * config_data.fiber.a, 150)


def unique_rows(data):
    uniq = []
    print data
    for row1 in data:
        add = True
        for row2 in uniq:
            if row1[0] == row2[0] and row1[1] == row2[1]:
                add = False
        if add:
            uniq.append(row1)

    return np.matrix(uniq)
    #    return uniques


def get_solutions(x):
    print x
    x = [[(round(10 * x[i][j]) / 10) for i in range(0, len(x))] for j in range(0, len(x[0]))]
    x = np.matrix(x)
    x = x.transpose()
    print "x = ", x
    y = unique_rows(x.tolist())
    print "y = ", y
    u_solution = y[:, 0]
    w_solution = y[:, 1]
    return u_solution, w_solution


def determine_electric_field(config_data, x):
    u, w = get_solutions(x)
    x = get_linspace_args(config_data)
    Ey = np.matrix([[float(0) for i in range(0, len(x))] for j in range(0, len(x))])
    # %Obliczanie pola elektrycznego
    print "len u = ", len(u)
    print "p = ", config_data.mod.p
    if len(u) >= config_data.mod.p:
        for i in range(0, len(x)):
            for j in range(0, len(x)):
                [fi, r] = cart2pol(x[i], x[j])
                value = 0
                if r <= config_data.fiber.a:
                    value = ((scipy.special.jv(config_data.mod.m,
                                               (u[config_data.mod.p - 1] * r) / config_data.fiber.a)) /
                             (scipy.special.jv(config_data.mod.m, u[config_data.mod.p - 1]))) \
                            * np.cos(config_data.mod.m * fi)
                else:
                    value = (scipy.special.kv(config_data.mod.m,
                                              (w[config_data.mod.p - 1] * r) / config_data.fiber.a) /
                             (scipy.special.kv(config_data.mod.m, w[config_data.mod.p - 1]))) \
                            * np.cos(config_data.mod.m * fi)
                Ey[i, j] = value
        return Ey
    else:
        return None


def plot_electric_field(config_data, ey):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(get_linspace_args(config_data), get_linspace_args(config_data))
    surf = ax.plot_surface(X, Y, ey, rstride=1, cstride=1,
                           # facecolors=C,
                           antialiased=True)
    plt.show()


def parseRequest(request):
    lam = float(request['data_lam']) * 10 ** (-6)  # dlugosc fali
    fiber_data = Fiber(float(request['data_a']) * 10 ** (-6), float(request['data_nc']), float(request['data_n']))
    #print float(request['data_a']) * 10 ** (-6), float(request['data_nc']), float(request['data_n'])   
    mod = Mod(int(request['data_m']), int(request['data_p']))
    #print mod  
    return Config(lam, fiber_data, mod)


def validateData(config):
    if config.fiber.nc < config.fiber.n:
        raise Exception


def validateSolutions(solutions, cfg):
    if cfg.mod.p > len(solutions):
        raise Exception


def getMatrix(request):
    cfg = parseRequest(request)
    try:
        validateData(cfg)
        #config_data = get_test_data()
        x = resolve_equations(cfg)
        validateSolutions(x, cfg)
        Ey = determine_electric_field(cfg, x)

        return {"matrix" : np.matrix.tolist(Ey)}#, "v" : get_normalized_freq(config)}
    except:
        return {}


def main():
    config_data = get_test_data()
    x = resolve_equations(config_data)
    Ey = determine_electric_field(config_data, x)
    if Ey is not None:
        plot_electric_field(config_data, Ey)
    else:
        print 'Podany mod nie rozchodzi sie w swiatlowodzie o zadanych parametrach'

if __name__ == '__main__':
    main()
