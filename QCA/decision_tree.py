import pandas as pd
from sklearn import tree
from sklearn.externals.six import StringIO
import os
from sklearn.externals.six import StringIO
from modified_sklearn.tree import export_graphviz as exp_graphviz
import pydot
import matplotlib.pyplot as plt
import itertools
from scipy.misc import comb
import statsmodels.api as sm
from sklearn import linear_model


execfile('../toolbox.py')

data = pd.read_csv("../data_source/all_data.csv", index_col=['code', 'year'])
data['rdstrb'] = data["gini_market_SWIID"] - data["gini_net_SWIID"]

var_list = ['gdp', 'gini_net'] # , "afrc", "ameri", "ferti", "PPPI" ,'invst',  "gini_mar",]

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


# # growth computation 2
# data_ten_y.loc[:, 'gdp'] = data_ten_y['gdp'].apply(np.log10)
# data_ten_y['g'] = growth(data_ten_y, "gdp", how='past')
# data_ten_y.loc[:, 'gdp'] = data_ten_y['gdp'] - data_ten_y['gdp'].groupby(level=1).mean()
# data_ten_y.loc[:, 'g'] = data_ten_y['g'] - data_ten_y['g'].groupby(level=1).mean()
# #data_ten_y.loc[:, 'g'] = data_ten_y['g'].apply(lambda x: (10**x - 1)* 100)
# data_ten_y = data_ten_y.dropna()


cont_data_1 = data_ten_y.copy()
# Regression tree using continuous noramlized
# cont_data_1.loc[:, 'g'] = cont_data_1['g'] - cont_data_1['g'].groupby(level=1).mean()
# cont_data_1['g'] = quartilize_periodwise(cont_data_1['g'], 4)

clf = tree.DecisionTreeRegressor(splitter='best', min_samples_leaf=35)
clf = clf.fit(cont_data_1[var_list], cont_data_1['g'])

cont_data_1.index = cont_data_1.index.to_native_types()
cont_data_1.index = map(lambda x: x[0] + str(x[1])[2:4], cont_data_1.index.tolist())
cont_data_1.index.name = "index"


dot_data = StringIO()
exp_graphviz(clf,
             cont_data_1,
             out_file=dot_data,
             # proportion=True,
             feature_names=var_list,
             filled=True, rounded=True,
             special_characters=True)

graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("RT_growth.pdf")
print "Regression : "
print pd.DataFrame(index=var_list, data=clf.feature_importances_), '\n'


# # cont_data_1 = cont_data_1[cont_data_1['gdp'] >= -0.13]
# data_norm = ((cont_data_1 - cont_data_1.mean(axis=0)) / cont_data_1.std(axis=0)).sort_index(level=1)
#
# X_sm = sm.add_constant(data_norm[var_list])
#
# model = sm.OLS(data_norm["g"], X_sm)
# all_results = model.fit()
# print(all_results.summary())
#




# truc = cont_data_1.query("""index == [
# 'BGD95', 'BOL95', 'CMR05', 'EGY75', 'GHA95', 'IND85', 'KEN75', 'KEN85', 'KEN95',
# 'KEN05', 'KGZ05', 'KHM05', 'MAR75', 'MLI95', 'MLI05', 'MRT95', 'MWI05', 'NER05',
# 'NPL95', 'NPL05', 'PAK85', 'PAK95', 'PAK05', 'PHL75', 'PNG05', 'RWA05', 'SEN95',
#  'UGA05', 'YEM05', 'ZWE95']""")
#
# plt.plot(truc['gini_net'], truc['g'], 'o')
# plt.xlabel("Gini net")
# plt.ylabel("Growth")
# plt.title("""A subgroup for which growth and inequalities are highly correlated \n
#         coef : -14.3, pvalue = 0.003""")
# plt.show()



#
# truc = cont_data_1.query("""index == ['BOL85', 'BOL95', 'BOL05', 'CHL85', 'CIV05', 'CMR05', 'DZA95', 'DZA05', 'ECU95',
# 'ECU05', 'EGY75', 'EGY85', 'EGY95', 'EGY05', 'GHA05', 'GUY95', 'GUY05', 'HND95',
# 'IDN85', 'IDN95', 'IDN05', 'IRN95', 'JAM75', 'JAM85', 'MNG95', 'MNG05', 'MRT95',
# 'MRT05', 'PER85', 'PER05', 'PNG95', 'PNG05', 'SYR05', 'TUN85', 'UKR05', 'VNM05',
# 'YEM05']""")
#
# plt.plot(truc['gini_net'], truc['g'], 'o')
# plt.xlabel("Gini net")
# plt.ylabel("Growth")
# plt.title("""A subgroup for which growth and inequalities are highly correlated \n
#         coef : -15, pvalue = 0.03""")
# plt.show()



