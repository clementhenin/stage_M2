import pandas as pd
import pdb
from scipy.integrate import trapz
import numpy as np
import sys
import math

code_country_dict = pd.read_csv("country_code_list.csv",
                                index_col="country")
COW_dict = pd.read_csv("COW_country_codes.csv",
                       index_col='StateAbb')

VALID_CODES = code_country_dict['code'].tolist()
KNOWN_INVALID_CODES = pd.read_csv("known_invalid_codes.csv",
                                  names=['code'])['code'].tolist()

if __name__ == "__main__":
    try:
        final_file_name = sys.argv[1]
    except IndexError:
        final_file_name = "all_data.csv"
    try:
        barro_option = sys.argv[2]
    except IndexError:
        barro_option = False


def import_from_WB(file_name, var_name, current_frame):
    # Importing the data from the csv file
    d = pd.read_csv(file_name, skiprows=4, index_col=['Country Code'])

    # selects the data and transpose it to the good format
    d = d[[str(item) for item in range(1960, 2016)]].stack().reset_index()
    d.columns = ['code', 'year', var_name]

    # Makes sure the types of the columns are good
    d['code'] = d['code'].astype(str)
    d['year'] = d['year'].astype(int)
    d[var_name] = d[var_name].astype(float)

    current_frame = remove_duplicates_visibly(current_frame, file_name)

    current_frame = pd.merge(
        current_frame, d, how='outer', on=['code', 'year'])

    current_frame = remove_unknown_country(current_frame, file_name)

    return current_frame


def remove_unknown_country(current_frame, file_name):
    # collect list of codes that do not appear in the list of countries
    e = current_frame.query(
        "code not in " + str(VALID_CODES + KNOWN_INVALID_CODES))
    if len(e) > 0:
        print("Warning data from " + file_name + " removed with country codes : ",
              set(e['code']))
    current_frame = current_frame.query("code in " + str(VALID_CODES))
    return current_frame


def remove_duplicates_visibly(current_frame, file_name):
    if current_frame.duplicated(['year', 'code']).sum() == 0:
        return current_frame
    else:
        dupl = current_frame[current_frame.duplicated(['year', 'code'],
                                                      keep=False)]
        print "Duplicates in ", file_name, " will be removed \n"
        print dupl.groupby(['code', 'year']).std() / dupl.groupby(['code', 'year']).mean()
        return current_frame.groupby(['code', 'year'], as_index=False).mean()


# Creates an empty dataset
data_frame = pd.DataFrame(columns=['code', 'year'])

"""Adding the data from data.worldbank.com
"""

files_list = ["10_highest_percent_income_share.csv",
              "10_lowest_percent_income_share.csv",
              "first_20_percent_income_share.csv",
              "second_20_percent_income_share.csv",
              "third_20_percent_income_share.csv",
              "fourth_20_percent_income_share.csv",
              "fifth_20_percent_income_share.csv", "GDP_at_market_prices.csv",
              "GDP_growth_WB.csv", "GDP_PC_WB.csv",
              "governments_consumption_over_GDP.csv",
              "inflation_consumer_price_WB.csv", "fertility_rate.csv",
              "gross_savings_WB.csv", "gross_fixed_capital_formation_WB.csv",
              "GNI_PC_WB.csv",
              "natural_ressources_rent_WB.csv"]

var_list = ["D1_WB", "D9_WB", "QU1_WB", "QU2_WB", "QU3_WB", "QU4_WB",
            "QU5_WB", "GDP_MP_WB", "GDP_growth_WB", "GDP_PC_WB",
            'gov_consumption_WB', 'inflation_WB', 'fertility_WB', "savings_WB",
            "investments_WB", "GNI_PC_WB", "nat_ress_WB"]

for i in range(len(files_list)):
    data_frame = import_from_WB(file_name=files_list[i],
                                var_name=var_list[i],
                                current_frame=data_frame)

"""Adding the data from Deininger and Squire
"""
D_S = pd.read_csv("income_inequality_Deininger_Squire.csv")
data = D_S[['Code', 'Year', 'Gini', 'Quntile 1',
            'Quntile 2', 'Quntile 3', 'Quntile 4', 'Quality']]
data.columns = ['code', 'year', 'gini_DS', 'Q1_DS',
                'Q2_DS', 'Q3_DS', 'Q4_DS', 'quality_DS']

