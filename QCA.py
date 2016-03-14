import pandas as pd
import numpy as np
import pdb


f_data = pd.read_csv("data_source/frankeinstein.csv",
                     index_col=['code', 'year'])


def quartilize_dataset(data, n_quartiles):
    data_copy = data.copy()
    data_copy = pd.DataFrame(data_copy)
    quartiles_thresholds = np.linspace(0, 100, n_quartiles + 1)[::-1]
    for var in data_copy.keys():
        data_copy["qu_" + var] = 0
        for i in range(n_quartiles):
            upper_limit = np.percentile(data_copy[var], quartiles_thresholds[i])
            lower_limit = np.percentile(data_copy[var], quartiles_thresholds[i + 1])
            if i == 0 :
                ith_qu_bool = data_copy[var].apply(lambda x: x <= upper_limit
                                              and x >= lower_limit)
            else :
                ith_qu_bool = data_copy[var].apply(lambda x: x < upper_limit
                                              and x >= lower_limit)
            data_copy["qu_" + var] += ith_qu_bool * (i + 1)
    return data_copy

for var in f_data.keys():
    quartilize_dataset(f_data[var], 4).sort_values(var).plot()
    plt.show()
