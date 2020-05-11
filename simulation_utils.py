from Dispatcher import Dispatcher
import multiprocessing as mp
import matplotlib.pyplot as plt
import seaborn as sns


def compute_process_time_exp(beta, alpha):
    return beta*2


def compute_interval_time_exp(t_0, q, y):
    return t_0 + (1-q)*y


def plot2(x, y1, y2, d, title, xlabel, ylabel, path):
    plt.plot(x, y1, label=('Pod-' + str(d)))
    plt.scatter(x, y1, c='r')
    plt.plot(x, y2, label='JSQ')
    plt.scatter(x, y2, c='r')
    plt.xticks(x)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(xlabel)
    plt.legend()
    plt.savefig(path)
    plt.show()


def plot(df, d, title, xlabel, ylabel, path):
    plt.figure(figsize=(16, 9))
    sns.set(style='darkgrid',)
    sns.lineplot(x='Rho', y=ylabel, data=df,
                 hue='Policy', style='Policy',
                 markers=True, dashes=False)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.savefig(path)
    plt.show()


class Simulator:

    def __init__(self, number_of_tasks, number_of_servers, d):
        self.number_of_servers = number_of_servers
        self.number_of_tasks = number_of_tasks
        self.d = d

    def simulate(self, rho):
        dispatcher = Dispatcher(self.number_of_tasks,
                                self.number_of_servers,
                                rho, self.d)
        mean_sys_delay = dispatcher.execute_simulation()
        return mean_sys_delay

    def simulate_partial(self, rho, i, output: list, overheads: list):
        dispatcher = Dispatcher(self.number_of_tasks,
                                self.number_of_servers,
                                rho, self.d)
        mean_sys_delay = dispatcher.execute_simulation()
        overhead = dispatcher.compute_overhead()
        output.append((i, mean_sys_delay))
        overheads.append((i, overhead))

    def multiprocessing_simulation(self, rho_values, n_proc):
        processes = []
        # initialize the Manager for results and shared variables
        manager = mp.Manager()
        output = manager.list()
        overheads = manager.list()

        # initialize processes
        for i in range(len(rho_values)):
            p = mp.Process(target=self.simulate_partial,
                           args=[rho_values[i], i, output, overheads])
            processes.append(p)

        # start processes
        for p in processes:
            p.start()

        # wait for each process to terminate
        for p in processes:
            p.join()

        output.sort()
        overheads.sort()
        results = [r[1] for r in output]
        overheads = [r[1] for r in overheads]
        return results, overheads
