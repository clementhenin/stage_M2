import pandas as pd
import pdb

code_country_dict = pd.read_csv("country_code_list.csv")

valid_codes = code_country_dict['code'].tolist()
known_invalid_codes = pd.read_csv("known_invalid_codes.csv",
                                  names=['code'])['code'].tolist()


def country_harmonize(x, y):
    if type(x) == str:
        return x
    else:
        return y

# Creates an empty dataset
data_frame = pd.DataFrame()

"""Adding the data from Deininger and Squire
"""
D_S = pd.read_csv("income_inequality_Deininger_Squire.csv")
data_frame = D_S[['Code', 'Year', 'Gini', 'Quntile 1',
                  'Quntile 2', 'Quntile 3', 'Quntile 4']]
data_frame.columns = [
    'code', 'year', 'gini_DS', 'Q4_DS', 'Q3_DS', 'Q2_DS', 'Q1_DS']

data_frame.loc[:, 'code'] = data_frame['code'].astype(str)
data_frame.loc[:, 'year'] = data_frame['year'].astype(int)
data_frame.loc[:, 'gini_DS'] = data_frame['gini_DS'].astype(float)
data_frame.loc[:, 'Q1_DS'] = data_frame['Q1_DS'].astype(float)
data_frame.loc[:, 'Q2_DS'] = data_frame['Q2_DS'].astype(float)
data_frame.loc[:, 'Q3_DS'] = data_frame['Q3_DS'].astype(float)
data_frame.loc[:, 'Q4_DS'] = data_frame['Q4_DS'].astype(float)

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from Deininger and Squire removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

""" Adding the 10 highest % from data.worldbank.org
"""
# Importing the data from the csv file
P_10 = pd.read_csv("10_highest_percent_income_share.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_10 = P_10[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_10.columns = ['code', 'year', 'D1_WB']

# Makes sure the types of the columns are good
P_10['code'] = P_10['code'].astype(str)
P_10['year'] = P_10['year'].astype(int)
P_10['D1_WB'] = P_10['D1_WB'].astype(float)

data_frame = pd.merge(data_frame, P_10, how='outer', on=['code', 'year'])

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from 10_highest_percent_income_share removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

del P_10

""" Adding the 10 lowest % from data.worldbank.org
"""
# Importing the data from the csv file
P_10 = pd.read_csv("10_lowest_percent_income_share.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_10 = P_10[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_10.columns = ['code', 'year', 'D9_WB']

# Makes sure the types of the columns are good
P_10['code'] = P_10['code'].astype(str)
P_10['year'] = P_10['year'].astype(int)
P_10['D9_WB'] = P_10['D9_WB'].astype(float)

data_frame = pd.merge(data_frame, P_10, how='outer', on=['code', 'year'])

del P_10

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from 10_lowest_percent_income_share removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))


