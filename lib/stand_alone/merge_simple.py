"""
Merge excel files to one csv without checking the columns or renaming columns.
The dataset must contain the column "Earliest publication number".

Merging can take 10-20 minutes
"""
import glob
import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def MergeFilesSimple (files_path):
    """
    Merge Files and Delete Duplicates
    """

    #store all file names under the directory in all_files
    all_files = glob.glob(files_path+'/*')

    #create empty list for storing dataframes (converted from excel)
    files = []

    #each iteration reads an excel file into a pandas dataframe
    for i in range(len(all_files)):
        file_name = all_files[i]
        file_raw = pd.read_excel(file_name,index_col=None)

        #finally, add the dataframe to the file list
        files.append(file_raw)
        print("processed ", str(i+1),"/", str(len(all_files)), " files...")

    #concatenate all files int he file list
    print("Concatenating files...")    
    combined_full = pd.concat(files,ignore_index=True,axis=0)

    #convert the type of data from object to string (for easy matching later)
    df = combined_full.astype(str)

    return df

def SaveDataset (df,save_path,name):
    """
    Save the merged dataset to output folder
    """
    loop = True
    while loop:
        try:
            save_to = save_path + "/" + name + ".csv"
            df.to_csv(save_to)
        except:
            print("Invalid address")
        loop = False
    return None


if __name__ == "__main__":
    files_path = input("Enter the path to the folder containing excel files:\n")
    save_path = input("Enter the path to the output folder:\n")
    name = input("\nGive the dataset a name(without extension): ")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    df = MergeFilesSimple (files_path)
    SaveDataset (df,save_path,name)