data.loc[:, 'code'] = data['code'].astype(str)
data.loc[:, 'year'] = data['year'].astype(int)
data.loc[:, 'quality_DS'] = data['quality_DS'].astype(str)
data.loc[:, 'gini_DS'] = data['gini_DS'].astype(float) / 100.
data.loc[:, 'Q1_DS'] = data['Q1_DS'].astype(float)
data.loc[:, 'Q2_DS'] = data['Q2_DS'].astype(float)
data.loc[:, 'Q3_DS'] = data['Q3_DS'].astype(float)
data.loc[:, 'Q4_DS'] = data['Q4_DS'].astype(float)

if barro_option:
    accepted_before = len(data[data['quality_DS'] == 'accept'])
    sel = [item in zip(added_obs['code'], added_obs['year'])
           for item in zip(data['code'], data['year'])]
    data.loc[sel, "quality_DS"] = "accept"
    accepted_after = len(data[data['quality_DS'] == 'accept'])
    print accepted_after - accepted_before, " lines added to accept "

data = data[data['quality_DS'] == 'accept']
del data['quality_DS']

data = remove_duplicates_visibly(
    data, "income_inequality_Deininger_Squire")

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

data_frame = remove_unknown_country(
    data_frame, "income_inequality_Deininger_Squire.csv")

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

selected = remove_duplicates_visibly(selected, "GDP_OCDE_countries")

data_frame = pd.merge(
    data_frame, selected, how='outer', on=['code', 'year'])

del selected, data

data_frame = remove_unknown_country(data_frame, "GDP_OCDE_countries.csv")

"""Adding the meseaures of inequality from OECD measures
"""
data = pd.read_csv("inequalities_OCDE.csv")

variable_choice = ['Gini (market income, before taxes and transfers)',
                   'Gini (disposable income, post taxes and transfers)',
                   'P90/P10 disposable income decile ratio',
                   'P90/P50  disposable income decile ratio',
                   'P50/P10  disposable income decile ratio',
                   'S80/S20 disposable income quintile share',
                   'S90/S10 disposable income decile share']

selected = pd.pivot_table(data, values='Value', index=['LOCATION', 'TIME'],
                          columns=['Measure'])[variable_choice].reset_index()
selected.columns = ['code', "year", "gini_post_taxe_OECD",
                    "gini_before_taxe_OECD", "P90/P10_OECD", "P90/P50_OECD",
                    "P50/P10_OECD", "S80/S20_OECD", "S90/S10_OECD"]

selected['code'] = selected["code"].astype(str)
selected["year"] = selected["year"].astype(int)
selected["gini_post_taxe_OECD"] = selected[
    "gini_post_taxe_OECD"].astype(float)
selected["gini_before_taxe_OECD"] = selected[
    "gini_before_taxe_OECD"].astype(float)
selected["P90/P10_OECD"] = selected["P90/P10_OECD"].astype(float)
selected["P90/P50_OECD"] = selected["P90/P50_OECD"].astype(float)
selected["P50/P10_OECD"] = selected["P50/P10_OECD"].astype(float)
selected["S80/S20_OECD"] = selected["S80/S20_OECD"].astype(float)
selected["S90/S10_OECD"] = selected["S90/S10_OECD"].astype(float)

selected = remove_duplicates_visibly(selected, "inequalities_OCDE")

data_frame = pd.merge(
    data_frame, selected, how='outer', on=['code', 'year'])

del selected, data

data_frame = remove_unknown_country(data_frame, "inequalities_OCDE.csv")

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
                 "National income",
                 'Private wealth. Net private wealth.6']

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
                "national_income_WID",
                "K_over_PIB"]

data["country"] = data["country"].astype(str)
data["year"] = data["year"].astype(int)
data["D1_WID"] = data["D1_WID"].astype(float)
data["V1_WID"] = data["V1_WID"].astype(float)
data["P1_WID"] = data["P1_WID"].astype(float)
data["top_0.5_income_share_WID"] = data[
    "top_0.5_income_share_WID"].astype(float)
data["Pr1_WID"] = data["Pr1_WID"].astype(float)
data["top_0.05_income_share_WID"] = data[
    "top_0.05_income_share_WID"].astype(float)
data["top_0.01_income_share_WID"] = data[
    "top_0.01_income_share_WID"].astype(float)
data["national_income_WID"] = data["national_income_WID"].astype(float)
data["K_over_PIB"] = data["K_over_PIB"].astype(float)

