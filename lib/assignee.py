"""
This module contains functions that generate citation matrix for assignee analysis
and consolidate assignee information (no. of patents published, top 3 IPC, top 3 CPC)
"""

from lib.default import *

def CreateAssigneeMatrix (df, setting = None):
    """
    Create empty matrix for assignee analysis.
    User can choose to save the parameters for later assignee analysis
    """
    assignees_dict = {}
    assignees= []

    for index, row in df.iterrows():   
        asn_list = row['Current assignees'].split('\n')
        if asn_list[0] != 'nan':
            for a in asn_list:
                citation = len(row['Citing patents - Standardized publication number'].split('\n'))
                if a not in assignees_dict.keys():
                    assignees_dict[a] = [citation]
                    assignees.append(a)
                else:
                    assignees_dict[a].append(citation)
                    assignees.append(a)

    if setting == None:
        number = int(input("How many top patent applicants (based on the number of forward citations) do you want to add to the analysis?\n"))
        assignees_count = Counter(assignees)
        top_assignees = sorted(assignees_count, key = assignees_count.get, reverse = True) [0:number]
        chosen = []
        con = False

        extra =  input("Do you want to add more applicants based on other criteria? (Y/N): ").strip().upper()
        if extra == "Y":
            con = False
        if extra == "N":
            con = True
        
        while con == False:
            print("\nThe program will select the applicants who have at least K% of their portfolio cited by at least N patents ") 
            K = int(input("Enter K: "))/100
            N = int(input("Enter N: "))
            chosen = []
            for a in assignees_dict.keys():
                counter =0
                citations = sorted(assignees_dict[a],reverse = True)
                length = len(citations)
                for c in citations:
                    if counter/length < K:
                        if c >= N:
                            counter += 1
                    else:
                        chosen.append(a)
                        break
            
            proceed = input(str(len(chosen)) + " applicants have been selected. Proceed to add them to the matrix? (Y/N): ").strip().upper()        
            if proceed == "Y":
                con = True
                
            else:
                con = False
                print("Adjust the parameters.\n")
        save_setting = input ("Do you want to save the parameters for other assignee analysis? (Y/N): ").strip().upper()
        if save_setting == "Y":
            setting = {}
            setting["top_assignees_number"] = number
            if "K" in locals():
                setting["extra_parameters"] = (K,N)
    else:
        number = setting["top_assignees_number"]
        assignees_count = Counter(assignees)
        top_assignees = sorted(assignees_count, key = assignees_count.get, reverse = True) [0:number]
        chosen = []
        if "extra_parameters" in setting.keys():
            (K, N) = setting["extra_parameters"]
            for a in assignees_dict.keys():
                counter =0
                citations = sorted(assignees_dict[a],reverse = True)
                length = len(citations)
                for c in citations:
                    if counter/length < K:
                        if c >= N:
                            counter += 1
                    else:
                        chosen.append(a)
                        break
    
    final_assignee_list = list(set(top_assignees + chosen))
    matrix = {}
    for a1 in final_assignee_list:
        matrix[a1]={}
        for a2 in final_assignee_list:
            matrix[a1][a2] = 0
    print(str(len(matrix)) + " applicants have been added to the matrix.")      
    parameters = "Top assignees chosen: {0}. \n".format(str(len(top_assignees)))  
    if len(chosen)>0:
        parameters += "     Plus additional {2} applicants whose {0} percent of portfolio cited by at least {1} patents.\n".format(str(K*100), str(N),str(len(chosen)))
    return matrix, parameters, setting


