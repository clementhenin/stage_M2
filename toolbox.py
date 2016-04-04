import pandas as pd
import pylab as plt
import numpy as np
import pdb

"""Ensemble de fonction utile pour le projet. Les donnees sont sous la
forme d'une dataframe pandas avec un double index : code puis annee.
"""


def plot_correlations(data, min_match=20, size_tuple=(15, 15)):
    """Plot the correlations between every variable of the data

    Input : pandas data frame with code, year as index and sorted
    in this order

    Output : graph of correlations
    """
    correlations = data.corr(min_periods=min_match)
    fig = plt.figure(figsize=size_tuple)
    norm = plt.cm.colors.Normalize(vmax=1, vmin=-1)
    plt.imshow(correlations, interpolation='nearest', norm=norm)
    plt.xticks(range(0, len(data.columns)), data.columns, rotation='vertical')
    plt.yticks(
        range(0, len(data.columns)), data.columns, rotation='horizontal')
    plt.colorbar()


def rolling_mean(df, variable, nbr_yrs, threshold, how='centered'):
    """Compute the mean value of a range of time for a time varying range.
    For exemple if variable if growth, the value in 1980 will be the average
    of the growth between 1980 and 1980 + nbr_yrs. Threshlod corresponds to
    the minimum number of non nan values necessary to compute the mean
    (otherwise nan).
    """
    new_frame = pd.DataFrame()
    for country in df.index.levels[0]:
        sel = pd.DataFrame(df.query("code == '" + country + "'")[variable])
        sel['roll_mean'] = float('nan')
        for obs in sel.iterrows():
            idx = obs[0]
            if how == 'futur':
                window = sel.loc[(idx[0], ), variable
                                 ].loc[[idx[1] + i for i in range(nbr_yrs)]]
            if how == 'past':
                window = sel.loc[(idx[0], ), variable
                                 ].loc[[idx[1] + i for i in range(-nbr_yrs + 1, 1)]]
            if how == 'centered':
                if nbr_yrs % 2 == 0:
                    raise ValueError("""Total number of years must be odd for
                                        centered option""")
                window = sel.loc[(idx[0], ), variable
                                 ].loc[[idx[1] + i for i in range(-(nbr_yrs / 2), nbr_yrs / 2 + 1)]]
            if window.notnull().sum() >= threshold:
                val = window.mean()
            else:
                val = float('nan')
            sel.loc[idx, 'roll_mean'] = val
        new_frame = pd.concat([new_frame, sel])
    return new_frame['roll_mean']


def resample(df, period):
    """Resample the frame df to period (in year)

    Input :
    - df : data
    - period : integer : new wanted period

    Output : resampled frame
    """
    df_copy = df.copy().reset_index()
    period = float(period)
    tuples = zip(df_copy['code'],
                 (((df_copy['year'].values) // period) * period) + period / 2.)
    df_copy.index = pd.MultiIndex.from_tuples(tuples)
    df_copy = df_copy.groupby(level=[0, 1]).mean().dropna(how='all')
    del df_copy['year']
    df_copy.index.names = ['code', 'year']
    return df_copy.sort_index().dropna(how='all')


def growth(df, variable, as_rate=False, how='past'):
    """Return the variation of the variable express as the difference
    between a value and the next value divided by the number of years between
    the two.

    If as_rate==True, then it divides the growth by the current value of
    the variable.

    how = ['futur', 'past'] argument decides if the growth is computed
    between t+1 and t ('futur'), or between t and t-1 ('past')
    """
    data = df.copy()
    data.sort_index(level=[0, 1], inplace=True)
    new_frame = pd.DataFrame()
    for country in data.index.levels[0]:
        sel = pd.DataFrame(data.query("code == '" + country + "'")[variable])
        years = np.array([x[1] for x in sel.index.tolist()])
        if sel.shape[0] > 1:
            if how == 'past':
                sel['growth'] = (sel - sel.shift(1))
                sel['growth'] /= years - np.insert(years[:-1], 0, float('nan'))
            elif how == 'futur':
                sel['growth'] = (sel.shift(-1) - sel)
                sel['growth'] /= np.append(years[1:], float('nan')) - years
            if as_rate == True:
                sel['growth'] /= sel[variable]
            new_frame = pd.concat([new_frame, sel])
    return new_frame['growth']


def quartilize_periodwise(data, n_quartiles):
    # pdb.set_trace()
    copy = data.copy().reset_index()
    copy.set_index('year', inplace=True)
    var_names = copy.keys()
    quartiles_thresholds = np.linspace(0, 100, n_quartiles + 1)[:: -1]
    for var in copy.keys():
        copy["qu_" + var] = 0
    for year in set(copy.index):
        for var in [item for item in var_names if item != "code"]:
            try:
                for i in range(n_quartiles):
                    upper_limit = np.percentile(
                        copy.loc[year, var], quartiles_thresholds[i])
                    lower_limit = np.percentile(
                        copy.loc[year, var], quartiles_thresholds[i + 1])
                    if i == 0:
                        ith_qu_bool = copy.loc[year, var].apply(lambda x: x <= upper_limit
                                                                and x >= lower_limit)
                    else:
                        ith_qu_bool = copy.loc[year, var].apply(lambda x: x < upper_limit
                                                                and x >= lower_limit)
                    copy.loc[
                        (year,), "qu_" + var] += ith_qu_bool * (n_quartiles - (i + 1))
            except AttributeError:
                if type(copy.loc[year, var]) in [np.float64, float]:
                    copy.loc[(year, ), var] = 0
                else:
                    raise("Unexpected Error")
            copy.loc[
                (year, ), "qu_" + var] = copy.loc[(year, ), "qu_" + var].astype(int)
    copy.reset_index(inplace=True)
    copy['year'] = copy['year'].astype(int)
    copy.set_index(['code', 'year'], inplace=True)
    copy = copy[["qu_" + var for var in
                 [item for item in var_names if item != "code"]]]
    copy.columns = [item for item in var_names if item != "code"]
    return copy.sort_index()


def quartilize_dataset(data, n_quartiles):
    data_copy = data.copy()
    data_copy = pd.DataFrame(data_copy)
    quartiles_thresholds = np.linspace(0, 100, n_quartiles + 1)[:: -1]
    for var in data_copy.keys():
        data_copy["qu_" + var] = 0
        for i in range(n_quartiles):
            upper_limit = np.percentile(
                data_copy[var], quartiles_thresholds[i])
            lower_limit = np.percentile(
                data_copy[var], quartiles_thresholds[i + 1])
            if i == 0:
                ith_qu_bool = data_copy[var].apply(lambda x: x <= upper_limit
                                                   and x >= lower_limit)
            else:
                ith_qu_bool = data_copy[var].apply(lambda x: x < upper_limit
                                                   and x >= lower_limit)
            data_copy["qu_" + var] += ith_qu_bool * (n_quartiles - (i + 1))
    return data_copy
