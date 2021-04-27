"""
Run modules in sequence
"""

from lib.default import *
from lib.read_data import GetCSV, GetXLSX, CheckColumns
from lib.merge import SelectColumns,MergeFiles,SaveDataset
from lib.citeflow import CleanMatrix, CreateCiteFlowMatrix,SaveCiteFlowMatrix
from lib.run_domain import RunDomain
from lib.run_inventor import RunInventor
from lib.run_assignee import RunAssignee
from lib.log import WriteYear
from lib.yearblock import YearSegment
from lib.clean_companies import ChangeSubsidiaryNamesDF
from lib.graphs import GenerateHeatMap

def RunAll (save_path):
    save_path_master = save_path

    #retrieve dataset
    havedataset = input("Do you have a dataset ready for analysis? (Y/N): ") 
    if havedataset == "Y" :
        datatype = input("What is the extension of the dataset?:\n1. csv\n2.xlsx\n")
        if datatype == "1":
            df = GetCSV()
        else:
            df = GetXLSX()
        CheckColumns(df)
        df = ChangeSubsidiaryNamesDF (df)

    #merge excel files to obtain dataset
    else:
        files_path = input("Enter the path to the folder containing the excel sheets:\n")
        download_prompt = input("Do you want to save the merged dataset? (Y/N): ")
        if download_prompt == "Y":
            name = input("\nGive the dataset a name(without extension): ")
        print("Selecting relevant columns...")
        relevant_cols, rename = SelectColumns(files_path)
        print("Merging excel files...")
        df = MergeFiles (files_path,relevant_cols, rename)
        df = ChangeSubsidiaryNamesDF (df)
        if download_prompt == "Y":
            SaveDataset (df,save_path,name)
    
    #save a copy of the complete df
    df['unknown_patents'] = "nan"
    df_whole = df

    #divide dataset into n-year blocks
    segmentbyyear = input("Do you want to segment the dataset by year? (Y/N): ")
    if segmentbyyear == "Y":
        year_blocks,endyear = YearSegment(df)
    else:
        year_blocks = [("all_years",df)]
        endyear = now
    
    normalize = input("Normalize citation numbers by year? (Y/N): ")
   
    use_count = input("Make citation matrix from:\n1: actual number of citations\n2: CiteFlow\n ")

    #if heap map should be created for all analysis
    create_graph = input("Do you want to create heap maps from citation matrices? (Y/N): ")
 
     #Choose type of analysis
    input_list = AnalysisType ()

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
                if "assignee_setting" in locals():
                    matrix_update, assignee_setting = RunAssignee(df,save_path,save_path_master, input_analysis, endyear, normalize, assignee_setting)
                else:
                    matrix_update, assignee_setting = RunAssignee(df,save_path,save_path_master, input_analysis, endyear, normalize, None)
                matrix_df = CleanMatrix(matrix_update)
                if use_count == "1":
                    CF_df = matrix_df #absolute number/ count
                else:
                    CF_df = CreateCiteFlowMatrix (matrix_df)  #citeflow index
                
            #Domain analysis
            elif input_analysis == '1':
                if "domain_dict" in locals():
                    matrix_update, domain_dict = RunDomain(df,df_whole, domain_dict, save_path, save_path_master,endyear, normalize)
                else:
                    matrix_update, domain_dict = RunDomain(df,df_whole, None , save_path, save_path_master,endyear, normalize)
                matrix_df = CleanMatrix(matrix_update)
                if use_count == "1":
                    CF_df = matrix_df #absolute number/ count
                else:
                    CF_df = CreateCiteFlowMatrix (matrix_df)  #citeflow index
                
            #Inventor analysis
            elif input_analysis == '8':
                if "inventor_setting" in locals():
                    setting = inventor_setting
                else:
                    setting = None
                if "inventor_dict" in locals():
                    in_dict = inventor_dict
                else:
                    in_dict = None
                matrix_update, inventor_dict, inventor_setting = RunInventor(df,in_dict, df_whole, save_path, save_path_master,endyear, normalize,setting)
                matrix_df = CleanMatrix(matrix_update)
                if use_count == "1":
                    CF_df = matrix_df #absolute number/ count
                else:
                    CF_df = CreateCiteFlowMatrix (matrix_df)  #citeflow index

            print("\nAnalysis #",input_analysis + " is completed for ",describe,"\n" )
            SaveCiteFlowMatrix (CF_df,save_path,input_analysis)

            if create_graph == "Y":
                GenerateHeatMap(CF_df, save_path, input_analysis)
        print("-------Analysis is completed for ",describe, "-------\n")

    return None

