import pandas as pd

year = '2010'

IMF_data_pure = pd.read_csv("IMF_trade_data.csv", usecols=['\xef\xbb\xbf"Country Name"',
                                                  'Indicator Name',
                                                  "Counterpart Country Name",
                                                  'Attribute', year])

IMF_data = IMF_data_pure[IMF_data_pure['Attribute'] == 'Value']
IMF_data = IMF_data[IMF_data['Indicator Name'] ==
                    'Goods, Value of Exports, Free on board (FOB), US Dollars']
IMF_data = IMF_data[
    ['\xef\xbb\xbf"Country Name"', "Counterpart Country Name", '2010']]
IMF_data.columns = ["country", "counterpart", "2010"]
IMF_data.set_index(['country', 'counterpart'], inplace=True)

data = IMF_data.astype(float).groupby(level=[0, 1]).mean().unstack()