data['code'] = data['country'].apply(
    lambda x: code_country_dict.loc[x]['code'])

del data['country']

data = remove_duplicates_visibly(data, "WID_extract")

data_frame = pd.merge(
    data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "WID_extract.csv")

"""Adding the data from Penn World Table
"""
df = pd.ExcelFile('GDPs_PWT.xlsx')
selected_cols = ["countrycode", "year", "rgdpe", "pop"]

data = df.parse("Data")
data = data[selected_cols]

data["pop"] = data['rgdpe'] / data['pop']

data.columns = ["code", "year", "GDP_PWT", "GDP_PC_PWT"]

data["code"] = data["code"].astype(str)
data["year"] = data["year"].astype(int)
data["GDP_PWT"] = data["GDP_PWT"].astype(float)
data["GDP_PC_PWT"] = data["GDP_PC_PWT"].astype(float)


data = remove_duplicates_visibly(data, "GDPs_PWT")

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "GDPs_PWT.csv")

"""Adding the years of schooling from Barro-Lee
"""
# Importing the data from the csv file
data = pd.read_csv("barro_lee_15_MF.csv")

data = data[["WBcode", "year", "yr_sch"]]

# selects the data and transpose it to the good format
data.columns = ["code", 'year', 'years_schooling']

# Makes sure the types of the columns are good
data['code'] = data['code'].astype(str)
data['year'] = data['year'].astype(int)
data['years_schooling'] = data['years_schooling'].astype(float)

data = remove_duplicates_visibly(data, "barro_lee_15_MF")

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "barro_lee_15_MF.csv")

"""Adding the years of secondary schooling for female over 25 from Barro-Lee
"""
# Importing the data from the csv file
data = pd.read_csv("barro_lee_25_female.csv")

data = data[["WBcode", "year", "yr_sch_sec"]]

# selects the data and transpose it to the good format
data.columns = ["code", 'year', 'yrs_sec_schlg_F_25']

# Makes sure the types of the columns are good
data['code'] = data['code'].astype(str)
data['year'] = data['year'].astype(int)
data['yrs_sec_schlg_F_25'] = data['yrs_sec_schlg_F_25'].astype(float)

data = remove_duplicates_visibly(data, "barro_lee_25_female")

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "barro_lee_25_female.csv")

"""Adding the years of schooling for male over 25 from Barro-Lee
"""
# Importing the data from the csv file
data = pd.read_csv("barro_lee_25_male.csv")

data = data[["WBcode", "year", "yr_sch_sec"]]

# selects the data and transpose it to the good format
data.columns = ["code", 'year', 'yrs_sec_schlg_M_25']

# Makes sure the types of the columns are good
data['code'] = data['code'].astype(str)
data['year'] = data['year'].astype(int)
data['yrs_sec_schlg_M_25'] = data['yrs_sec_schlg_M_25'].astype(float)

data = remove_duplicates_visibly(data, "barro_lee_25_male")

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "barro_lee_25_male.csv")

"""Adding the democracy index from PRIO
"""

# Importing the data from the csv file
data = pd.read_csv("democracy_index.csv")

data = data[["code_COW", "year", "democracy_index"]]

data['country'] = data['code_COW'].apply(
    lambda x: COW_dict.loc[x]['StateNme'])
data['code'] = data['country'].apply(
    lambda x: code_country_dict.loc[x]['code'])

data = data[['code', 'year', "democracy_index"]]

# Makes sure the types of the columns are good
data['code'] = data['code'].astype(str)
data['year'] = data['year'].astype(int)
data['democracy_index'] = data['democracy_index'].astype(float)

data = remove_duplicates_visibly(data, "democracy_index")

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "democracy_index.csv")

"""Adding adding dummy continents variables from country_continent_code.csv
"""

# Importing the data from the csv file
data = pd.read_csv("country_continent_code.csv",
                   index_col=['ISO 3166-1 alpha-3'])

data_frame.loc[:, "dummy_africa"] = data_frame['code'].apply(
    lambda x: int(data.loc[x]['continent'] == 'AF'))
data_frame.loc[:, "dummy_south_america"] = data_frame['code'].apply(
    lambda x: int(data.loc[x]['continent'] == 'SA'))

del data

"""Adding the openness from data.worldbank.org
"""

# Importing the data from the csv file
imports = pd.read_csv("imports_good_service_%GDP.csv",
                      skiprows=4, index_col=['Country Code'])
