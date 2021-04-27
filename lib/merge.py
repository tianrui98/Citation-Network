"""
Select relevant columns from the dataset.
Rename the assignee column headers based on the type of citation: examiner, applicant or all
Merge individual excel sheets into a csv file

Merging can take 10-20 minutes
"""
from lib.default import *

def SelectColumns (files_path):
    """
    Check if all relevant columns are in the dataset
    Figure out which assignee column has only examiner citations, or applicant citations or both 
    """
    #import the first data file to check if all relevant columns are there
    first_file = glob.glob(files_path+'/*')[0]
    df = pd.read_excel(first_file, index_col = None)
    relevant_cols = [
        'Publication numbers',
        'Earliest publication number',
        'Technology domains',
        'Current assignees',
        'Main IPC',
        'Main CPC',
        'Title',
        'Abstract',
        'Earliest publication date',
        'Inventors'
       ]
    for item in relevant_cols:
        try:
            assert(item in df.columns)
        except:
            sys.exit("Cannot find "+item+" in your dataset.")
    rename = {}
    check_cited = []
    check_citing = []
    for col in df.columns:
        if 'Cited patents - By Examiner, applicant' in col:
            check_cited.append(col)
        elif 'Citing patents - By Examiner, applicant' in col:
            check_citing.append(col)
    try:
        assert(len(check_cited) >= 3)
    except:
        sys.exit("Less than three sets of backward citations")
    try:
        assert(len(check_citing) >= 3)
    except:
        sys.exit("Less than three sets of forward citations")
   
    for c in [check_cited,check_citing]:
        df = df.astype(str)
        #Assume the first 50 columns contains enough information
        head = df.head(50)
        for col in c:
            info = head.loc[:,col].tolist()
            content = []
            for row in info:
                items = row.split('\n')
                content += items
            if ("EXAMINER" in content) and ("APPLICANT" not in content):
                    examiner_col = col
            elif ("APPLICANT" in content) and ("EXAMINER" not in content):
                    applicant_col = col
            elif ("EXAMINER" in content) and ("APPLICANT" in content):
                    both_col = col
        assert(examiner_col != applicant_col)   
        assert(both_col != examiner_col)
        assert(both_col != applicant_col)
        col_dict ={ "APPLICANT":applicant_col, "EXAMINER": examiner_col ,  "ALL": both_col}
        for key in col_dict.keys():
            match = re.search("[1-9]", col_dict[key])
            if match is not None:
                number = match.group(0)
                if "Cited" in c[0]:
                    rename['Cited patents - Standardized publication number'+'.'+str(number)] = str('Cited patents - Standardized publication number-'+ key)
                    rename['Cited patents - Applicant/assignee'+'.'+str(number)] = str('Cited patents - Applicant/assignee-'+ key)
                    # rename['Cited patents - By Examiner, applicant'+'.'+str(number)] = str('Cited patents - By Examiner, applicant-'+key)
                elif "Citing" in c[0]:
                    rename['Citing patents - Standardized publication number'+'.'+str(number)] = str('Citing patents - Standardized publication number-'+key)
                    rename['Citing patents - Applicant/assignee'+'.'+str(number)] = str('Citing patents - Applicant/assignee-'+key)
                    # rename['Citing patents - By Examiner, applicant'+'.'+str(number)] = str('Citing patents - By Examiner, applicant-'+key)
                else:
                    sys.exit("Error occurred during renaming.")
            else:
                if "Cited" in c[0]:
                    rename['Cited patents - Standardized publication number'] = str('Cited patents - Standardized publication number-'+ key)
                    rename['Cited patents - Applicant/assignee'] = str('Cited patents - Applicant/assignee-'+ key)
                    # rename['Cited patents - By Examiner, applicant'] = str('Cited patents - By Examiner, applicant-'+ key)
                elif "Citing" in c[0]:
                    rename['Citing patents - Standardized publication number'] = str('Citing patents - Standardized publication number-'+ key)
                    rename['Citing patents - Applicant/assignee'] = str('Citing patents - Applicant/assignee-'+ key)
                    # rename['Citing patents - By Examiner, applicant'] = str('Citing patents - By Examiner, applicant-'+ key)
                else:
                    sys.exit("Error occurred during renaming.")

    for key in rename.keys():
        relevant_cols.append(key)
    return relevant_cols, rename




def MergeFiles (files_path,relevant_cols, rename):
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
        file_raw = pd.read_excel(file_name,usecols=relevant_cols ,index_col=None)

        #finally, add the dataframe to the file list
        files.append(file_raw)
        print("processed ", str(i+1),"/", str(len(all_files)), " files...")

    print("Concatenating files...")    
    #concatenate all files int he file list    
    combined_full = pd.concat(files,ignore_index=True,axis=0)

    print("Removing duplicates...")   
    #drop duplicate rows of the same earliest publication number
    df = combined_full.drop_duplicates(subset = ['Earliest publication number'])

    df = df.rename(columns = rename)

    #convert the type of data from object to string (for easy matching later)
    df = df.astype(str)

    return df

def SaveDataset (df,save_path,name):
    """
    Save the merge dataset to output folder
    """
    save_to = save_path + "/" + name + ".csv"
    df.to_csv(save_to)
    return None
