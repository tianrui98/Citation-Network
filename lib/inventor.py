"""
This module contains functions to create a patent-inventor dictionary, save and load it, and 
use the dictionary to match patents to their inventors. Those patents without inventor information
are saved to txt files. User can upload these files to the online database and obtain inventor information.
"""
from lib.default import *

def CreateInventorMatrix (df, setting = None):
    """
    Creates empty matrix for inventor analysis
    """
    matrix = {}
    inventors_dict = {}
    inventors= []
    for index, row in df.iterrows():   
        inventor_list = row['Inventors'].split('\n')
        if inventor_list[0] != 'nan':
            for a in inventor_list:
                citation = len(row['Citing patents - Standardized publication number'].split('\n'))
                if a not in inventors_dict.keys():
                    inventors_dict[a] = [citation]
                    inventors.append(a)
                else:
                    inventors_dict[a].append(citation)
                    inventors.append(a)
    
    if setting == None:
        number = int(input("How many top patent inventors (based on the number of forward citations) do you want to add to the analysis?\n"))
        parameters = "Top inventors chosen: {0}. ".format(str(number))
        inventors_count = Counter(inventors)
        top_inventors = sorted(inventors_count, key = inventors_count.get, reverse = True) [0:number]
        chosen = []
        extra =  input("Do you want to add more inventors based on other criteria? (Y/N): ")

        while extra == "Y":
            print("\nThe program will select the inventors who have at least K% of their portfolio cited by at least N patents ") 
            K = int(input("Enter K: "))/100
            N = int(input("Enter N: "))
            chosen = []
            for a in inventors_dict.keys():
                counter =0
                citations = sorted(inventors_dict[a],reverse = True)
                length = len(citations)
                for c in citations:
                    if counter/length < K:
                        if c >= N:
                            counter += 1
                    else:
                        chosen.append(a)
                        break
            proceed = input(str(len(chosen)) + " inventors have been selected. Proceed to add them to the matrix? (Y/N): ")        
            if proceed == "Y":
                extra = "N"
                parameters += "     Plus additional {2} inventors whose {0} percent of portfolio cited by at least {1} patents.\n".format(str(K*100), str(N),str(len(chosen)))
            else:
                print("Adjust the parameters.\n")

        #save parameters for other inventor analysis
        save_setting = input ("Do you want to save the parameters for other inventor analysis? (Y/N): ")
        if save_setting == "Y":
            setting = {}
            setting["top_inventors_number"] = number
            if "K" in locals():
                setting["extra_parameters"] = (K,N)

    #if parameters are already saved, retrieve them from the setting dictionary
    else:
        number = setting["top_inventors_number"]
        inventors_count = Counter(inventors)
        top_inventors = sorted(inventors_count, key = inventors_count.get, reverse = True) [0:number]
        chosen = []
        if "extra_parameters" in setting.keys():
            (K, N) = setting["extra_parameters"]
            for a in inventors_dict.keys():
                counter =0
                citations = sorted(inventors_dict[a],reverse = True)
                length = len(citations)
                for c in citations:
                    if counter/length < K:
                        if c >= N:
                            counter += 1
                    else:
                        chosen.append(a)
                        break
    
    final_inventors_list = list(set(top_inventors + chosen))
    for a1 in final_inventors_list:
        matrix[a1]={}
        for a2 in final_inventors_list:
            matrix[a1][a2] = 0
    print(str(len(matrix)) + " inventors have been added to the matrix.")
    
    parameters = "Top inventors chosen: {0}. \n".format(str(len(top_inventors)))  
    if len(chosen)>0:
        parameters += "     Plus additional {2} inventors whose {0} percent of portfolio cited by at least {1} patents.\n".format(str(K*100), str(N),str(len(chosen)))
    
    return matrix,parameters, setting

#%% Create Patent-Domain Dictionary based on current dataset. Save in a folder. 

