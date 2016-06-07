import pandas as pd
import numpy as np
execfile("../toolbox.py")
import sys
import os


data = pd.read_csv("../data_source/all_data.csv", index_col=['code', 'year'])

# list_of_OECD = np.unique(data[data["gini_post_taxe_OECD"].notnull()].reset_index()['code'])
# data = data.query("code in " + str(list_of_OECD.tolist()))

var_list = ['gini', 'gdp', 'schl','invst']
nbr_quantiles = [3, 4, 2, 2, 4]

data = data.rename(columns={"GDP_PC_WB": "gdp", "years_schooling": "schl",
                            "investments_WB": "invst", "gini_net_SWIID": "gini",
                            "nat_ress_WB": "nat_ress"})

data['shocks'] = 0
data.loc[(slice(None),1972), 'shocks'] = 5
data.loc[(slice(None),1978), 'shocks'] = 5
data.loc[(slice(None),1980), 'shocks'] = 5
data.loc[(slice(None),1990), 'shocks'] = 5
data.loc[(slice(None),2007), 'shocks'] = 5


data_ten_y = resample(data[var_list], 10, 5)
data_ten_y['gdp'] = data_ten_y['gdp'].apply(np.log)
data_ten_y['growth'] = growth(data_ten_y, "gdp", how='past')
data_ten_y = data_ten_y.dropna()
data_ten_y = data_ten_y.rename(columns={"growth": "g"})

QCA_data = quartilize_periodwise(data_ten_y, nbr_quantiles)

QCA_data.index = QCA_data.index.to_native_types()
QCA_data.index = map(lambda x: x[0] + x[1][2:], QCA_data.index.tolist())
QCA_data.index.name = "index"

# print QCA_data.query("""index in ['CHL67','CHL82','CHL87','CHL02','CHL07','GRC67','IRL87','ISR87','KOR72','MEX72','MEX77','MEX87','MEX92','MEX97','MEX02','RUS97','RUS02','RUS07','TUR77','TUR82','TUR87','TUR02','TUR07']""")

QCA_data['g'] = (QCA_data['g'] == 3).apply(int)
QCA_data.to_csv("/tmp/temporary_quantile.csv")

data_ten_y.to_csv("/tmp/data_ten_y.csv")

R_script = """library(TeachingDemos)
#txtStart("results.txt", append=T)


#sink("results.txt", append=T, split=T, type = c("output", "message"))

ineg=read.csv(file='/tmp/temporary_quantile.csv', row.names='index')
library(QCA)
tt<-truthTable(ineg, outcome="g", conditions=c(VAR_LIST), incl.cut1=INCLUSION_CUT, sort.by='n', show.cases=T)
tt
write.csv(tt$tt, file='/tmp/R_qca_results.csv')
eqmcc(tt,details=T, show.cases=T)


#txtStop()
""".replace("VAR_LIST", str(var_list).replace('[', '').replace(']', '')
).replace("INCLUSION_CUT", str((1 / float(nbr_quantiles[-1])) * 1.5))

f = open("/tmp/r_script.R", "w")
f.write(R_script)
f.close()


os.system("Rscript /tmp/r_script.R")
