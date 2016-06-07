import pandas as pd
import numpy as np
import itertools
execfile("../toolbox.py")
from scipy.stats import chisquare


def p_value(x, expected=[1 / 2., 1 / 2.]):
    exp_array = np.array(expected) * x['size']
    return chisquare(
        [x['mean'] * x['size'], (1 - x['mean']) * x['size']], exp_array)[1]


def staring_relevant(x):
    res = str(x['mean'])[:7]
    if x['p-value'] < 0.1:
        res += '*'
    if x['p-value'] < 0.05:
        res += '*'
    if x['p-value'] < 0.01:
        res += '*'
    return res


def means_table_4var(comb, data, nbr_quantiles=[2, 2, 2, 4]):
    var_1, var_2, var_3, output = comb[0], comb[1], comb[2], comb[3]

    # create new column on data to inform which quantile a line belongs to
    frame = quartilize_periodwise(data[comb], nbr_quantiles)
    frame.columns = ['qu_' + var for var in frame.keys()]
    frame['qu_' + output] = (frame['qu_' + output] == 3).apply(int)
    m = frame['qu_' + output].mean()
    freq_exp = [m, 1 - m]
    means = {i : comp_means(comb[1:], frame.query('qu_' + var_1 + " == " + str(i)), freq_exp)
                for i in range(nbr_quantiles[0])}
    means['all'] = comp_means(comb[1:], frame, freq_exp)
    for i in range(nbr_quantiles[0]) + ['all']:
        means[i].index = pd.MultiIndex.from_tuples(
        [(i, it[0], it[1]) for it in means[i].index.to_native_types().tolist()])
        means[i].index.names = [var_1, var_3, var_2]
    return pd.concat(means.values())


def get_means_table(comb, data, nbr_quantiles=[3, 3, 4]):
    # create new column on data to inform which quantile a line belongs to
    frame = quartilize_periodwise(data, nbr_quantiles)
    frame.columns = ['qu_' + var for var in frame.keys()]
    frame['qu_' + comb[-1]] = (frame['qu_' + comb[-1]] == 3).apply(int)
    m = frame['qu_' + comb[-1]].mean()
    freq_exp = [m, 1 - m]
    return comp_means(comb, frame, freq_exp)


def comp_means(comb, qu_data, freq_exp, functions=['mean', 'size']):
    var_1, var_2, output = comb[0], comb[1], comb[2]

    # compute mean values for each sub-groups
    center = qu_data.groupby(['qu_' + var_1, 'qu_' + var_2]).agg(functions)['qu_' + output]

    # adding stars when mean significantly away from mean
    center['p-value'] = center.apply(lambda x: p_value(x, expected=freq_exp), axis=1)
    center['mean'] = center.apply(staring_relevant, axis=1)
    del center['p-value']

    # displaying arrangement
    center = center.stack().unstack('qu_' + var_1)

    # compute mean for var_2 only
    last_col = qu_data.groupby(['qu_' + var_2]).agg(functions)['qu_' + output]

    # adding stars when mean significantly away from mean
    last_col['p-value'] = last_col.apply(lambda x: p_value(x, expected=freq_exp), axis=1)
    last_col['mean'] = last_col.apply(staring_relevant, axis=1)
    del last_col['p-value']

    # displaying arrangement
    last_col = last_col.stack()

    # compute mean for var_1 only
    last_row = qu_data.groupby(['qu_' + var_1]).agg(functions)['qu_' + output]

    # adding stars when mean significantly away from mean
    last_row['p-value'] = last_row.apply(lambda x: p_value(x, expected=freq_exp), axis=1)
    last_row['mean'] = last_row.apply(staring_relevant, axis=1)
    del last_row['p-value']

    # displaying arrangement
    last_row = last_row.transpose()
    last_row['0'] = [''] * len(functions)
    last_row.index = pd.MultiIndex.from_tuples(
        [("all", var) for var in last_row.index])
    full_mat = pd.concat([pd.concat([center, last_col], axis=1),
                          last_row])
    full_mat.columns = range(center.shape[1]) + ['all']
    full_mat.index.names = [var_2, var_1]
    full_mat.loc[('all', 'mean'), 'all'] = qu_data['qu_' + output].mean()
    full_mat.loc[('all', 'size'), 'all'] = len(qu_data['qu_' + output])
    return full_mat