def CreateInventorDictionary (df):
    family_list=[]
    family_inventors = []

    for index, row in df.iterrows():
        fmls = row['Publication numbers'].split('\n')
        inventors = row['Inventors']
        for l in fmls:
            member_patent = l.split(' ')[0]
            family_list.append(member_patent)
            family_inventors.append(inventors)

    zipped = zip(family_list, family_inventors)
    inventors_dict = dict(zipped)

    assert(len(inventors_dict.keys()) == len(set(family_list)))

    return inventors_dict

def SaveInventorsDictionary(inventors_dict,save_path):
    path = str(save_path) + '/' + 'InventorsDictionary_'+ date+'.pkl'
    f = open(path,"wb")
    pickle.dump(inventors_dict,f)
    f.close()
    return None

#To load the dictionary:
def LoadInventorsDictionary(path):
    file_to_read = open(path, "rb")
    loaded_dictionary = pickle.load(file_to_read)
    return loaded_dictionary

#%% Find the inventors of patents
def MatchExistingPatentsInventor (df,inventors_dict,matrix,endyear, normalize):
    #Create a dictionary for storing the citation counts of each domain
    inventors_count = {}
    for inventor in matrix.keys():
        inventors_count[inventor]= 0
    
    exist_pt = inventors_dict.keys()
    all_unknowns = []
    for index, row in df.iterrows():
        own_inventors = row['Inventors'].split('\n')
        cited_inventors=[]
        unknown_patents = []
        known_patents = []
        cited_ls = row['Cited patents - Standardized publication number']
        cited_items_raw = cited_ls.split('\n')
        cited_items_trimmed =[]
    
        for item in cited_items_raw:
            cited_items_trimmed.append(item.split(';')[0])
            
        for pt in cited_items_trimmed:
            if pt in exist_pt:
                for inventor in inventors_dict[pt].split('\n'):
                    cited_inventors.append(inventor)
                known_patents.append(pt)
            else:
                unknown_patents.append(pt)
               
        cited_inventors_uq = list(set(cited_inventors))
        unknown_uq =list(set(unknown_patents))
        all_unknowns.append(unknown_uq)

        #a copy of df is created to avoid SettingWithCopyWarning
        df = df.copy()
        df.loc[index, 'unknown_patents_inventor'] = ','.join(unknown_uq)
        
        if normalize == "Y":
            year = row['datetime'].year
            denominator = float(endyear- year) +1.0
        else:
            denominator = 1.0
        
        #Add to the Matrix
        for oi in own_inventors:
            if oi != 'nan':
                if (oi in matrix.keys()):
                    inventors_count[oi] += 1/denominator
                    if (len(cited_inventors_uq) >0) & (cited_inventors_uq != 'nan'):
                        for ci in cited_inventors_uq:
                            if ci != 'nan':
                                if (ci in matrix.keys()):
                                    matrix[oi][ci] += 1/denominator
        
    unknowns = list(set([item for sublist in all_unknowns for item in sublist]))
    return (df,unknowns, matrix, inventors_count)

def SaveUnknownPatentsInventor (unknown,save_path):
    #make multiple documents each 46k long
    chunks = [unknown[x:x+46000] for x in range(0, len(unknown), 46000)]
    folder_path = save_path + '/' + 'UnknownPatents_Inventor_'+date
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for c in range(len(chunks)):
        path = folder_path +'/'+ str(c)+ '.txt'
        with open(path, 'w') as f:
            for item in chunks[c]:
                f.write(item + "\n") 
    return None

def SaveInventorCount(inventor_count,save_path):
    inventor_count_df = pd.DataFrame(inventor_count, index = ['count']).T
    inventor_count_df.reset_index(level=0, inplace=True)
    result = inventor_count_df.rename(columns = {'index': 'id'})
    path = save_path + '/' + 'node_list_inventors_' + date+'.xlsx'
    result.to_excel(path)
    return None