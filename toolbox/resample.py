import pandas as pd


def resample(df, period):
    """Resample the frame df to period (in year)

    Input :
    -df : dataframe pandas with no index the time dimension exist as a year
        columns (column of integer)
    - period : integer : new wanted period

    Output : resampled frame
    """
    pdb.set_trace()
    period = float(period)
    tuples = zip(df['code'],
                 ((df['year'].values + period / 2.) // period) * period)
    df_copy = df.copy()
    df_copy.index = pd.MultiIndex.from_tuples(tuples)
    df_copy = df_copy.groupby(level=[0, 1]).mean().dropna(how='all')
    del df_copy['year']
    return df_copy
