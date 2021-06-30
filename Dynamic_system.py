import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pylab as p
from scipy import integrate


class LotkiVolterra:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def dX_dt(self, X, t=0):
        """ Return the growth rate of fox and rabbit populations. """
        return np.array([self.a * X[0] - self.b * X[0] * X[1],
                         -self.c * X[1] + self.d * self.b * X[0] * X[1]])

    def d2X_dt2(self, X, t=0):
        """ Return the Jacobian matrix evaluated in X. """
        return np.array([[self.a - self.b * X[1], -self.b * X[0]],
                         [self.b * self.d * X[1], -self.c + self.b * self.d * X[0]]])

    def X_f1_Func(self):
        return np.array([self.c / (self.d * self.b), self.a / self.b])

    def analysis(self, t, X0):
        X_f0 = np.array([0., 0.])
        X_f1=self.X_f1_Func()
        if all(self.dX_dt(X_f0) != np.zeros(2)) and all(self.dX_dt(X_f1) != np.zeros(2)):
             return None

        A_f0 = self.d2X_dt2(X_f0)
        A_f1 = self.d2X_dt2(X_f1)
        lambda1, lambda2 = np.linalg.eigvals(A_f1)  # >>> (1.22474j, -1.22474j)
        # They are imaginary numbers. The fox and rabbit populations are periodic as follows from further
        # analysis. Their period is given by:
        # print(lambda1, lambda2)
        T_f1 = 2 * np.pi / abs(lambda1)  # >>> 5.130199

        X, infodict = integrate.odeint(self.dX_dt, X0, t, full_output=True)
        # print(X)
        return X


    def plot_x_t(self, name='rabbits_and_foxes_1.png'):
        t = np.linspace(0, 15, 1000)  # time
        X0 = np.array([10, 5])  # initials conditions: 10 rabbits and 5 foxes
        res = self.analysis(t, X0)
        if res is None:
            return None
        rabbits, foxes = res.T
        f1 = p.figure()
        p.plot(t, rabbits, 'r-', label='Rabbits')
        p.plot(t, foxes, 'b-', label='Foxes')
        p.grid()
        p.legend(loc='best')
        p.xlabel('time')
        p.ylabel('population')
        p.title('Evolution of fox and rabbit populations')
        f1.savefig(name)



class LotkiVolterraModified(LotkiVolterra):
    def __init__(self,a,b,c,d,e):
        super().__init__(a,b,c,d)
        self.e = e

    def dX_dt(self, X, t=0):
        """ Return the growth rate of fox and rabbit populations. """
        return np.array([self.a * X[0] - self.b * X[0] * X[1]-self.e*(X[0]**2),
                         -self.c * X[1] + self.d * self.b * X[0] * X[1]])

    def d2X_dt2(self, X, t=0):
        """ Return the Jacobian matrix evaluated in X. """
        return np.array([[self.a - self.b * X[1]-2*self.e*X[0], -self.b * X[0]],
                         [self.b * self.d * X[1], -self.c + self.b * self.d * X[0]]])

    def X_f1_Func(self):
        return np.array([self.c / (self.d * self.b), (self.a-self.e*self.c) / (self.d*(self.b**2))])


if __name__ == "__main__":
    # Definition of parameters
    a = 1.
    b = 0.1
    c = 1.5
    d = 0.75
    e = 0.8
    system = LotkiVolterra(a, b, c, d)
    system.plot_x_t('test.png')
    plt.show()
    modif = LotkiVolterraModified(a, b, c, d,e )
    modif.plot_x_t('test1.png')
    plt.show()