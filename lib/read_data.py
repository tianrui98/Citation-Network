"""
Read merged and cleaned data in csv or xlsx format.
Check if all relevant columns are in the dataset.
"""
from lib.default import *
def GetCSV (file_path):
    print("\nReading csv file...")
    df = pd.read_csv(file_path, index_col= 0)
    df = df.astype(str)
    return df

def GetXLSX (file_path):
    print("\nReading excel file...")
    df = pd.read_excel(file_path, index_col= 0)
    df = df.astype(str)
    return df

def CheckColumns(df):
    """
    Check if df contains all important columns. 
    User can choose to ignore warnings if the particular analysis does not requires all the columns.
    """
    important_headers = [
    'Publication numbers',
    'Earliest publication number',
    'Technology domains',
    'Current assignees', 
    'Earliest publication date',
    'Cited patents - Standardized publication number',
    'Cited patents - Applicant/assignee',
    ]

    headers = [
    'Main IPC',
    'Main CPC',
    'Title',
    'Abstract',
    'Inventors',
    'Cited patents - Standardized publication number-EXAMINER',
    'Cited patents - Applicant/assignee-EXAMINER',
    'Cited patents - Standardized publication number-APPLICANT',
    'Cited patents - Applicant/assignee-APPLICANT',
    'Citing patents - Standardized publication number',
    'Citing patents - Applicant/assignee',
    'Citing patents - Standardized publication number-EXAMINER',
    'Citing patents - Applicant/assignee-EXAMINER',
    'Citing patents - Standardized publication number-APPLICANT',
    'Citing patents - Applicant/assignee-APPLICANT']

    cols = df.columns
    warnings = False
    #Important headers should all be present in the dataset
    for header in important_headers:
        if header not in important_headers:
            sys.exit("ERROR: ", header + " not found in columns")
    #Optional headers are necessary only for certain analysis
    for header in headers:
        if header not in cols:
            print("WARNING: ",header + " not found in columns")
            warnings = True
    if warnings:
        ignore =  input("Ignore warnings? (Y/N): ").strip().upper()
        if ignore != "Y":
            sys.exit("Please make sure the dataset has relevant columns")

    return None 

def AddDatetime(df):
    """
    add a "datetime" column to df if it does not already exists
    """
    if 'datetime' not in df.columns:
        df['datetime'] = df['Earliest publication date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    else:
        if type(df['datetime'][0]) != datetime:
            df['datetime'] = df['Earliest publication date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    return df