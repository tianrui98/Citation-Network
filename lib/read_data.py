"""
Read merged and cleaned data in csv or xlsx format.
Check if all relevant columns are in the dataset.
"""
import pandas as pd
import sys

def GetCSV ():
    file_path = input("Enter the path to the csv file (including .csv):\n")
    print("\nReading csv file...")
    df = pd.read_csv(file_path, index_col= 0)
    df = df.astype(str)
    return df

def GetXLSX ():
    file_path = input("Enter the path to the excel file (including .xlsx):\n")
    print("\nReading excel file...")
    df = pd.read_excel(file_path, index_col= 0)
    df = df.astype(str)
    return df

def CheckColumns(df):
    """
    Check if df contains all important columns. 
    User can choose to ignore warnings if the particular analysis does not requires all the columns.
    """
    headers = [
    'Publication numbers',
    'Earliest publication number',
    'Technology domains',
    'Current assignees',
    'Main IPC',
    'Main CPC',
    'Title',
    'Abstract',
    'Earliest publication date',
    'Inventors',
    'Cited patents - Standardized publication number-ALL',
    'Cited patents - Applicant/assignee-ALL',
    'Cited patents - Standardized publication number-EXAMINER',
    'Cited patents - Applicant/assignee-EXAMINER',
    'Cited patents - Standardized publication number-APPLICANT',
    'Cited patents - Applicant/assignee-APPLICANT',
    'Citing patents - Standardized publication number-ALL',
    'Citing patents - Applicant/assignee-ALL',
    'Citing patents - Standardized publication number-EXAMINER',
    'Citing patents - Applicant/assignee-EXAMINER',
    'Citing patents - Standardized publication number-APPLICANT',
    'Citing patents - Applicant/assignee-APPLICANT']
    cols = df.columns
    warnings = False
    for header in headers:
        if header not in cols:
            print(header + " not found in columns")
            warnings = True
    if warnings:
        ignore =  input("Ignore warnings? (Y/N): ")
        if ignore != "Y":
            sys.exit("Please make sure the dataset has relevant columns")

    return None 
