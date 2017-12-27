import matplotlib.pyplot as plt
import time
import numpy as np
from fx import ackley, ackley_noise_creator
from zoopt import Dimension, Objective, Parameter, Opt, Solution
from zoopt.utils.zoo_global import gl
from quick_start import result_analysis


# ssracos example for minimizing ackley with Gaussian noise
def minimize_ackley_continuous_noisy():
    gl.set_seed(10001)  # set random seed
    t1 = time.clock()
    repeat = 1  # repeat of optimization experiments
    result = []
    history = []
    for i in range(repeat):
        # setup optimization problem
        ackley_noise_func = ackley_noise_creator(0, 0.1)
        dim_size = 100  # dimensions
        dim_regs = [[-1, 1]] * dim_size  # dimension range
        dim_tys = [True] * dim_size  # dimension type : real
        dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
        objective = Objective(ackley_noise_func, dim, balance_rate=0.5)  # form up the objective function
        budget = 200000  # 20*dim_size  # number of calls to the objective function
        parameter = Parameter(budget=budget, suppression=True, non_update_allowed=500, resample_times=100)

        # perform the optimization
        solution = Opt.min(objective, parameter)

        print('solved solution is:')
        solution.print_solution()
        true_result = ackley(solution)
        result.append(true_result)
        # store the optimization result
        result.append(true_result)

        # for plotting the optimization history
        if i == 0:
            history.append([0 for k in range(budget)])  # init for reducing
        history.append(objective.get_history_bestsofar())
    average_regret = reduce(lambda x, y: np.array(x) + np.array(y), history) / repeat  # get average regret
    plt.plot(average_regret)
    # plt.show()
    plt.savefig("img/ackley_continuous_noisy_figure.png")  # uncomment this line and comment last line to save figures
    result_analysis(result, 1)
    t2 = time.clock()
    print('time cost: %f' % (t2 - t1))

if __name__ == '__main__':
    minimize_ackley_continuous_noisy()