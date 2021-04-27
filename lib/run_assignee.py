from lib.default import *
from lib.assignee import CreateAssigneeMatrix, MatchExistingPatentsAssignee, SaveAssigneeCount
from lib.log import WriteLog

def RunAssignee(df,save_path,save_path_master, input_analysis, endyear, normalize, assignee_setting):
    matrix, parameters, assignee_setting = CreateAssigneeMatrix (df, assignee_setting) 
    WriteLog (save_path_master,input_analysis, parameters)
    print("Matching cited patents with assignee information...")
    df_update,matrix_update,assignee_count, assignee_IPC, assignee_CPC = MatchExistingPatentsAssignee (df,matrix,input_analysis,endyear,normalize)
    SaveAssigneeCount(assignee_count,assignee_IPC, assignee_CPC, save_path)

    return matrix_update, assignee_setting