exports = pd.read_csv("exports_good_service_%GDP.csv",
                      skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
imports = imports[[str(item)
                   for item in range(1960, 2016)]].stack().reset_index()
imports.columns = ['code', 'year', 'imports_%GDP']
exports = exports[[str(item)
                   for item in range(1960, 2016)]].stack().reset_index()
exports.columns = ['code', 'year', 'exports_%GDP']

# Makes sure the types of the columns are good
imports['code'] = imports['code'].astype(str)
imports['year'] = imports['year'].astype(int)
imports['imports_%GDP'] = imports['imports_%GDP'].astype(float)
exports['code'] = exports['code'].astype(str)
exports['year'] = exports['year'].astype(int)
exports['exports_%GDP'] = exports['exports_%GDP'].astype(float)

# gathering the two sources of data
openness = pd.merge(imports, exports, how='inner', on=['code', 'year'])

# Computing the opennes ratio
openness.loc[:, "openness_WB"] = openness.loc[:, 'imports_%GDP']
openness.loc[:, "openness_WB"] += openness.loc[:, 'exports_%GDP']
openness.loc[:, "openness_WB"] /= 100.

del openness['imports_%GDP'], openness['exports_%GDP']

data = remove_duplicates_visibly(openness, "openness files")

data_frame = pd.merge(
    data_frame, openness, how='outer', on=['code', 'year'])

del openness, exports, imports

data_frame = remove_unknown_country(data_frame, "openness files")

"""Adding the data of World Income database
"""
data = pd.read_csv('inequality_WIID.csv')
selected_cols = ["Countrycode3", "Year", "Gini", "D1", "D2", "D3", "D4",  "D5", "D6", "D7",
                 "D8", "D9", "Q1", "Q2", "Q3", "Q4", "Q5", "P5", "P95"]

data = data[selected_cols]
data.columns = ["code", "year", "gini_WIID", "D1_WIID", "D2_WIID", "D3_WIID", "D4_WIID",
                "D5_WIID", "D6_WIID", "D7_WIID", "D8_WIID", "D9_WIID",
                "Q1_WIID", "Q2_WIID", "Q3_WIID", "Q4_WIID", "Q5_WIID", "P5_WIID",
                "P95_WIID"]

data["code"] = data["code"].astype(str)
data["year"] = data["year"].astype(int)
data["gini_WIID"] = data["gini_WIID"].astype(float) / 100.
data["D1_WIID"] = data["D1_WIID"].astype(float)
data["D2_WIID"] = data["D2_WIID"].astype(float)
data["D3_WIID"] = data["D3_WIID"].astype(float)
data["D4_WIID"] = data["D4_WIID"].astype(float)
data["D5_WIID"] = data["D5_WIID"].astype(float)
data["D6_WIID"] = data["D6_WIID"].astype(float)
data["D7_WIID"] = data["D7_WIID"].astype(float)
data["D8_WIID"] = data["D8_WIID"].astype(float)
data["D9_WIID"] = data["D9_WIID"].astype(float)
data["Q1_WIID"] = data["Q1_WIID"].astype(float)
data["Q2_WIID"] = data["Q2_WIID"].astype(float)
data["Q3_WIID"] = data["Q3_WIID"].astype(float)
data["Q4_WIID"] = data["Q4_WIID"].astype(float)
data["Q5_WIID"] = data["Q5_WIID"].astype(float)
data["P5_WIID"] = data["P5_WIID"].astype(float)
data["P95_WIID"] = data["P95_WIID"].astype(float)

data = remove_duplicates_visibly(data, "inequality_WIID")

data_frame = pd.merge(
    data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "inequality_WIID.csv")

"""Adding the price level of investment from PWT 7.1
"""
# Importing the data from the csv file
data = pd.read_csv("PWT_71.csv")

data = data[["isocode", "year", "pi"]]

# selects the data and transpose it to the good format
data.columns = ["code", 'year', 'price_level_investment_PWT']

# Makes sure the types of the columns are good
data['code'] = data['code'].astype(str)
data['year'] = data['year'].astype(int)
data['price_level_investment_PWT'] = data[
    'price_level_investment_PWT'].astype(float)

data = remove_duplicates_visibly(data, "PWT_71")

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "PWT_71.csv")

"""Adding total investment and gross national saving from IMF
"""

# import in a pandas frame
data = pd.read_csv("investment_saving_IMF.aspx", delimiter='\t'
                   ).replace('n/a', float('nan')).replace(',', '')

