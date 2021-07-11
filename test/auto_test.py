"""
Test all main functionality without user inputs
Inputs:
test/test_data.xlsx
test/test_resources/additional_data
"""

#%% Set-up
import sys, os
import shutil
#%% Set-up
import pathlib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

date = datetime.now().strftime("%d_%m_%Y_%H%M")

# sys.path.append(os.path.abspath(os.path.join('..', 'lib')))
#set the working directory to the folder containing the current script
pathlib.Path(__file__).parent.absolute()
#all outputs will be saved to the current folder
save_path = 'test/test_output/'+ date

if not os.path.exists(save_path):
    os.makedirs(save_path)

#%%$ Run main functions in sequence
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from lib.flow import *
from lib.run_domain import *
from lib.run_assignee import *
from lib.run_inventor import *

def RunDomain_test (df, df_whole, dm_dict,save_path,save_path_master,endyear, normalize):
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
        proceed_pt = "N"

    elif len(unknown) == 0:
        print("All the cited patents have been assigned technology domains.")
        proceed_pt = "Y"
 
    #If answer is "N", load new dataset
    while proceed_pt == "N":
        new_name = "test/test_resources/additional_data"
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

def RunInventor_test (df,inventors_dict, df_whole, save_path, save_path_master, endyear, normalize, inventor_setting):
    matrix, parameters, inventor_setting = CreateInventorMatrix (df,inventor_setting) 
    WriteLog (save_path_master,'8', parameters)

    if inventors_dict == None:
        var_pt = input("Do you want to create a new patent-inventor dictionary? (Y/N): ")
        if var_pt == "Y":
            print("Creating patent-inventor dictionary...")
            inventors_dict = CreateInventorDictionary(df_whole)
            SaveInventorsDictionary(inventors_dict, save_path_master)
            print("Dictionary created and saved to the Output folder.")

        elif var_pt == "N":  
            dict_name = input("Provide the path to the existing dictionary with extension? :")
            dict_path = os.path.abspath(dict_name)
            if os.path.exists(dict_path):
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
        proceed_pt = "N"
 
    elif len(unknown) == 0:
        print("All the cited patents have been assigned inventors.")
        proceed_pt = "Y"

    
        #Add another while loop for invalid input
    while proceed_pt == "N":
        new_name = "test/test_resources/additional_data"
        if os.path.exists(new_name) == True:
            new_path = os.path.abspath(new_name)
            new_dict = LoadNewDatasetInventor(new_path)
            print("Adding to existing patent-inventor dictionary...")
            inventors_dict = UpdateDictionary(inventors_dict, new_dict)
            SaveInventorsDictionary(inventors_dict, save_path)
            print("Dictionary has been updated and saved to Output folder. It has " + str(len(inventors_dict)) + " key-value pairs.")
            print("Matching cited patents with inventors...")
            df_rest =df_update[df_update['unknown_patents'] != '']
            df_update, unknown, matrix_update, _ = MatchExistingPatentsInventor (df_rest,inventors_dict,matrix_update,endyear, normalize)
            print("Finished matching.")

            if len(unknown) > 0:
                SaveUnknownPatentsInventor (unknown,save_path_master)
                print(str(len(unknown)) + " patents have no match in current dataset. List exported to Output folder.")
                proceed_pt = input("Do you want to save the matrix with incomplete data?(Y/N): ")

            elif len(unknown) == 0:
                print("All the cited patents have been assigned inventors.")
                proceed_pt = "Y"
        else:
            sys.exit("Cannot find the dataset.")

    return matrix_update, inventors_dict,inventor_setting

def auto_test (save_path):
    #load dictionary and parameters
    domain_dict = LoadDomainDictionary("test/test_resources/DomainDictionary.pkl")
    inventor_dict = LoadDomainDictionary("test/test_resources/InventorDictionary.pkl")
    inventor_setting  = {"top_inventors_number":10, "extra_parameters": (10,10)}
    assignee_setting = {"top_assignees_number":10, "extra_parameters": (10,10)}

    save_path_master = save_path
    #retrieve dataset
    df = GetXLSX("test/test_data.xlsx")
    CheckColumns(df)
    df = ChangeSubsidiaryNamesDF (df)
    df = AddDatetime(df)

    #merge excel files to obtain dataset

    files_path = "test/test_input"
    name = "test_saved_data"
    print("Selecting relevant columns...")
    relevant_cols, rename = SelectColumns(files_path)
    print("Merging excel files...")
    df = MergeFiles (files_path,relevant_cols, rename)
    df = ChangeSubsidiaryNamesDF (df)
    df = AddDatetime(df)
    SaveDataset (df,save_path,name)
    CheckColumns(df)
    
    #save a copy of the complete df
    df['unknown_patents'] = "nan"
    df_whole = df

    #divide dataset into n-year blocks
    year_blocks,endyear = YearSegment(df,2011,2020,1,10,2020)
    assert(len(year_blocks) == 1)
    assert(year_blocks[0][0] == "2011to2020")
    assert(len(year_blocks[0][1]) == len(df))
    assert(endyear == 2020)
    
    #try all permutations of parameters
    parameters = (
    ("Y","1"),
    ("Y","2"),
    ("N","1"),
    ("N","2"),
    )
    for (normalize, use_count) in parameters:
        #Choose type of analysis
        input_list = ["1","2","3","4","5","6","7","8"]

        #Create matrix for each n-year block
        for describe, df in year_blocks:
            #Log the current year block. Create folder for each block
            WriteYear(save_path_master,describe)
            save_path =save_path_master + "/" + describe +"/"
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            #Creatematrix for each analysis
            for input_analysis in input_list:
                print("Generating Citeflow matrix"+" for analysis #"+ input_analysis+"...")
                #Assignee analysis
                if input_analysis != '1' and input_analysis != '8':
                    matrix_update, assignee_setting = RunAssignee(df,save_path,save_path_master, input_analysis, endyear, normalize, assignee_setting)
                    matrix_df = CleanMatrix(matrix_update)
                    if use_count == "1":
                        CF_df = matrix_df #absolute number/ count
                    else:
                        CF_df = CreateCiteFlowMatrix (matrix_df)  #citeflow index
                    
                #Domain analysis
                elif input_analysis == '1':
                    matrix_update, domain_dict = RunDomain_test(df,df_whole, domain_dict, save_path, save_path_master,endyear, normalize)
                    matrix_df = CleanMatrix(matrix_update)
                    if use_count == "1":
                        CF_df = matrix_df #absolute number/ count
                    else:
                        CF_df = CreateCiteFlowMatrix (matrix_df)  #citeflow index
                    
                #Inventor analysis
                elif input_analysis == '8':
                    matrix_update, inventor_dict, inventor_setting = RunInventor_test(df,inventor_dict, df_whole, save_path, save_path_master,endyear, normalize,inventor_setting)
                    matrix_df = CleanMatrix(matrix_update)
                    if use_count == "1":
                        CF_df = matrix_df #absolute number/ count
                    else:
                        CF_df = CreateCiteFlowMatrix (matrix_df)  #citeflow index

                print("\nAnalysis #",input_analysis + " is completed for ",describe,"\n" )
                SaveCiteFlowMatrix (CF_df,save_path,input_analysis)
                GenerateHeatMap(CF_df, save_path, input_analysis)
            print("-------Analysis is completed for ",describe, "-------\n")

    to_remove = input("Test done. Remove test outputs? (Y/N): ")
    if to_remove == "Y":
        shutil.rmtree(save_path_master)
    return None

if __name__ == "__main__":
    auto_test (save_path)