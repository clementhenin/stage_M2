import pandas as pd
import pdb

PATH_TO_DATA = "/home/clement/Documents/stage_M2/data_source/"

code_country_dict = pd.read_csv(PATH_TO_DATA + "country_code_list.csv")


def country_harmonize(x, y):
    if type(x) == str:
        return x
    else:
        return y

# Creates an empty dataset
data_frame = pd.DataFrame()

"""Adding the data from Deininger and Squire
"""
D_S = pd.read_csv(PATH_TO_DATA + "income_inequality_Deininger_Squire.csv")
data_frame = D_S[['Code', 'Year', 'Gini', 'Quality']]
data_frame.columns = ['code', 'year', 'gini_DS', 'quality']

data_frame['code'] = data_frame['code'].astype(str)
data_frame['year'] = data_frame['year'].astype(int)
data_frame['gini_DS'] = data_frame['gini_DS'].astype(float)
data_frame['quality'] = data_frame['quality'].astype(str)

"""Adding the data from Penn World Table
"""
df = pd.ExcelFile(PATH_TO_DATA + 'GDPs_PWT.xlsx')
selected_cols = ["countrycode",
                 "year",
                 "rgdpe",
                 "pop"]

data = df.parse("Data")
data = data[selected_cols]

data["pop"] = data['rgdpe'] / data['pop']

data.columns = ["code",
                "year",
                "GDP_PWT",
                "GDP_PC_PWT"]

data['code'] = data['code'].astype(str)
data['year'] = data['year'].astype(int)
data['GDP_PWT'] = data['GDP_PWT'].astype(float)
data['GDP_PC_PWT'] = data['GDP_PC_PWT'].astype(float)

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

"""Adding the governments expenditure from data.worldbank.org
"""

# Importing the data from the csv file
P_20 = pd.read_csv(PATH_TO_DATA + "governments_consumption_over_GDP.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'gov_consumption_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['gov_consumption_WB'] = P_20['gov_consumption_WB'].astype(float)

result = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

data_frame = result

del P_20, result

"""Adding the years of schooling from Barro-Lee
"""

# Importing the data from the csv file
P_20 = pd.read_csv(
    PATH_TO_DATA + "barro_lee_education_data.csv")

P_20 = P_20[["WBcode", "year", "yr_sch"]]

# selects the data and transpose it to the good format
P_20.columns = ["code", 'year', 'years_schooling']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['years_schooling'] = P_20['years_schooling'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

"""Adding the democracy index from PRIO
"""

# Importing the data from the csv file
P_20 = pd.read_csv(
    PATH_TO_DATA + "democracy_index.csv")

P_20 = P_20[["code", "year", "democracy_index"]]

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['democracy_index'] = P_20['democracy_index'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20


""" Adding the GDP at market price from data.worldbank.org
"""
# Importing the data from the csv file
P_20 = pd.read_csv(PATH_TO_DATA + "GDP_at_market_prices.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'GDP_MP_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['GDP_MP_WB'] = P_20['GDP_MP_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

"""Adding the GDP growth from data.worldbank.org
"""

# Importing the data from the csv file
P_20 = pd.read_csv(PATH_TO_DATA + "GDP_growth_WB.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'GDP_growth_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['GDP_growth_WB'] = P_20['GDP_growth_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

data_frame.sort(['code', 'year']).to_csv("barro_data.csv", index=False)


"""Adding the inflation from data.worldbank.org
"""

# Importing the data from the csv file
P_20 = pd.read_csv(PATH_TO_DATA + "inflation_consumer_price_WB.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'inflation_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['inflation_WB'] = P_20['inflation_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

data_frame.sort(['code', 'year']).to_csv("barro_data.csv", index=False)

"""Adding the fertility rate from data.worldbank.org
"""

# Importing the data from the csv file
P_20 = pd.read_csv(PATH_TO_DATA + "fertility_rate.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'fertility_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['fertility_WB'] = P_20['fertility_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

data_frame.sort(['code', 'year']).to_csv("barro_data.csv", index=False)


data_frame.sort(['code', 'year']).to_csv("barro_data.csv", index=False)
