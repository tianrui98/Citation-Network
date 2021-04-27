"""
Run the modules for inventor analysis in sequence
"""
from lib.default import *
from lib.inventor import (CreateInventorMatrix, CreateInventorDictionary,
                            SaveInventorsDictionary,LoadInventorsDictionary, 
                            MatchExistingPatentsInventor,SaveUnknownPatentsInventor,
                            SaveInventorCount)
from lib.log import WriteLog
from lib.update import LoadNewDatasetInventor, UpdateDictionary 

def RunInventor (df,inventors_dict, df_whole, save_path, save_path_master, endyear, normalize, inventor_setting):
    matrix, parameters, inventor_setting = CreateInventorMatrix (df,inventor_setting) 
    WriteLog (save_path_master,'8', parameters)

    if inventors_dict == None:
        var_pt = input("Do you want to create a new patent-inventor dictionary? (Y/N): ").strip().upper()
        if var_pt == "Y":
            print("Creating patent-inventor dictionary...")
            inventors_dict = CreateInventorDictionary(df_whole)
            SaveInventorsDictionary(inventors_dict, save_path_master)
            print("Dictionary created and saved to the Output folder.")

        elif var_pt == "N":  
            dict_name = input("Provide the path to the existing dictionary with extension? :")
            dict_path = os.path.abspath(dict_name)
            if os.path.exists(dict_path) == True:
                inventors_dict = LoadInventorsDictionary(dict_path)
            else:
                sys.exit("Cannot find the dictionary.")
    else:
        pass

    print("Matching cited patents with inventors...")
    df_update,unknown,matrix_update,inventor_count = MatchExistingPatentsInventor (df,inventors_dict,matrix, endyear, normalize)
    print("Finished matching.")

    SaveInventorCount(inventor_count,save_path)
    print("Saved domain sizes to the Output folder.")

    if len(unknown) > 0:
        SaveUnknownPatentsInventor (unknown,save_path)
        print(str(len(unknown)) + " patents have no match in current dataset. List exported to Output folder.")
        proceed_pt = input("Do you want to save the matrix with incomplete data?(Y/N): ").strip().upper()
 
    elif len(unknown) == 0:
        print("All the cited patents have been assigned inventors.")
        proceed_pt = "Y"

    
        #Add another while loop for invalid input
    while proceed_pt == "N":
        new_name = input("Please provide the path to the folder containing the additional datasets (xlsx format): ")
        if os.path.exists(new_name) == True:
            new_path = os.path.abspath(new_name)
            new_dict = LoadNewDatasetInventor(new_path)
            print("Adding to existing patent-inventor dictionary...")
            inventors_dict = UpdateDictionary(inventors_dict, new_dict)
            SaveInventorsDictionary(inventors_dict, save_path)
            print("Dictionary has been updated and saved to Output folder. It has " + str(len(inventors_dict)) + " key-value pairs.")
            print("Matching cited patents with inventors...") #improve this with a diff function that uses partial data
            df_rest =df_update[df_update['unknown_patents'] != '']
            df_update, unknown, matrix_update, _ = MatchExistingPatentsInventor (df_rest,inventors_dict,matrix_update,endyear, normalize)
            print("Finished matching.")

            if len(unknown) > 0:
                SaveUnknownPatentsInventor (unknown,save_path_master)
                print(str(len(unknown)) + " patents have no match in current dataset. List exported to Output folder.")
                proceed_pt = input("Do you want to save the matrix with incomplete data?(Y/N): ").strip().upper()

            elif len(unknown) == 0:
                print("All the cited patents have been assigned inventors.")
                proceed_pt = "Y"
        else:
            sys.exit("Cannot find the dataset.")
            proceed_pt = "N"

    return matrix_update, inventors_dict,inventor_setting