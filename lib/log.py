
"""
Records the type of analysis performed and the time frames of the analysis
"""
from lib.default import InputToName

def WriteLog (save_path,input_analysis, parameters = None):
    path = save_path + '/' + 'Log.txt'
    name = InputToName(input_analysis)
    with open(path, 'a+') as f:
        f.write(name + "\n")
        if parameters != None:
            f.write("   " + parameters + "\n")
    return None

def WriteYear (save_path, describe):
    path = save_path + '/' + 'Log.txt'
    with open(path, 'a+') as f:
        f.write(describe + "\n")
    return None