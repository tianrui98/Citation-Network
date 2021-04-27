"""
Stores default information and imports
"""
import pandas as pd
import glob
import math
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import pickle
import time
import os
import sys
from collections import Counter
from datetime import datetime
import re

now = datetime.now()
date = now.strftime("%d_%m_%Y_%H%M")

dms_ls =['Electrical machinery, apparatus, energy', 'Audio-visual technology', 'Telecommunications', 'Digital communication', 'Basic communication processes', 'Computer technology',
         'IT methods for management', 'Semiconductors', 'Optics', 'Measurement', 'Analysis of biological materials', 'Control', 'Medical technology', 'Organic fine chemistry', 
         'Biotechnology', 'Pharmaceuticals', 'Macromolecular chemistry, polymers', 'Food chemistry', 'Basic materials chemistry', 'Materials, metallurgy', 'Surface technology, coating',
         'Micro-structure and nano-technology', 'Chemical engineering', 'Environmental technology', 'Handling', 'Machine tools', 'Engines, pumps, turbines', 'Textile and paper machines',
         'Other special machines', 'Thermal processes and apparatus', 'Mechanical elements', 'Transport', 'Furniture, games', 'Other consumer goods', 'Civil engineering']

tech_fields = {'Electrical machinery, apparatus, energy':'Electrical Engineering',
'Audio-visual technology':'Electrical Engineering',
'Telecommunications':'Electrical Engineering',
'Digital communication':'Electrical Engineering',
'Basic communication processes':'Electrical Engineering',
'Computer technology':'Electrical Engineering',
'IT methods for management':'Electrical Engineering',
'Semiconductors':'Electrical Engineering',
'Optics':'Instruments',
'Measurement':'Instruments',
'Analysis of biological materials':'Instruments',
'Control':'Instruments',
'Medical technology':'Instruments',
'Organic fine chemistry':'Chemistry',
'Biotechnology':'Chemistry',
'Pharmaceuticals':'Chemistry',
'Macromolecular chemistry, polymers':'Chemistry',
'Food chemistry':'Chemistry',
'Basic materials chemistry':'Chemistry',
'Materials, metallurgy':'Chemistry',
'Surface technology, coating':'Chemistry',
'Micro-structure and nano-technology':'Chemistry',
'Chemical engineering':'Chemistry',
'Environmental technology':'Chemistry',
'Handling':'Mechanical Engineering',
'Machine tools':'Mechanical Engineering',
'Engines, pumps, turbines':'Mechanical Engineering',
'Textile and paper machines':'Mechanical Engineering',
'Other special machines':'Mechanical Engineering',
'Thermal processes and apparatus':'Mechanical Engineering',
'Mechanical elements':'Mechanical Engineering',
'Transport':'Mechanical Engineering',
'Furniture, games':'Mechanical Engineering',
'Other consumer goods':'Mechanical Engineering',
'Civil engineering':'Mechanical Engineering'}

#%% Decide the type of analysis and create an empty matrix (dictionary form)
def AnalysisType ():
    input_string = input("What analysis do you want to perform(enter numbers separated by ',''):"+
    "\n1:Analyse the technology domains of cited patents"+
    "\n2:Analyse the assignees of cited patents"+
    "\n3:Analyse the assignees of cited patents (Examiner citations only)"+
    "\n4:Analyse the assignees of cited patents (Applicant citations only)"+
    "\n5:Analyse the assignees of citing patents"+
    "\n6:Analyse the assignees of citing patents (Examiner citations only)"+
    "\n7:Analyse the assignees of citing patents (Applicant citations only)"+
    "\n8:Analyse the inventors of cited patents.\n") 
    input_list = input_string.split(',')
    for input_analysis in input_list:
        while input_analysis not in ['1','2','3','4','5','6','7','8']:
            input_string = input("Please enter valid numbers.\nWhat analysis do you want to perform(enter number,separated by ',')\n")
            input_list = input_string.split(',')
            for i in input_list:
                input_analysis = i
    return input_list

def InputToName (input_analysis):
    if input_analysis == "1":
        name = "cited_domain"
    elif input_analysis == "2":
        name = "cited_assignee_all"
    elif input_analysis == "3":
        name = "cited_assignee_examiner"
    elif input_analysis == "4":
        name = "cited_assignee_applicant"
    elif input_analysis == "5":
        name = "citing_assignee_all"
    elif input_analysis == "6":
        name = "citing_assignee_examiner"
    elif input_analysis == "7":
        name = "citing_assignee_applicant"
    elif input_analysis == "8":
        name = "cited_inventor"
    return name