def generate_optimal_dataset(comb, data):
    data_ten_y = resample(data[comb], 10, 5).dropna()
    return data_ten_y


def check_anormal_corr(comb, data_set):
    means_table = get_means_table(comb, data_set)
    cond = True
    for j in range(nbr_quantiles[0] - 1):
        test = means_table[j] - means_table[j+1]
        cond *= (test.loc[:, functions[0]] * test.loc[('all',functions[0])] > 0).all()
        test = means_table.loc[(j, functions[0])] - means_table.loc[(j+1, functions[0])]
        cond *= (test * test.loc['all'] > 0).all()
    if not cond:
        return means_table
    else:
        return -1


def iter_all_variables(list_of_variables, data):
    anormal_corr = {}
    combinaisons = [list(tu)
                    for tu in itertools.combinations(list_of_variables, 2)]
    # all possible combinaisons of 3 variables (var_1, var2, output)
    for comb in combinaisons:
        data_set = generate_optimal_dataset(comb + ['growth'], data)
        res = check_anormal_corr(comb + ['growth'], data_set)
        if type(res) != int:
            anormal_corr[str(comb + ['growth'])] = res
    return anormal_corr


data = pd.read_csv("../data_source/all_data.csv", index_col=['code', 'year'])

data = data.rename(columns={"GDP_PC_WB": "gdp", "years_schooling": "schl",
                            "investments_WB": "invst", "gini_net_SWIID": "gini",
                            "nat_ress_WB": "nat_ress"})


for var in ["invst", "schl", "nat_ress", 'gdp']:
    print "Var1 = Gini , Var 2 = ", var, "Output = growth"
    sel = data[np.unique([var, "gdp", "gini"]).tolist()]
    data_ten_y = resample(sel, 10, 5)
    data_ten_y['gdp'] = data_ten_y['gdp'].apply(np.log)
    data_ten_y['growth'] = growth(data_ten_y, "gdp", how='past')
    data_ten_y = data_ten_y[[var, "gini", 'growth']].dropna()
    print get_means_table([var, "gini", "growth"], data_ten_y), '\n'


var_selection = ['invst', "gdp", "gini"]
quantiles = [2, 4, 2, 4]
sel = data[var_selection]
data_ten_y = resample(sel, 10, 5)
data_ten_y['gdp'] = data_ten_y['gdp'].apply(np.log)
data_ten_y['growth'] = growth(data_ten_y, "gdp", how='past')
data_ten_y = data_ten_y.dropna()
res =  means_table_4var(var_selection + ["growth"],
                         data_ten_y, nbr_quantiles=quantiles)
print res


#
# OECD set up
# #
# list_of_OECD = np.unique(data[data["gini_post_taxe_OECD"].notnull()].reset_index()['code'])
# data = data.query("code in " + str(list_of_OECD.tolist()))
#
#
# for var in ["invst"]:
#     print "Var1 = Gini , Var 2 = ", var, "Output = growth"
#     sel = data[np.unique([var, "gdp", "gini"]).tolist()]
#     data_ten_y = resample(sel, 5, 3)
#     # Conforming to the OECD study
#     data_ten_y['gdp'] = data_ten_y['gdp'].apply(np.log)
#     data_ten_y['growth'] = growth(data_ten_y, "gdp", how='futur')
#     data_ten_y = data_ten_y[[var, "gini", 'growth']].dropna()
#     print get_means_table([var, "gini", "growth"], data_ten_y), '\n'
#
#
# sel = data[['invst', "gdp", "gini"]]
# data_ten_y = resample(sel, 5, 3)
# # Conforming to the OECD study
# data_ten_y['gdp'] = data_ten_y['gdp'].apply(np.log)
# data_ten_y['growth'] = growth(data_ten_y, "gdp", how='futur')
# data_ten_y = data_ten_y.dropna()
# res =  means_table_4var(["gini", "gdp", "invst", "growth"],
#                          data_ten_y)
# print res
