#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from Tkinter import *

FIELDS = ("Długość fali","Fiber 1","Fiber 2","Fiber 3", "Mod m", "Mod p")
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
    for i in range(0, len(u0)):
        eq = Equations(config)
        x_prim = fsolve(eq.fun, [u0[i], w0[i]])
        if np.imag(x_prim[0]) == 0 and np.imag(x_prim[1]) == 0 and x_prim[0] >= 0 and x_prim[1] >= 0:
            x1.append(x_prim)
            n += 1
    return x1


def determine_electric_field(config, x):
    return None


def get_linspace_args(config_data):
    return np.linspace(-2 * config_data.fiber.a, 2 * config_data.fiber.a, 150)

def get_solutions(x):
    x = [[(round(10 * x[i][j]) / 10) for i in range(0, len(x))] for j in range(0, len(x[0]))]
    x = np.matrix(x)
    x = x.transpose()
    u_solution = x[:, 0]
    w_solution = x[:, 1]
    return u_solution, w_solution


def determine_electric_field(config_data, x):
    u, w = get_solutions(x)
    x = get_linspace_args(config_data)
    Ey = np.matrix([[float(0) for i in range(0, len(x))] for j in range(0, len(x))])
    # %Obliczanie pola elektrycznego
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

def main(config):
    config_data = config
    x = resolve_equations(config_data)

    Ey = determine_electric_field(config_data, x)
    if Ey is not None:
        plot_electric_field(config_data, Ey)
    else:
        print 'Podany mod nie rozchodzi sie w swiatlowodzie o zadanych parametrach'


def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"0")
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
   return entries

def create_gui():

	master = Tk()
	master.title('Projekt #2 TOPT')
	ents = makeform(master, FIELDS)
	
	b1 = Button(master, text='Rysuj', command=(lambda e=ents: parse_data(e)))
	b1.pack(side=LEFT, padx=5, pady=5)

	
	b2 = Button(master, text = "Zamknij", command=master.quit)
	b2.pack(side=LEFT, padx=5, pady=5)
	master.mainloop()


def parse_data(entries):
	
	lam = float(entries[FIELDS[0]].get()) #podawac w formacie z e, np 5e-06
	fiber_1 = float(entries[FIELDS[1]].get())
	fiber_2 = float(entries[FIELDS[2]].get())
	fiber_3 = float(entries[FIELDS[3]].get())
	fiber = Fiber(fiber_1, fiber_2, fiber_3)

	mod_m = int(entries[FIELDS[4]].get())
	mod_p = int(entries[FIELDS[5]].get())
	
	mod = Mod(mod_m, mod_p)
	config = Config(lam, fiber, mod)

	main(config)

if __name__ == '__main__':
	create_gui()
	