# truc = cont_data_1.query("""index == ['ARG85', 'AUT85', 'BRA05', 'CHL85',
# 'COL05', 'CRI95', 'CRI05', 'DOM05', 'ECU95', 'ECU05', 'ESP85', 'HKG75',
# 'MEX95', 'MUS05', 'PAN85', 'PER95', 'PRT95', 'SLV05', 'THA05', 'TUN05',
# 'URY85', 'URY95', 'URY05', 'VEN05', 'ZAF95']""")
#
# plt.plot(truc['gini_net'], truc['g'], 'o')
# plt.xlabel("Gini net")
# plt.ylabel("Growth")
# plt.title("""A subgroup for which growth and inequalities are highly correlated \n
#         coef : -13.8, pvalue = 0.027""")
# plt.show()


#
# truc = cont_data_1.query("""index == ['CHL85', 'CHL95', 'CHL05', 'CZE05',
#  'CZE15', 'ESP85', 'EST05', 'EST15', 'GRC85', 'HUN05', 'HUN15', 'KOR75',
#   'KOR85', 'KOR95', 'KOR05', 'MEX75', 'MEX85', 'MEX95', 'MEX05', 'MEX15',
#    'POL05', 'POL15', 'PRT75', 'PRT85', 'PRT95', 'PRT15', 'RUS05', 'SVK05',
#     'SVK15', 'SVN15', 'TUR75', 'TUR85', 'TUR95', 'TUR05', 'TUR15']""")
#
#
# clf = linear_model.LinearRegression()
# clf.fit(truc[['gini_net']], truc['g'])
# plt.plot(truc['gini_net'], truc['g'], 'bo')
# plt.plot(truc['gini_net'], clf.predict(truc[['gini_net']]), 'b')
# plt.xlabel("Gini net")
# plt.ylabel("Growth")
# plt.title("""A subgroup for which growth and inequalities are correlated \n
#         coef : -13.7, pvalue = 0.012""")
#
# truc = cont_data_1.query("""index == ['AUS75', 'AUS85', 'AUS95', 'AUS05',
# 'AUT85', 'AUT05', 'AUT15', 'BEL85', 'BEL05', 'BEL15', 'CAN85', 'CAN95',
# 'CAN05', 'DEU85', 'DEU05', 'DEU15', 'ESP75', 'ESP95', 'ESP05', 'ESP15',
# 'FIN75', 'FIN85', 'FIN05', 'FIN15', 'FRA75', 'FRA85', 'FRA05', 'FRA15',
# 'GBR75', 'GBR85', 'GBR95', 'GBR05', 'GBR15', 'GRC75', 'GRC95', 'GRC05',
# 'GRC15', 'IRL75', 'IRL85', 'IRL95', 'IRL15', 'ISL15', 'ISR85', 'ISR95',
# 'ISR05', 'ITA75', 'ITA85', 'ITA95', 'ITA05', 'ITA15', 'JPN75', 'JPN05',
# 'KOR15', 'NLD85', 'NLD15', 'NZL75', 'NZL85', 'NZL95', 'NZL05', 'NZL15',
# 'PRT05', 'SVN05', 'USA15']""")
#
# plt.plot(truc['gini_net'], truc['g'], 'ro')
# clf = linear_model.LinearRegression()
# clf.fit(truc[['gini_net']], truc['g'])
# plt.plot(truc['gini_net'], clf.predict(truc[['gini_net']]), 'r')
# plt.title("""Two subgroups for which growth and inequalities are correlated \n
#         RED : coef : 11, pvalue = 0.04 ; BLUE : coef : -13.7, pvalue = 0.012""")
# plt.show()
#
#


