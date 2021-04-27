"""
For domain and inventor analysis, update the dictionary with additional data
"""
from lib.default import *

def LoadNewDataset(name):
    """
    Input: name of the folder containing additional excel files

    Create a new patent-domain dictionary from additional data
    """
    new_dict = {}
    files_path = os.path.abspath(name)
    file_list = glob.glob(files_path+'/*')
    #TO BE WRITTEN: a loop
    for file in file_list:
        new_df = pd.read_excel(file,usecols=['Publication numbers','Technology domains'] ,index_col=None)
        new_df = new_df.astype(str)
        try:
            assert('Publication numbers' in new_df.columns)
            assert('Technology domains' in new_df.columns)
        except:
            sys.exit("Please make sure the file ",file," contains Publication numbers and Technology domains")   

        family_list=[]
        family_domains = []
        for index, row in new_df.iterrows():
            fmls = row['Publication numbers'].split('\n')
            domain = row['Technology domains']
            for l in fmls:
                family_list.append(l)
                family_domains.append(domain)
        zipped = zip(family_list, family_domains)
        new_dict.update(dict(zipped))
    return new_dict

def LoadNewDatasetInventor(name):
    """
    Input: name of the folder containing additional excel files

    Create a new patent-inventor dictionary from additional data
    """
    new_dict = {}
    files_path = os.path.abspath(name)
    file_list = glob.glob(files_path+'/*')
    #TO BE WRITTEN: a loop
    for file in file_list:
        new_df = pd.read_excel(file,usecols=['Publication numbers','Inventors'] ,index_col=None)
        new_df = new_df.astype(str)
        try:
            assert('Publication numbers' in new_df.columns)
            assert('Inventors' in new_df.columns)
        except:
            sys.exit("Please make sure the file ",file," contains Publication numbers and Inventors'")

        family_list=[]
        family_inventors = []
        for index, row in new_df.iterrows():
            fmls = row['Publication numbers'].split('\n')
            inventor = row['Inventors']
            for l in fmls:
                family_list.append(l)
                family_inventors.append(inventor)
        zipped = zip(family_list, family_inventors)
        new_dict.update(dict(zipped))
    return new_dict

def UpdateDictionary(dm_dict, new_dict):
    dm_dict.update(new_dict)
    return dm_dict