def MatchExistingPatentsAssignee (df,matrix,input_analysis,endyear, normalize):
    """
    Match "Current assignees" with the citing or cited assignee depending on the type of analysis.
    It provides the option to normalize the number of citations by year.
    """

    assignee_count = {}
    assignee_IPC = {}
    assignee_CPC = {}
    for an in matrix.keys():
        assignee_count[an]= 0
    if input_analysis == '2':
        direction = 'Cited'
        EAfilter = ''
    elif input_analysis == '3':
        direction = 'Cited'
        EAfilter = '-EXAMINER'
    elif input_analysis == '4':
        direction = 'Cited'
        EAfilter = '-APPLICANT'
    elif input_analysis == '5':
        direction = "Citing"
        EAfilter = ''
    elif input_analysis == '6':
        direction = "Citing"
        EAfilter = '-EXAMINER'
    elif input_analysis == '7':
        direction = "Citing"
        EAfilter = '-APPLICANT'

    for index, row in df.iterrows():
        own_assignees = row['Current assignees'].split('\n')
        own_assignees_IPC = row ['Main IPC']
        own_assignees_CPC = row ['Main CPC']
        col_name = direction +' patents - Applicant/assignee'+ EAfilter
        cited_ls = row[col_name]
        cited_items_raw = cited_ls.split('\n')     
        cited_items_trimmed =[]
        for item in cited_items_raw:
            cited_items_trimmed.append(item.split('([')[0])
        cited_assignees_set = list(set(cited_items_trimmed))

        if normalize == "Y":
            year = row['datetime'].year
            denominator = float(endyear- year) +1.0
        else:
            denominator = 1.0

        for oa in own_assignees:
            if oa != 'nan':
                if (oa in matrix.keys()):
                    assignee_count[oa] += 1/denominator
                    if oa not in assignee_IPC.keys():
                        assignee_IPC[oa] = [own_assignees_IPC]
                        assignee_CPC[oa] = [own_assignees_CPC]
                    else:
                        assignee_IPC[oa].append(own_assignees_IPC)
                        assignee_CPC[oa].append(own_assignees_CPC)
                    if (len(cited_assignees_set) >0) & (cited_assignees_set != 'nan'):
                        for ca in cited_assignees_set:
                            if ca != 'nan':
                                if (ca in matrix.keys()):
                                    matrix[oa][ca] += 1 /denominator 

    return (df,matrix,assignee_count,assignee_IPC, assignee_CPC)


def SaveAssigneeCount(assignee_count,assignee_IPC, assignee_CPC, save_path):
    """
    Consolidate assignee information (count, IPC, CPC) and save to the output folder
    as a node list.
    """
    assignee_count_df = pd.DataFrame(assignee_count, index = ['count']).T
    assignee_count_df = assignee_count_df.rename(columns = {'index': 'id'})
    IPC_CPC_dict = {}
    for key in assignee_IPC.keys():
        IPC_list = list(filter(lambda a: a != "nan", assignee_IPC[key]))
        CPC_list = list(filter(lambda a: a != "nan", assignee_CPC[key]))
        if len(IPC_list) > 0 :
            IPC_sorted = sorted(Counter(IPC_list), key = Counter(IPC_list).get, reverse = True)
            Top_3_IPC = IPC_sorted[0:3]
            Top_IPC = IPC_sorted[0]
            IPC_CPC_dict[key] = {}
            IPC_CPC_dict[key]["top_3_IPC"] = ",".join(Top_3_IPC) 
            IPC_CPC_dict[key]["top_IPC"] = Top_IPC 
        else:
            IPC_CPC_dict[key]["top_3_IPC"] = ""
            IPC_CPC_dict[key]["top_IPC"] = ""
        if len(CPC_list) > 0 :
            CPC_sorted = sorted(Counter(CPC_list), key = Counter(CPC_list).get, reverse = True)
            Top_3_CPC = CPC_sorted[0:3]
            Top_CPC = CPC_sorted[0]
            IPC_CPC_dict[key]["top_3_CPC"] = ",".join(Top_3_CPC) 
            IPC_CPC_dict[key]["top_CPC"] = Top_CPC   
        else:
            IPC_CPC_dict[key]["top_3_CPC"] = "" 
            IPC_CPC_dict[key]["top_CPC"] = ""
    IPC_CPC_df = pd.DataFrame(IPC_CPC_dict).T
    combine = pd.merge(assignee_count_df, IPC_CPC_df, left_index=True, right_index=True)
    path = save_path + '/' + 'node_list_assignee' + date+'.xlsx'
    combine.to_excel(path)
    return combine

def test_save_assignee_count () :
    """
    unit test for save_assignee_count function
    """
    assignee_count = {"a": 100, "b": 200, "c": 300}
    assignee_IPC = {"a": ["1","1","nan"], "b":["nan","2","2"], "c": ["nan","2","3"]}
    assignee_CPC = {"a": ["1","2","2"], "b":["1","2","1"], "c": ["1","2","3"]}
    combine = SaveAssigneeCount (assignee_count, assignee_IPC, assignee_CPC, "~/Desktop")
    assert(len(combine.columns) == 5)
    assert(combine.loc["a","count"] == 100)
    assert(combine.loc["a","top_3_IPC"] == "1")
    assert(combine.loc["b","top_3_CPC"] == "1,2")