#
#
# f, axarr = plt.subplots(int(comb(len(var_list), 2, exact=True)), 1, figsize=(20, len(var_list) * 9))
# for n, v in enumerate(itertools.combinations(var_list, 2)):
#     data_ten_y = resample(data[list(v)], 5, 3)
#
#     data_ten_y['gdp'] = data_ten_y['gdp'].apply(np.log10)
#     data_ten_y['g'] = growth(data_ten_y, "gdp", how='futur')
#     data_ten_y = data_ten_y.dropna()
#
#     # Regression tree using continuous noramlized
#     cont_data_1 = data_ten_y.copy()
#     cont_data_1.loc[:, 'g'] = cont_data_1['g'] - cont_data_1['g'].groupby(level=1).mean()
#     cont_data_1.loc[:, 'gdp'] = cont_data_1['gdp'] - cont_data_1['gdp'].groupby(level=1).mean()
#     # cont_data_1['g'] = quartilize_periodwise(cont_data_1['g'], 4)
#     cont_data_1.loc[:, 'g'] = cont_data_1['g'].apply(lambda x: (10**x -1) * 100)
#
#     x_min, x_max = cont_data_1[v[0]].min(), cont_data_1[v[0]].max()
#     y_min, y_max = cont_data_1[v[1]].min(), cont_data_1[v[1]].max()
#     plot_stepx = (x_max - x_min) / 100.
#     plot_stepy = (y_max - y_min) / 100.
#     xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_stepx),
#                          np.arange(y_min, y_max, plot_stepy))
#     clf_plot = tree.DecisionTreeRegressor(min_samples_leaf=25)
#     clf_plot = clf_plot.fit(cont_data_1[list(v)], cont_data_1['g'])
#     Z = clf_plot.predict(np.c_[xx.ravel(), yy.ravel()])
#     Z = Z.reshape(xx.shape)
#     c = axarr[n].contourf(xx, yy, Z, 8, cmap='jet')
#     axarr[n].contour(xx, yy, Z, 8, colors='black', linewidth=.5)
#     axarr[n].set_xlabel(v[0])
#     axarr[n].set_ylabel(v[1])
#     axarr[n].axis("tight")
#     plt.axes(axarr[n])
#     f.colorbar(c)
#     axarr[n].scatter(cont_data_1[v[0]], cont_data_1[v[1]], c="w")
#
# plt.savefig("two_variables_phase_space.pdf")

if len(var_list) == 2:
    x_min, x_max = cont_data_1[var_list[0]].min(), cont_data_1[var_list[0]].max()
    y_min, y_max = cont_data_1[var_list[1]].min(), cont_data_1[var_list[1]].max()
    plot_stepx = (x_max - x_min) / 100.
    plot_stepy = (y_max - y_min) / 100.
    xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_stepx),
                         np.arange(y_min, y_max, plot_stepy))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    c = plt.contourf(xx, yy, Z, 8, cmap='jet')
    plt.contour(xx, yy, Z, 8, colors='black', linewidth=.5)
    plt.xlabel(var_list[0])
    plt.ylabel(var_list[1])
    plt.axis("tight")
    plt.colorbar(c)
    plt.scatter(cont_data_1[var_list[0]], cont_data_1[var_list[1]], c="w")
plt.savefig("phase_space_representation.pdf", bbox_inches='tight')

# nbr_quantiles = [3, 3, 3, 3, 4]
#
# # Classification tree using growth quartiles
# cont_data = data_ten_y.copy()
# cont_data['g'] = quartilize_periodwise(cont_data['g'], 4)
# cont_data['g'] = (cont_data['g'] >= 2).apply(int)
# # cont_data['g2'] = (cont_data['g'] >= 2).apply(int)
# # cont_data['g3'] = (cont_data['g'] == 3).apply(int)
#
# clf = tree.DecisionTreeClassifier(min_samples_leaf=14)
# clf = clf.fit(cont_data[var_list], cont_data['g'])
#
# dot_data = StringIO()
# tree.export_graphviz(clf, out_file=dot_data,
#                      feature_names=var_list,
#                     #  proportion=True,
#                      filled=True, rounded=True,
#                      special_characters=True)
#
# graph = pydot.graph_from_dot_data(dot_data.getvalue())
# graph.write_pdf("CT_growth_median.pdf")
# print "Classification : "
# print pd.DataFrame(index=var_list, data=clf.feature_importances_)



# plt.plot(cont_data_1[cont_data_1['gdp'] >= -0.13]['gini_net'], cont_data_1[cont_data_1['gdp'] >= -0.13]['g'], 'x')