""" Adding the 20 highest % from data.worldbank.org
"""
# Importing the data from the csv file
P_20 = pd.read_csv("first_20_percent_income_share.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'QU1_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['QU1_WB'] = P_20['QU1_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from first_20_percent_income_share removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

""" Adding the second 20 highest % from data.worldbank.org
"""
# Importing the data from the csv file
P_20 = pd.read_csv("second_20_percent_income_share.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'QU2_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['QU2_WB'] = P_20['QU2_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from second_20_percent_income_share removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

""" Adding the third 20 highest % from data.worldbank.org
"""
# Importing the data from the csv file
P_20 = pd.read_csv("third_20_percent_income_share.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'QU3_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['QU3_WB'] = P_20['QU3_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from third_20_percent_income_share removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

""" Adding the fourth 20 highest % from data.worldbank.org
"""
# Importing the data from the csv file
P_20 = pd.read_csv("fourth_20_percent_income_share.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'QU4_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['QU4_WB'] = P_20['QU4_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from fourth_20_percent_income_share removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

""" Adding the fifth 20 highest % from data.worldbank.org
"""
# Importing the data from the csv file
P_20 = pd.read_csv("fifth_20_percent_income_share.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'QU5_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['QU5_WB'] = P_20['QU5_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from fifth_20_percent_income_share removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

""" Adding the GDP at market price from data.worldbank.org
"""
# Importing the data from the csv file
P_20 = pd.read_csv("GDP_at_market_prices.csv",
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

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from GDP_at_market_prices removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

"""Adding the GDP growth from data.worldbank.org
"""

# Importing the data from the csv file
P_20 = pd.read_csv("GDP_growth_WB.csv",
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

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from GDP_growth_WB removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

"""Adding the GDP growth from data.worldbank.org
"""

# Importing the data from the csv file
P_20 = pd.read_csv("GDP_PC_WB.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'GDP_PC_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['GDP_PC_WB'] = P_20['GDP_PC_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from GDP_PC_WB removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))


"""Adding the GDP from OECD measures
"""
data = pd.read_csv("GDP_OCDE_countries.csv")

variable_choice = ['MLN_USD', 'USD_CAP']

selected = pd.pivot_table(data, values='Value', index=['LOCATION', 'TIME'],
                          columns=['MEASURE'])[variable_choice].reset_index()
selected.columns = ['code', "year", "GDP_OECD", "GDP_CAP_OECD"]

selected['code'] = selected["code"].astype(str)
selected["year"] = selected["year"].astype(int)
selected["GDP_OECD"] = selected["GDP_OECD"].astype(float)
selected["GDP_CAP_OECD"] = selected["GDP_CAP_OECD"].astype(float)

data_frame = pd.merge(data_frame, selected, how='outer', on=['code', 'year'])

del selected, data

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from GDP_OCDE_countries removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

"""Adding the GDP from OECD measures
"""
data = pd.read_csv("inequalities_OCDE.csv")

variable_choice = ['Gini (market income, before taxes and transfers)',
                   'Gini (disposable income, post taxes and transfers)',
                   'Median disposable income (current prices)',
                   'Palma ratio',
                   'P90/P10 disposable income decile ratio',
                   'P90/P50  disposable income decile ratio',
                   'P50/P10  disposable income decile ratio',
                   'S80/S20 disposable income quintile share',
                   'S90/S10 disposable income decile share']

selected = pd.pivot_table(data, values='Value', index=['LOCATION', 'TIME'], columns=[
    'Measure'])[variable_choice].reset_index()
selected.columns = ['code', "year", "gini_post_taxe_OECD",
                    "gini_before_taxe_OECD", "median_income_OECD", "palma_OECD",
                    "P90/P10_OECD", "P90/P50_OECD", "P50/P10_OECD",
                    "S80/S20_OECD", "S90/S10_OECD"]

selected['code'] = selected["code"].astype(str)
selected["year"] = selected["year"].astype(int)
selected["gini_post_taxe_OECD"] = selected["gini_post_taxe_OECD"].astype(float)
selected["gini_before_taxe_OECD"] = selected[
    "gini_before_taxe_OECD"].astype(float)
selected["median_income_OECD"] = selected["median_income_OECD"].astype(float)
selected["palma_OECD"] = selected["palma_OECD"].astype(float)
selected["P90/P10_OECD"] = selected["P90/P10_OECD"].astype(float)
selected["P90/P50_OECD"] = selected["P90/P50_OECD"].astype(float)
selected["P50/P10_OECD"] = selected["P50/P10_OECD"].astype(float)
selected["S80/S20_OECD"] = selected["S80/S20_OECD"].astype(float)
selected["S90/S10_OECD"] = selected["S90/S10_OECD"].astype(float)

data_frame = pd.merge(data_frame, selected, how='outer', on=['code', 'year'])

del selected, data

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from inequalities_OCDE removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

"""Adding the data of World Income database
"""
data = pd.read_csv('WID_extract.csv', skiprows=1)
selected_cols = ["Country",
                 "Year",
                 "Top 10% income share-including capital gains",
                 "Top 5% income share-including capital gains",
                 "Top 1% income share-including capital gains",
                 "Top 0.5% income share-including capital gains",
                 "Top 0.1% income share-including capital gains",
                 "Top 0.05% income share-including capital gains",
                 "Top 0.01% income share-including capital gains",
                 "National income"
                #  ,
                #  "Top 10% average income",
                #  "Top 5% average income",
                #  "Top 1% average income",
                #  "Top 0.5% average income",
                #  "Top 0.1% average income",
                #  "Top 0.05% average income",
                #  "Top 0.01% average income",
                #  "Bottom 90% average income",
                #  "Top 0.25% average income",
                #  "Top 0.15% average income"
                 ]

data = data[selected_cols]
data.columns = ["country",
                "year",
                "D1_WID",
                "V1_WID",
                "P1_WID",
                "top_0.5_income_share_WID",
                "Pr1_WID",
                "top_0.05_income_share_WID",
                "top_0.01_income_share_WID",
                "national_income_WID"
                # ,
                # "D1_average_WID",
                # "V1_average_WID",
                # "P1_average_WID",
                # "top_0.5_average_income_WID",
                # "Pr_average_WID",
                # "top_0.05_average_WID",
                # "top_0.01_average_WID",
                # "bottom90_average_income_WID",
                # "top_0.25_average_WID",
                # "top_0.15_average_WID"
                ]

data["country"] = data["country"].astype(str)
data["year"] = data["year"].astype(int)
data["D1_WID"] = data["D1_WID"].astype(float)
data["V1_WID"] = data["V1_WID"].astype(float)
data["P1_WID"] = data["P1_WID"].astype(float)
data["top_0.5_income_share_WID"] = data["top_0.5_income_share_WID"].astype(float)
data["Pr1_WID"] = data["Pr1_WID"].astype(float)
data["top_0.05_income_share_WID"] = data["top_0.05_income_share_WID"].astype(float)
data["top_0.01_income_share_WID"] = data["top_0.01_income_share_WID"].astype(float)
data["national_income_WID"] = data["national_income_WID"].astype(float)

data = pd.merge(data, code_country_dict, how='left', on='country')
data_frame = pd.merge(
    data_frame, data, how='outer', on=['code', 'year'])

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from WID-report removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))


"""Adding the data from Penn World Table
"""
df = pd.ExcelFile('GDPs_PWT.xlsx')
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

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from GDPs_PWT removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

data_frame.sort(['code', 'year']).to_csv("income_GDP_data.csv", index=False)