# removing the estimations from IMF
for country in data.iterrows():
    begin_estim = country[1]['Estimates Start After']
    if not math.isnan(begin_estim):
        if begin_estim == 0:
            begin_estim = 1980
        for year in range(int(begin_estim), 2017):
            data.loc[country[0], str(year)] = float('nan')

cols = ['1980', '1981', '1982', '1983', '1984', '1985', '1986',
        '1987', '1988',
        '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996',
        '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004',
        '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012',
        '2013', '2014', '2015', '2016']

data.set_index(u'ISO', inplace=True)
savings = data[data["Subject Descriptor"] == 'Gross national savings'][cols]
invest = data[data["Subject Descriptor"] == 'Total investment'][cols]

savings = savings.stack()
invest = invest.stack()

savings = savings.reset_index()
invest = invest.reset_index()

savings.columns = ['code', 'year', 'savings_IMF']
invest.columns = ['code', 'year', 'invest_IMF']


savings['code'] = savings['code'].astype(str)
savings['year'] = savings['year'].astype(int)
savings['savings_IMF'] = savings['savings_IMF'].apply(
    lambda x: x.replace(',', '')).astype(float)

invest['code'] = invest['code'].astype(str)
invest['year'] = invest['year'].astype(int)
invest['invest_IMF'] = invest['invest_IMF'].apply(
    lambda x: x.replace(',', '')).astype(float)


data_frame = pd.merge(data_frame, savings, how='outer', on=['code', 'year'])
data_frame = pd.merge(data_frame, invest, how='outer', on=['code', 'year'])

del data, invest, savings

data_frame = remove_unknown_country(data_frame, "investment_saving_IMF.csv")

"""Adding the savings rate from OECD measures
"""
data = pd.read_csv("national_savings_rate_OECD.csv", usecols=[0, 5, 6])
data.columns = ["code", 'year', 'savings_OECD']

data['code'] = data["code"].astype(str)
data["year"] = data["year"].astype(int)
data["savings_OECD"] = data["savings_OECD"].astype(float)

selected = remove_duplicates_visibly(data, "national_savings_rate_OECD")

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(
    data_frame, "national_savings_rate_OECD.csv")


"""Adding the data of SWIID 5.0 data
"""
data = pd.read_csv('SWIID_5_0.csv')

data = data.replace('Cape Verde', 'Cabo Verde')
data = data.replace('Congo, Democratic Republic of', 'Congo')
data = data.replace('Congo, Republic of', 'Congo-Brazzaville')
data = data.replace("Korea, Republic of", 'South Korea')
data = data.replace("Kyrgyz Republic", 'Kyrgyzstan')
data = data.replace("Lao", 'Laos')
data = data.replace("Macedonia, FYR", 'Macedonia')
data = data.replace("Cote d'Ivoire", 'Ivory Coast')
data = data.replace("Moldova", 'Republic of Moldova')
data = data.replace("Slovak Republic", 'Slovakia')
data = data.replace("St. Lucia", 'Saint Lucia')
data = data.replace("St. Vincent and the Grenadines", 'Saint Vincent and the Grenadines')
data = data.replace("Syria", 'Syrian Arab Republic')
data = data.replace("Turks and Caicos", 'Turks and Caicos Islands')
data = data.replace("USSR", 'Russian Federation')
data = data.replace("United States", 'United States of America')
data = data.replace("Viet Nam", 'Socialist Republic of Vietnam')
data = data.replace("Yemen, Republic of", 'Republic of Yemen')

data.columns = ["country", "year", "gini_net_SWIID",
                 "gini_market_SWIID", "rel_red_SWIID", "abs_red_SWIID"]

data["country"] = data["country"].astype(str)
data["year"] = data["year"].astype(int)
data["gini_net_SWIID"] = data["gini_net_SWIID"].astype(float) / 100.
data["gini_market_SWIID"] = data["gini_market_SWIID"].astype(float) / 100.
data["rel_red_SWIID"] = data["rel_red_SWIID"].astype(float)
data["abs_red_SWIID"] = data["abs_red_SWIID"].astype(float)

data['code'] = data['country'].apply(
    lambda x: code_country_dict.loc[x]['code'])

del data['country']

data = remove_duplicates_visibly(data, "SWIID_5_0")

data_frame = pd.merge(
    data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "SWIID_5_0.csv")


