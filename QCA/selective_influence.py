import pandas as pd
import numpy as np
import sys
import os

from scipy.stats import ttest_ind

execfile("../toolbox.py")


def compute_influence_one_grp(group_indexes, data, infl_variable,
                              output, glb_mean_0, glb_mean_1):
    """Input : - group_indexes : list : list of the indexes defining the group
               - infl_variable : string : name of the variable that influence
               - output : string : name of the output variable
        Output : - influence : array : [share of output=1 in group variable=0,
                                        share of output=1 in group variable=1]
                 - p_value : float : p_value of Welch t_test
    """
    sel = data.query("index in " + str(group_indexes.split(','))
                     )[[infl_variable, output]]
    if len(sel)==0:
        return np.nan, np.nan
    print sel[sel[infl_variable]==0][output].values.tolist()
    pop_0 = sel[sel[infl_variable]==0][output] - glb_mean_0
    pop_1 = sel[sel[infl_variable]==1][output] - glb_mean_1
    effect = pop_0.mean() - pop_1.mean()
    p_value = ttest_ind(pop_0.values, pop_1.values,
                        equal_var=False, nan_policy='raise')[1]
    n_0 = len(pop_0)
    n_1 = len(pop_1)
    return effect, p_value, n_0, n_1


def compute_groups(data, list_of_variables, output):
    """Input : - data : pandas frame : all data quartalized
               - list_of_variables : list of string : variables selected to
                                    create the groups
                - output : string : name of the output variable
        Output : pandas frame : return the truth table computed with R
    """
    data[list_of_variables +[output]].to_csv("/tmp/data_sel_influ_script.csv")

    R_script = """ineg=read.csv(file='/tmp/data_sel_influ_script.csv', row.names='index')
    library(QCA)
    tt<-truthTable(ineg, outcome="OUTPUT", conditions=c(VAR_LIST), incl.cut1=0.5, show.cases=T)
    tt
    write.csv(tt$tt, file='/tmp/R_qca_results.csv')
    """.replace("VAR_LIST", str(list_of_variables).replace('[', '').replace(']', '')
    ).replace("OUTPUT", output)

    f = open("/tmp/r_script.R", "w")
    f.write(R_script)
    f.close()

    os.system("Rscript /tmp/r_script.R")

    return pd.read_csv('/tmp/R_qca_results.csv', index_col=[0])


def seek_max_influence_groups(cat_data, list_of_variables, infl_var, output):
    """Name of the index column for data must be 'index'
    """
    groups = compute_groups(cat_data, list_of_variables, output)
    gbl_0 = cat_data[cat_data[infl_var]==0][output].mean()
    gbl_1 = cat_data[cat_data[infl_var]==1][output].mean()
    infl = groups['cases'].apply(
                lambda x: compute_influence_one_grp(x,
                                                    cat_data,
                                                    infl_var,
                                                    output,
                                                    gbl_0,
                                                    gbl_1))
    infl = zip(*infl)
    groups['effect'] = infl[0]
    groups['p_value'] = infl[1]
    groups['n_0'] = infl[2]
    groups['n_1'] = infl[3]
    return groups.sort_values('p_value')


data = pd.read_csv("../data_source/all_data.csv", index_col=['code', 'year'])
data['rdstrb'] = data["gini_market_SWIID"] - data["gini_net_SWIID"]

var_list = ['gdp', 'schl', 'gini_net', 'invst'] # , "afrc", "ameri", "ferti", "PPPI" ,'invst',  "gini_mar",]

data = data.rename(columns={"GDP_PC_WB": "gdp", "years_schooling": "schl",
                            "investments_WB": "invst", "gini_net_SWIID": "gini_net",
                            "nat_ress_WB": "nat_ress", "democracy_index": "demos",
                            "dummy_africa": "afrc", "gini_market_SWIID": 'gini_mar',
                            "fertility_WB": "ferti", "price_level_investment_PWT": "PPPI",
                            "dummy_south_america": "ameri"})


# list_of_OECD = np.unique(data[data["gini_post_taxe_OECD"].notnull()].reset_index()['code'])
# data = data.query("code in " + str(list_of_OECD.tolist()))

data_ten_y = resample(data[var_list], 10, 3)

# growth computation 1
data_ten_y.loc[:, 'gdp'] = (data_ten_y['gdp'] / data_ten_y['gdp'].groupby(level=1).mean()).apply(np.log10)
data_ten_y['g'] = growth(data_ten_y, "gdp", how='past')
data_ten_y.loc[:, 'g'] = data_ten_y['g'].apply(lambda x: (10**x - 1)* 100)
data_ten_y = data_ten_y.dropna()

data_ten_y = quartilize_periodwise(data_ten_y, 2)

data_ten_y.index = data_ten_y.index.to_native_types()
data_ten_y.index = map(lambda x: x[0] + str(x[1])[2:4], data_ten_y.index.tolist())
data_ten_y.index.name = "index"

res = seek_max_influence_groups(data_ten_y,
                          ['gdp', 'schl', 'invst'],
                          'gini_net',
                          'g')
