import pandas as pd
import pdb
import numpy as np

code_country_dict = pd.read_csv("../data_source/country_code_list.csv",
                                index_col="country")
COW_dict = pd.read_csv("../data_source/COW_country_codes.csv",
                       index_col='StateAbb')

VALID_CODES = code_country_dict['code'].tolist()
KNOWN_INVALID_CODES = pd.read_csv("../data_source/known_invalid_codes.csv",
                                  names=['code'])['code'].tolist()

# if __name__ == "__main__":
#     try:
#         final_file_name = sys.argv[1]
#     except IndexError:
#         final_file_name = "all_data.csv"
#     try:
#         barro_option = sys.argv[2]
#     except IndexError:
#         barro_option = False


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


"""Adding the data of SWIID 5.0 data
"""
data = pd.read_csv('../data_source/SWIID_5_0.csv')

variables = ["code", "year", "gini_net_SWIID"]

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
    data_frame, data[variables], how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "SWIID_5_0.csv")

"""Adding the data of infant mortality from WHO
"""
data = pd.read_csv("infant_death_WHO_global_health_estimates.csv",
usecols=['Country', 'Year', 'Infant mortality rate (probability of dying between birth and age 1 per 1000 live births)'])

data.columns = ['country', 'year', 'infant_mortality']

data["infant_mortality"] = data["infant_mortality"
                               ].apply(lambda x: float(x.split(' ')[0]))

data["country"] = data["country"].astype(str)
data["year"] = data["year"].astype(int)
data["infant_mortality"] = data["infant_mortality"].astype(float)


data = data.replace("Bolivia (Plurinational State of)", 'Bolivia')
data = data.replace("Cote d'Ivoire", 'Ivory Coast')
data = data.replace("Democratic People's Republic of Korea", 'North Korea')
data = data.replace('Democratic Republic of the Congo', 'Congo')
data = data.replace("Iran (Islamic Republic of)", 'Iran')
data = data.replace("Lao People's Democratic Republic", 'Laos')
data = data.replace("Republic of Korea", 'South Korea')

data = data.query("country != 'Micronesia (Federated States of)'")

data = data.replace("The former Yugoslav republic of Macedonia", 'Macedonia')
data = data.replace("United Kingdom of Great Britain and Northern Ireland", 'United Kingdom')
data = data.replace("United Republic of Tanzania", 'Tanzania')
data = data.replace("Venezuela (Bolivarian Republic of)", 'Venezuela')
data = data.replace("Viet Nam", 'Socialist Republic of Vietnam')
data = data.replace("Yemen", 'Republic of Yemen')

data['code'] = data['country'].apply(
    lambda x: code_country_dict.loc[x]['code'])

del data['country']

data = remove_duplicates_visibly(data, "infant_death_WHO_global_health_estimates")

data_frame = pd.merge(
    data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "infant_death_WHO_global_health_estimates.csv")


"""Adding the data of quintiles from WIID
"""
data = pd.read_csv("wiid_quintiles.csv",
usecols=['Countrycode3', 'Year', 'D1', 'D10'])

data.columns = ['code', 'year', 'D1', 'D10']

data["code"] = data["code"].astype(str)
data["year"] = data["year"].astype(int)
data["D10/D1"] = data["D10"].astype(float) / data["D1"].astype(float)
del data["D1"],  data['D10']


data = remove_duplicates_visibly(data, "wiid_quintiles")

data_frame = pd.merge(
    data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "wiid_quintiles.csv")


"""Adding the data of mortality rate from OECD
"""
data = pd.read_csv("infant_mortality_rate_OECD.csv",
usecols=['LOCATION', 'TIME', 'Value'])

data.columns = ['code', 'year', 'infant_mortality_OECD']

data["code"] = data["code"].astype(str)
data["year"] = data["year"].astype(int)
data["infant_mortality_OECD"] = data["infant_mortality_OECD"].astype(float)
data['OECD_dummy'] = 1

data = remove_duplicates_visibly(data, "infant_mortality_rate_OECD")

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "infant_mortality_rate_OECD.csv")


"""Adding the rate of homicide from UN
"""
data = pd.read_csv("homicide_rate_UN.csv",
usecols=['Country or Area', 'Year', 'Rate'])

data.columns = ['country', 'year', 'homicide_rate']

data["country"] = data["country"].astype(str)
data["year"] = data["year"].astype(int)
data["homicide_rate"] = data["homicide_rate"].astype(float)



data = data.replace("Bolivia (Plurinational State of)", 'Bolivia')
data = data.replace("British Virgin Islands", 'Virgin Islands')
data = data.replace("Cape Verde", 'Cabo Verde')
data = data.replace("Cote d'Ivoire", 'Ivory Coast')
data = data.replace("Hong Kong Special Administrative Region of China", 'Hong Kong')
data = data.replace("Libyan Arab Jamahiriya", 'Libya')
data = data.replace("Democratic People's Republic of Korea", 'North Korea')
data = data.replace('Democratic Republic of the Congo', 'Congo')
data = data.replace("Iran (Islamic Republic of)", 'Iran')
data = data.replace("Lao People's Democratic Republic", 'Laos')
data = data.replace("Republic of Korea", 'South Korea')

data = data.query("country != 'Micronesia (Federated States of)'")
data = data.query("country != 'Occupied Palestinian Territory'")


data = data.replace("The former Yugoslav republic of Macedonia", 'Macedonia')
data = data.replace("United Kingdom of Great Britain and Northern Ireland", 'United Kingdom')
data = data.replace("United Republic of Tanzania", 'Tanzania')
data = data.replace("Venezuela (Bolivarian Republic of)", 'Venezuela')
data = data.replace("Viet Nam", 'Socialist Republic of Vietnam')
data = data.replace("Yemen", 'Republic of Yemen')
data = data.replace("Macao Special Administrative Region of China", 'Macao')
data = data.replace("The former Yugoslav Republic of Macedonia", 'Macedonia')
data = data.replace("United States Virgin Islands", 'Virgin Islands')
data = data.replace("Bolivia", 'Bolivia')
data = data.replace("Bolivia", 'Bolivia')
data = data.replace("Bolivia", 'Bolivia')
data = data.replace("Bolivia", 'Bolivia')



data['code'] = data['country'].apply(
    lambda x: code_country_dict.loc[x]['code'])

del data['country']

data = remove_duplicates_visibly(data, "homicide_rate_UN")

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

del data

data_frame = remove_unknown_country(data_frame, "homicide_rate_UN.csv")

data_frame.sort_values(by=['code', 'year']).to_csv(
    "wilkinson_database.csv", index=False)