"""Adding capital income share from TP data
"""
data = pd.read_csv("share_capital_income.csv")
data.columns = ["code", 'year', 'cap_share_income']

data['code'] = data["code"].astype(str)
data["year"] = data["year"].astype(int)
data["cap_share_income"] = data["cap_share_income"].astype(float)

selected = remove_duplicates_visibly(data, "share_capital_income")

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(
    data_frame, "share_capital_income.csv")


"""Interpolate scholling data from 5 years data to yearly data
"""
data_frame.sort_values(['code', 'year'], inplace=True)
data_frame.set_index(['code'], inplace=True)
new_frame = pd.DataFrame()

# extrapolating years of schooling to yearly data
for country in set(data_frame.index.values):
    sel = data_frame.loc[country]
    if sel.shape != (len(data_frame.keys()),):
        try:
            sel.loc[:, 'years_schooling'] = sel[
                'years_schooling'].interpolate()
        except TypeError:
            None
        new_frame = pd.concat([new_frame, sel])
data_frame = new_frame.reset_index().dropna(how='all')


data_frame.sort_values(by=['code', 'year']).to_csv(
    final_file_name, index=False)


# ##########################################################################
# #######################  CREATING NEW VARIABLES ##########################
# ##########################################################################
#
# """Creating a gini variable from the World Income Database data
# """
# share_dict_WID = {"D1_WID": 0.1, "V1_WID": 0.05, "P1_WID": 0.01,
#                   "top_0.5_income_share_WID": 0.005, "Pr1_WID": 0.001,
#                   "top_0.05_income_share_WID": 0.0005,
#                   "top_0.01_income_share_WID": 0.0001}
#
# data_frame.set_index(["year", "code"], inplace=True)
# data_frame['gini_WID'] = float('nan')
# for row in data_frame[share_dict_WID.keys()].dropna(how="all").iterrows():
#     actual_share_list = row[1][~row[1].isnull()].keys().values
#     actual_share_dict = dict(
#         (k, share_dict_WID[k]) for k in actual_share_list)
#     lorentz = pd.DataFrame({"x-%_poorest": (1 - np.array(actual_share_dict.values())),
#                             "share": [100 - row[1][var_name] for var_name in actual_share_dict.keys()]})
#     lorentz.loc[len(lorentz) + 1] = {"share": 0, "x-%_poorest": 0}
#     lorentz.loc[len(lorentz) + 1] = {"share": 100, "x-%_poorest": 1}
#     lorentz = lorentz.sort_values(by="x-%_poorest")
#     G_trapz = 1 - 2 * \
#         trapz(lorentz["share"].values / 100.,
#               lorentz["x-%_poorest"].values)
#     data_frame.set_value((row[0][0], row[0][1]), 'gini_WID', G_trapz)
#
# """Creating a gini variable from the World Bank data
# """
# share_dict_WB = {'D1_WB': 0.1, 'cum_QU1_WB': 0.2, 'cum_QU2_WB': 0.4,
#                  'cum_QU3_WB': 0.6, 'cum_QU4_WB': 0.8, 'cum_QU5_WB': 1}
#
# for i in range(1, 6):
#     data_frame["cum_QU" + str(i) + "_WB"] = sum(data_frame["QU" + str(k) + "_WB"]
#                                                 for k in range(1, i + 1))
#
# data_frame['gini_WB'] = float('nan')
# for row in data_frame[share_dict_WB.keys()].dropna(how="all").iterrows():
#     actual_share_list = row[1][~row[1].isnull()].keys().values
#     actual_share_dict = dict(
#         (k, share_dict_WB[k]) for k in actual_share_list)
#     lorentz = pd.DataFrame({"x-%_poorest": (1 - np.array(actual_share_dict.values())),
#                             "share": [100 - row[1][var_name] for var_name in actual_share_dict.keys()]})
#     lorentz.loc[len(lorentz) + 1] = {"share": 0, "x-%_poorest": 0}
#     lorentz = lorentz.sort_values(by="x-%_poorest")
#     G_trapz = 1 - 2 * \
#         trapz(lorentz["share"].values / 100.,
#               lorentz["x-%_poorest"].values)
#     data_frame.set_value((row[0][0], row[0][1]), 'gini_WB', G_trapz)
#
# data_frame = data_frame.reset_index()
#
# for i in range(1, 6):
#     del data_frame["cum_QU" + str(i) + "_WB"]
#
# """Sorting and saving the data
# """
