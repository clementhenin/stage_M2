import pandas as pd
from os import listdir
from os.path import isfile, join

xls_data = [f for f in listdir('.') if isfile(join('.', f))]

for i, xls_file in enumerate(xls_data):
    if xls_file[-4:] == '.xls':
        df = pd.ExcelFile(xls_file)
        for sheet in df.sheet_names:
            data = df.parse(sheet, header=None)
            name = "csv_data/" + xls_file.replace("TableauxGraphiques.xls", "")
            name += "_" + sheet + ".csv"
            for i in range(len(data)):
                if (type(data[data.keys()[0]][i]) == str
                        or type(data[data.keys()[0]][i]) == unicode):
                    try:
                        name = "csv_data/" + data[data.keys()[0]][i]
                        data.dropna(how='all').to_csv(name[:100],
                                                      encoding='utf-8',
                                                      index=False,
                                                      header=False)
                        break
                    except:
                        None
