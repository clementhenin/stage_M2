import pandas as pd

data = pd.read_csv("direct_investment_IMF_data.csv")
country_code_dict = pd.read_csv("../data_source/country_continent_code.csv",
                                index_col="country")
def retrieve_name(bad_format):
    return " ".join(bad_format.split(', ')[::-1])


# data.replace("Afghanistan, Islamic Republic of", "Afghanistan", inplace=True)
# data.replace("Armenia, Republic of", "Armenia", inplace=True)
# data.replace("Azerbaijan, Republic of", "Azerbaijan", inplace=True)
# data.replace("Bahamas, The", "Bahamas", inplace=True)
# data.replace("", "Armenia", inplace=True)
# data.replace("", "Armenia", inplace=True)
# data.replace("", "Armenia", inplace=True)
# data.replace("", "Armenia", inplace=True)
# data.replace("", "Armenia", inplace=True)
# data.replace("", "Armenia", inplace=True)
# data.replace("", "Armenia", inplace=True)
# data.replace("", "Armenia", inplace=True)

data.columns = ["country",
                "'Country Code'",
                'Indicator Name',
                'Indicator Code',
                'counterpart_country',
                'Counterpart Country Code',
                'Attribute',
                '2008',
                '2009',
                '2010',
                '2011',
                '2012',
                '2013',
                '2014',
                'Unnamed: 14']

data['country'] = data['country'].apply(retrieve_name)

# data["code"] = data['country'].apply(lambda x: country_code_dict.loc[x])
# data["counterpart_code"] = data['counterpart_country'].apply(lambda x: country_code_dict.loc[x])

inward_DI = data[data['Indicator Name'] ==
                 'Inward Direct Investment Positions, US Dollars']
outward_DI = data[data['Indicator Name'] ==
                  'Outward Direct Investment Positions, US Dollars']

inward_DI_2010 = inward_DI[["country", "counterpart_country",
                            "Attribute", '2010']]

outward_DI_2010 = outward_DI[["country", "counterpart_country",
                              "Attribute", '2010']]

inward_DI_2010 = inward_DI_2010[inward_DI_2010["Attribute"] == 'Value']
outward_DI_2010 = outward_DI_2010[outward_DI_2010["Attribute"] == 'Value']

inward_DI_2010 = inward_DI_2010[["country",
                                 'counterpart_country',
                                 '2010']]
outward_DI_2010 = outward_DI_2010[["country",
                                   'counterpart_country',
                                   '2010']]

inward_DI_2010.set_index(["country", "counterpart_country"], inplace=True)
outward_DI_2010.set_index(["country", "counterpart_country"], inplace=True)
