"""
This module contains functions to create an empty citation matrix, a patent-domain dictionary, save and load it, and 
use the dictionary to match patents to their tech domains, and save the result to the matrix. Those patents without domain information
are saved to txt files. User can upload these files to the online database and obtain domain information.
"""
from lib.default import *

#Create empty matrix
def CreateMatrix ():
    """
    Create empty matrix for domain analysis
    """
    matrix = {}
    for dm1 in dms_ls:
        matrix[dm1]={}
        for dm2 in dms_ls:
            matrix[dm1][dm2] = 0
    return matrix
#%% Create Patent-Domain Dictionary based on current dataset. Save in a folder. 

def CreateDomainDictionary (df):
    family_list=[]
    family_domains = []

    for i in range(len(df)):
        fmls = df.loc[i,'Publication numbers'].split('\n')
        domain = df.loc[i,'Technology domains']
        for l in fmls:
            member_patent = l.split(' ')[0]
            family_list.append(member_patent)
            family_domains.append(domain)

    zipped = zip(family_list, family_domains)
    dm_dict = dict(zipped)

    assert(len(dm_dict.keys()) == len(set(family_list)))

    return dm_dict

def SaveDomainDictionary(dm_dict,save_path):
    path = str(save_path) + '/' + 'DomainDictionary_'+ date+'.pkl'
    f = open(path,"wb")
    pickle.dump(dm_dict,f)
    f.close()

    return None

#To load the dictionary:

def LoadDomainDictionary(path):
    file_to_read = open(path, "rb")
    loaded_dictionary = pickle.load(file_to_read)
    return loaded_dictionary

#%% Find the domain/assignee of patents

#Domain
def MatchExistingPatents (df,dm_dict,matrix,endyear, normalize):
    #Create a dictionary for storing the citation counts of each domain
    domain_count = {}
    for dm in dms_ls:
        domain_count[dm]= 0

    exist_pt = dm_dict.keys()
    all_unknowns = []

    for i in range(len(df)):
        own_domains = df.loc[i,'Technology domains'].split('\n')
        cited_domains=[]
        unknown_patents = []
        known_patents = []
        cited_ls = df.loc[i,'Cited patents - Standardized publication number']
        cited_items_raw = cited_ls.split('\n')
        cited_items_trimmed =[]
    
        for item in cited_items_raw:
            cited_items_trimmed.append(item.split(';')[0])
            
        for pt in cited_items_trimmed:
            
            if pt in exist_pt:
                for dm in dm_dict[pt].split('\n'):
                    cited_domains.append(dm)
                known_patents.append(pt)
            else:
                unknown_patents.append(pt)
               
        cd_uq = list(set(cited_domains))
        unknown_uq =list(set(unknown_patents))
        all_unknowns.append(unknown_uq)

        #a copy of df is created to avoid SettingWithCopyWarning
        df = df.copy()
        df.loc[i, 'unknown_patents_domain'] = ','.join(unknown_uq)
        
        if normalize == "Y":
            year = df.loc[i,'datetime'].year
            denominator = float(endyear- year) +1.0
        else:
            denominator = 1.0

        #Add to the Matrix
        for dm in own_domains:
            if dm != 'nan':
                #if one patent family has multiple domains, add one count/denominator to each domain
                domain_count[dm] += 1/denominator 
                if (len(cd_uq) >0) & (cd_uq != 'nan'):
                    for cd in cd_uq:
                        if cd != 'nan':
                            matrix[dm][cd] += 1/denominator
        
    unknowns = list(set([item for sublist in all_unknowns for item in sublist]))
    return (df,unknowns, matrix, domain_count)

def SaveUnknownPatents (unknown,save_path):
    #make multiple documents each 46k long
    
    chunks = [unknown[x:x+46000] for x in range(0, len(unknown), 46000)]
    
    folder_path = save_path + '/' + 'UnknownPatents_'+date
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for c in range(len(chunks)): 
        path = folder_path +'/'+ str(c)+ '.txt'
        with open(path, 'w') as f:
            for item in chunks[c]:
                f.write(item + "\n")
                
    return None


def SaveDomainCount(domain_count,save_path):
    field = pd.DataFrame(tech_fields, index = ['field']).T
    domain_count_df = pd.DataFrame(domain_count, index = ['count']).T
    result = pd.concat([field, domain_count_df], axis=1, join='outer')
    result.reset_index(level=0, inplace=True)
    result = result.rename(columns = {'index': 'id'})
    path = save_path + '/' + 'node_list_' + date+'.xlsx'
    result.to_excel(path)
    return None
