import pandas as pd

data = pd.read_csv("direct_investment_IMF_data.csv")
country_code_dict = pd.read_csv("../data_source/country_continent_code.csv",
                                index_col="country",
                                # dtype={'\xef\xbb\xbf"Country Name"':str,
                                #         'Country Code':str,
                                #         'Indicator Name':str,
                                #         'Indicator Code':str,
                                #         'Counterpart Country Name':str,
                                #         'Counterpart Country Code':str,
                                #         'Attribute':str,
                                #         '2008':float,
                                #         '2009':float,
                                #         '2010':float,
                                #         '2011':float,
                                #         '2012':float,
                                #         '2013':float,
                                #         '2014':float,
                                #         'Unnamed: 14':str}
                                       )


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
data['counterpart_country'] = data['counterpart_country'].apply(retrieve_name)

data = pd.concat([pd.merge(data, country_code_dict, left_on='country',
                           right_index=True, how='right'),
                  pd.merge(data, country_code_dict, left_on='country',
                           right_on="Full english country name", how='right')],
                 axis=0)

data = data[['Indicator Name',
             'counterpart_country', 'Attribute',
             '2008', '2009', '2010', '2011', '2012', '2013', '2014',
             'ISO 3166-1 alpha-3']]

data.columns = ['Indicator Name',
                'counterpart_country', 'Attribute',
                '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                'code']

data = pd.concat([pd.merge(data, country_code_dict, left_on='counterpart_country',
                           right_index=True, how='right'),
                  pd.merge(data, country_code_dict, left_on='counterpart_country',
                           right_on="Full english country name", how='right')],
                 axis=0)

data = data[['Indicator Name', 'Attribute', '2008',
             '2009', '2010', '2011', '2012', '2013', '2014', 'code',
             'ISO 3166-1 alpha-3']]

data.columns = ['Indicator Name', 'Attribute', '2008',
                '2009', '2010', '2011', '2012', '2013', '2014', 'code',
                'counterpart_code']

data.dropna(how='all',
            subset=['Indicator Name', 'Attribute',
                    '2008', '2009', '2010', '2011', '2012', '2013', '2014'],
            inplace=True)

# data = data.groupby(['Indicator Name', 'Attribute', 'code', 'counterpart_code'],
#                     as_index=False).mean()

# data["code"] = data['country'].apply(lambda x: country_code_dict.loc[x])
# data["counterpart_code"] = data['counterpart_country'].apply(lambda x: country_code_dict.loc[x])

inward_DI = data[data['Indicator Name'] ==
                 'Inward Direct Investment Positions, US Dollars']
outward_DI = data[data['Indicator Name'] ==
                  'Outward Direct Investment Positions, US Dollars']

inward_DI_2010 = inward_DI[["code",
                            "counterpart_code",
                            "Attribute",
                            '2010']]

outward_DI_2010 = outward_DI[["code", "counterpart_code",
                              "Attribute", '2010']]

inward_DI_2010 = inward_DI_2010[inward_DI_2010["Attribute"] == 'Value']
outward_DI_2010 = outward_DI_2010[outward_DI_2010["Attribute"] == 'Value']

inward_DI_2010 = inward_DI_2010[["code",
                                 'counterpart_code',
                                 '2010']]
outward_DI_2010 = outward_DI_2010[["code",
                                   'counterpart_code',
                                   '2010']]

inward_DI_2010.set_index(["code", "counterpart_code"], inplace=True)
outward_DI_2010.set_index(["code", "counterpart_code"], inplace=True)

inward_DI_2010 = inward_DI_2010.astype(float)
outward_DI_2010 = outward_DI_2010.astype(float)

inward_DI_2010 = inward_DI_2010.groupby(level=[0,1]).mean()
outward_DI_2010 = outward_DI_2010.groupby(level=[0,1]).mean()
