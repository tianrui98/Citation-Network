"""
Functions in this module performs operations on the citation matrix.
"""
from lib.default import *

def CleanMatrix (matrix):
    """
    Cleans matrix (dictionary):
    Set self-citation to 0.0

    Return: citation matrix (pd.DataFrame)
    """
    matrix_df = pd.DataFrame.from_dict(matrix).T.astype(float)

    
    for name, row in matrix_df.iterrows():
        matrix_df.at[name,name] = 0.0
    
    print(str(len(matrix_df)) + " items are in the final matrix.")    
    return matrix_df


def CreateCiteFlowMatrix (matrix_df):
    """
    Convert citation matrix to Citeflow matrix using the CiteFlow formula

    Return: Citeflow matrix (pd.DataFrame)
    """
    CF_df = matrix_df
    for index, row in CF_df.iterrows():
        #Calculate citeflow: Y cites X / Y cites non-Y
        row_sum = sum(row)
        assert(row_sum == sum(row.to_list()))
        for col in CF_df.columns:
            #if a company/domain only cites itself, citeflow value is 0
            if row_sum == 0.0:
                value = 0.0
            #otherwise, citeflow value = No.of citations / row sum
            else:
                value = row[col]/row_sum
            if index != col:
                CF_df.at[index, col] = value

    return CF_df

def SaveCiteFlowMatrix (CF_df, save_path,input_analysis):
    """
    Save citation matrix or citeflow matrix to the output folder.
    Convert the matrix to edge list and save to the output folder
    """
    name = InputToName(input_analysis)
    path = save_path + '/' + 'matrix_'+name + '_' + date+'.xlsx'
    CF_df.to_excel(path)
    edge = CF_df.rename_axis('Source')\
              .reset_index()\
              .melt('Source', value_name='Weight', var_name='Target')\
              .query('Source != Target')\
              .reset_index(drop=True)

    if "citing" in name:
        direction  = "Source cited by Target"
    if "cited" in name:
        direction = "Source cites Target"
    edge.insert(3, 'Interaction', pd.Series([direction for i in range(len(edge))]), allow_duplicates=False)
    for index, row in edge.iterrows():
        if row['Weight'] == 0:
            edge.drop(index = index, inplace = True)
    path = save_path + '/' + 'edge_list_'+name + '_' + date+'.xlsx'
    edge.to_excel(path)
    return None