# -*- coding: utf-8 -*-
"""MVO FIX.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1soEZU9FqOwCHF424yK5aK-UOtx9xe9QO
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from google.colab import files
data_to_load = files.upload()

nasa_93 = pd.read_csv('dataset.csv')

EM = nasa_93["EM"]
LOC = nasa_93["loc"]
A_TD = nasa_93["A_TD"]
A_E = nasa_93["AE"]
LOC.head()

nasa = pd.DataFrame(nasa_93, columns=["EM", "loc", "AE", "A_TD"])

# Inisialisasi populasi awal
def initialize(pop_size, d, ub, lb):
    position = np.random.rand(pop_size, d) * (ub - lb) + lb
    return position

# def fitfun
def fitness_function_nasa(nasa, constant):
    a = constant[0]
    b = constant[1]
    c = constant[2]
    d = constant[3]
    total_mre_tdev = 0
    total_mre_effort = 0
    count = 0
    MMRE_TDEV = 0
    MMRE_EFFORT = 0
    tdev_list = []
    effort_list = []

    for row in nasa.itertuples():
        EM = row.EM
        LOC = row.loc
        A_TD = row.A_TD
        AE = row.AE
        PM = a * (LOC**b) * EM
        TD = c * (PM**d)
        mre_tdev = (abs(A_TD-TD) / A_TD) * 100
        mre_effort = (abs(AE-PM) / AE) * 100
        tdev_list.append(mre_tdev)
        effort_list.append(mre_effort)
        total_mre_tdev += mre_tdev
        total_mre_effort += mre_effort
        count += 1

    MMRE_TDEV = total_mre_tdev / count
    MMRE_EFFORT = total_mre_effort / count

    pd_data = {"MRE_TDEV": tdev_list, "MRE_EFFORT": effort_list}
    df = pd.DataFrame(pd_data)

    return [MMRE_TDEV, MMRE_EFFORT]

def multiverse_optimizer(pop_size, max_t, lb, ub, d, fit_fun):
    best_pos = np.zeros(d)
    best_val = [np.inf, np.inf]

    position = initialize(pop_size, d, ub, lb)
    convergence_curve = np.zeros(max_t)
    fitness_val = 0

    t = 0

    while t < max_t:
        for i in range(position.shape[0]):
            check_ub = position[i, :] > ub
            check_lb = position[i, :] < lb
            position[i, :] = (position[i, :] * ~(check_ub + check_lb)) + ub * check_ub + lb * check_lb

            fitness_val = fit_fun(nasa, position[i, :])
            if sum(fitness_val) < sum(best_val):
                best_val = fitness_val
                best_pos = position[i, :]

            r1 = np.random.rand()
            r2 = np.random.rand()
            A = 2 * r1 - 1
            C = 2 * r2
            l = np.random.rand()

            for j in range(position.shape[1]):
                distance2best = abs(best_pos[j] - position[i, j])
                position[i, j] = distance2best * np.exp(l) * np.cos(l * 2 * np.pi) + best_pos[j]

        t += 1
        convergence_curve[t - 1] = min(best_val)

    return best_pos, best_val, convergence_curve

# Example usage
pop_size = 30
max_t = 20
lb = -5
ub = 5
d = 4

best_pos, best_val, sol_convergence = multiverse_optimizer(pop_size, max_t, lb, ub, d, fitness_function_nasa)

# Calculate the best value and position for (a, b) pair

# Print results
print('Best Position (a, b):', best_pos[:2])
print('Best Value (a, b):', best_val[1])
print('Best Position (c, d):', best_pos[2:])
print('Best Value (c, d):', best_val[0])

plt.plot(sol_convergence, color='r')
plt.title('Convergence Curve')
plt.xlabel('Iteration')
plt.ylabel('Best Value')
plt.grid(True)
plt.show()