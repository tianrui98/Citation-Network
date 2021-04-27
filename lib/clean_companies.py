"""
This module contains functions to Change the subsidiary company's name to its parent company,
Or standardize the alternative names of a company.
User can modify the parent-subsidiary list under the folder "data". The module will read
the list only from that excel sheet.
"""
from lib.default import *

def CreateCompaniesDict ():
    """
    Convert the data/parent_subsidiary.xlsx excel sheet to dictionary
    company dictionary: key = subsidiary, value = parent
    """
    #all outputs will be saved to the current folder
    path = "data/parent_subsidiary.xlsx"
    companies = pd.read_excel (path, index_col = None)

    companies_dict = {}
    for index, row in companies.iterrows():
        parent = row[0]
        for i in range(1,row.count()) :
            companies_dict [row[i]] = parent
    return companies_dict

def ChangeSubsidiaryNames (cell, companies_dict):
    """
    Replace the subsidiary name with parent name

    Input: company name (string)

    Return: new name (string)
    """
    if type(cell) == float:
        return ''
    else:
        companies = cell.split('\n')
        for company_name in companies:
            if company_name in companies_dict.keys():
                parent = companies_dict[company_name]
                cell = cell.replace(company_name, parent)
        return cell

def ChangeSubsidiaryNamesDF (df):
    """
    Perform the name change to applicable columns

    Return: updated dataframe
    """

    companies_dict = CreateCompaniesDict ()
    for col in df.columns:
        if 'assignee' in col:
            df[col]=df[col].apply(lambda x: ChangeSubsidiaryNames(x,companies_dict))
    return df

def test_change_company_names(df_path):
    df = pd.read_csv(df_path)
    alipay = df.loc[df['Current assignees'] == "ALIPAY INFORMATION TECHNOLOGY",]
    assert(len(alipay) > 0)
    df = df.astype('str')
    new_df = ChangeSubsidiaryNamesDF (df)
    alipay = new_df.loc[df['Current assignees'] == "ALIPAY INFORMATION TECHNOLOGY",]
    assert(len(alipay) ==0 )