import pandas as pd


def get_emr3d1():
    xlsx = pd.ExcelFile('data/EMR-Blood.xlsx')
    sheet1 = xlsx.parse(0)
    sheet1.set_index("Key", inplace=True)

    variables1 = ["K","WBC","Hgb"]
    EMR3d1 = sheet1.loc[:, variables1].values
    return EMR3d1, variables1