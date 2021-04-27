"""
Run the modules for domain analysis in sequence
"""

from lib.default import *
from lib.domain import (CreateMatrix, CreateDomainDictionary,
                        SaveDomainCount,SaveDomainDictionary,
                        LoadDomainDictionary,MatchExistingPatents,
                        SaveUnknownPatents)
from lib.log import WriteLog
from lib.update import LoadNewDataset, UpdateDictionary 

def RunDomain (df, df_whole, dm_dict,save_path,save_path_master,endyear, normalize):
    matrix = CreateMatrix()
    WriteLog (save_path_master,'1', None)
    if dm_dict == None:
        var_pt = input("Do you want to create a new patent-domain dictionary? (Y/N): ")
        if var_pt == "Y":
            print("Creating patent-domain dictionary...")
            dm_dict = CreateDomainDictionary(df_whole)
            SaveDomainDictionary(dm_dict, save_path_master)
            print("Dictionary created and saved to the Output folder.")

        elif var_pt == "N":  
            dict_name = input("Provide the path to the existing dictionary with extension :")
            dict_path = os.path.abspath(dict_name)
            if os.path.exists(dict_path) == True:
                dm_dict = LoadDomainDictionary(dict_path)
            else:
                sys.exit("Cannot find the dictionary.")
    else:
        pass

    print("Matching cited patents with technology domains...")
    df_update, unknown, matrix_update, domain_count = MatchExistingPatents (df,dm_dict,matrix,endyear, normalize)
    print("Finished matching.")

    SaveDomainCount(domain_count,save_path)
    print("Saved domain sizes to the Output folder.")

    if len(unknown) > 0:
        SaveUnknownPatents (unknown,save_path)
        print(str(len(unknown)) + " patents have no match in current dataset. List exported to Output folder.")
        proceed_pt = input("Do you want to save the matrix with incomplete data?(Y/N): ")

    elif len(unknown) == 0:
        print("All the cited patents have been assigned technology domains.")
        proceed_pt = "Y"
 
    #If answer is "N", load new dataset
    while proceed_pt == "N":
        new_name = input("Please provide the path to the folder containing the additional datasets (xlsx format): ")
        if os.path.exists(new_name) == True:
            new_path = os.path.abspath(new_name)
            new_dict = LoadNewDataset(new_path)
            print("Adding to existing patent-domain dictionary...")
            dm_dict = UpdateDictionary(dm_dict, new_dict)
            SaveDomainDictionary(dm_dict, save_path_master)
            print("Dictionary has been updated and saved to Output folder. It has " + str(len(dm_dict)) + " key-value pairs.")
            print("Matching cited patents with technology domains...") #improve this with a diff function that uses partial data
            df_rest =df_update[df_update['unknown_patents'] != '']
            df_update, unknown, matrix_update, _ = MatchExistingPatents (df_rest,dm_dict,matrix_update, endyear, normalize)
            print("Finished matching.")

            if len(unknown) > 0:
                SaveUnknownPatents (unknown,save_path)
                print(str(len(unknown)) + " patents have no match in current dataset. List exported to Output folder.")
                proceed_pt = input("Do you want to save the matrix with incomplete data?(Y/N): ")

            elif len(unknown) == 0:
                print("All the cited patents have been assigned domain information.")
                proceed_pt = "Y"
        else:
            sys.exit("Cannot find the dataset.")
            proceed_pt = "N"

    return matrix_update, dm_dict