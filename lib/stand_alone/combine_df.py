"""
combine two datasets: both must have "Earliest publication number" column
"""
import numpy as np
import pandas as pd
import glob
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def CombineCSV (df1_path, df2_path, save_path, save_name, additional_column):

    df1=pd.read_csv(df1_path)
    df1 = df1.astype(str)

    #Select the column from df2 to be joined to df1
    df2 =pd.read_csv(df2_path)
    df2= df2[["Earliest publication number", additional_column]]
    df2 = df2.astype(str)

    #Merge on publication numbers
    df3 = df1.merge(df2, on = "Earliest publication number", how = 'inner')

    #Replace 'nan' value with empty string
    def strip_code (text):
        if text == 'nan':
            return ""
        elif type(text) == float:
            return ""
        elif '\n' in text:
            return text.split('\n')[1]
        else:
            return text

    df3['Abstract']= df3['Abstract'].apply(strip_code)
    df3['Title'] = df3['Title'].apply(strip_code)

    path = save_path + "/" + save_name + ".csv"
    df3.to_csv(path)

if __name__ == "__main__":

    df1_path = input("Enter the path to the base dataset:\n")
    df2_path = input("Enter the path to the new dataset:\n")
    save_path = input("Enter the path to output folder:\n")
    save_name = input("Enter the name of the output file (without extension):\n")
    additional_column = input("Enter ONE column from the new dataset to be added to the base dataset:\n")
    CombineCSV (df1_path, df2_path, save_path, save_name, additional_column)