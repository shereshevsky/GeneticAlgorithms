import pandas as pd


def get_eu_measurments():
    xlsx = pd.ExcelFile('data/European Measurements.xlsx')
    sheet1 = xlsx.parse(3)  # Note the other datasets in the file.
    variables = ["Month", "Avg. Likes"]
    data = sheet1.loc[:, variables].values
    return data
