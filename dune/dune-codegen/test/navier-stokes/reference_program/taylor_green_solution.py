import numpy as np
import matplotlib.pyplot as plt

def pressure(t, x, y):
    rho = 1.0
    mu = 1.0/100
    nu = mu/rho
    pi = np.pi
    return -0.25*rho*np.exp(-4.0*pi**2*nu*t)*(np.cos(2.0*pi*x) + np.cos(2.0*pi*y))


def velocity(t, x, y):
    rho = 1.0
    mu = 1.0/100
    nu = mu/rho
    pi = np.pi
    v = np.empty(2)
    v[0] = -np.exp(-2.0*pi*mu/rho*t)*np.cos(pi*x)*np.sin(pi*y)
    v[1] = np.exp(-2.0*pi*mu/rho*t)*np.sin(pi*x)*cos(pi*y)
    return v


def v_0(t, x, y):
    rho = 1.0
    mu = 1.0/100
    nu = mu/rho
    pi = np.pi
    return -np.exp(-2.0*pi*mu/rho*t)*np.cos(pi*x)*np.sin(pi*y)


def v_1(t, x, y):
    rho = 1.0
    mu = 1.0/100
    nu = mu/rho
    pi = np.pi
    return np.exp(-2.0*pi*mu/rho*t)*np.sin(pi*x)*cos(pi*y)


def velocity_norm(t, x, y):
    rho = 1.0
    mu = 1.0/100
    nu = mu/rho
    pi = np.pi
    return np.sqrt((-np.exp(-2.0*pi*mu/rho*t)*np.cos(pi*x)*np.sin(pi*y))**2 + (np.exp(-2.0*pi*mu/rho*t)*np.sin(pi*x)*np.cos(pi*y))**2)


def plot_pressure(t, n):
    h = 2.0/n
    x = np.arange(-1,1,h)
    y = np.arange(-1,1,h)
    xx, yy = np.meshgrid(x, y, sparse=True)
    z = pressure(t, xx, yy)
    CS = plt.contourf(x,y,z)
    cbar = plt.colorbar(CS)
    plt.show()


def minmax_pressure(t, n):
    h = 2.0/n
    x = np.arange(-1,1,h)
    y = np.arange(-1,1,h)
    xx, yy = np.meshgrid(x, y, sparse=True)
    z = pressure(t, xx, yy)
    return np.min(z), np.max(z)


def plot_velocity(t, n):
    h = 2.0/n
    x = np.arange(-1,1,h)
    y = np.arange(-1,1,h)
    xx, yy = np.meshgrid(x, y, sparse=True)
    z = velocity_norm(t, xx, yy)
    CS = plt.contourf(x,y,z)
    cbar = plt.colorbar(CS)
    plt.show()


def minmax_velocity_norm(t, n):
    h = 2.0/n
    x = np.arange(-1,1,h)
    y = np.arange(-1,1,h)
    xx, yy = np.meshgrid(x, y, sparse=True)
    z = velocity_norm(t, xx, yy)
    return np.min(z), np.max(z)


print(minmax_velocity_norm(1.0, 64))

# plot_pressure(1.0, 100)
# plot_velocity(1.0, 100)

# dt = 1.0e-4
# n = 1000
# t = 0.0

# for i in range(20):
#     minimum, maximum = minmax_pressure(t, n)
#     print("t: {}, n: {}, minumum: {}, maximum: {}".format(t,n,minimum,maximum))
#     t = t + dt
