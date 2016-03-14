import pandas as pd
import numpy as np

# importing the data
data = pd.read_csv('all_data.csv', index_col=['code', 'year'])

# suppress outliers values of saving data
data = data[(data['savings_IMF'].apply(np.absolute) < 200).values + (data['savings_IMF'].isnull()).values]


# create groups of variables and merge them together to increse the data availability
rich_share_var = ["D1_WB", "QU1_WB", "D9_WIID", "Q5_WIID", "D1_WID", "V1_WID", "P1_WID",
"top_0.5_income_share_WID", "Pr1_WID", "top_0.05_income_share_WID", "top_0.01_income_share_WID",
"P90/P10_OECD", "P90/P50_OECD", "P50/P10_OECD", "S80/S20_OECD", "S90/S10_OECD"]
ginis = ["gini_DS", "gini_before_taxe_OECD", "gini_WIID"]
GDP_PC_var = ["GDP_PC_WB", "GDP_PC_PWT"]
savings = ["savings_WB", "savings_OECD", "savings_IMF"]
investments = ["investments_WB", "invest_IMF"]

data['rich_share'] = data[rich_share_var].mean(axis=1)
data['GDP_PC'] = data[GDP_PC_var].mean(axis=1)
data['savings'] = data[savings].mean(axis=1)
data['investments'] = data[investments].mean(axis=1)
data['gini'] = data[ginis].mean(axis=1)


# we limit ourselves to a subset of variables to have as much couple country/period
all_variable = ['GDP_growth_WB', "openness_WB", "investments", "years_schooling", "savings", 'gini',
                "price_level_investment_PWT", "gov_consumption_WB", "inflation_WB", "fertility_WB",
                'rich_share', 'GDP_PC']
dataset = data[all_variable]
dataset = dataset.dropna(how='all')


# making linear interpolation of years of schooling data to artificially increase the number of points
country = np.random.choice(dataset.index.levels[0])
dataset['years_schooling'].loc[country].interpolate().plot(marker='o')
dataset['years_schooling'].dropna().loc[country].plot(marker='o')
dataset.reset_index(inplace=True)
dataset.sort_values(['code', 'year'], inplace=True)
dataset.set_index(['code'], inplace=True)
new_frame = pd.DataFrame()
for country in set(dataset.index.values):
    sel = dataset.loc[country]
    if sel.shape != (len(all_variable) + 1,):
        try:
            sel.loc[:, 'years_schooling'] = sel['years_schooling'].interpolate()
        except TypeError:
            None
        new_frame = pd.concat([new_frame, sel])
dataset = new_frame.reset_index().set_index(['code', 'year'])


dataset = dataset.dropna(how='any')

dataset.to_csv("frankeinstein.csv")
