"""
Divide the dataset into year blocks
"""
from lib.default import *

def CheckYears (df):
    """
    Ask user for the time frame
    """
    maxyear =  df['datetime'].max().year
    minyear = df['datetime'].min().year
    print("The earliest patent was published in {0}, the latest in {1}.".format(str(minyear), str(maxyear)))
    earliest = int(input("Key in the earliest year you want to include in this analysis: "))
    latest = int(input("Key in the latest year you want to include in this analysis: "))
    num = int(input("How many subgroups do you want create from the selected data?: "))
    size = math.floor((latest-earliest+1)/num)

    return earliest,latest,num,size,maxyear

def year_to_datetime (year):
    yearstring = str(year) + "-01-01"
    res = datetime.strptime(yearstring,'%Y-%m-%d')
    return res

def YearSegment (df,earliest,latest,num,size,maxyear) :
    """
    Return: A list of tuple (description, sliced data) and the latest year in the analysis
    """
    year_blocks =[]
    startyear = earliest
    endyear = earliest + size
    for i in range(0,num):
        start = year_to_datetime(startyear)
        end = year_to_datetime(endyear)
        slice = df.loc[(df['datetime'] >= start) & (df['datetime'] < end)].reset_index(drop = True)
        describe = str(startyear)+"to"+ str(endyear-1)
        year_blocks.append((describe,slice))
        startyear += size
        endyear += size
    #add the big time frame if subgroup is larger than 1
    if num >1 :
        all_years = df.loc[(df['datetime'] >= year_to_datetime(earliest)) & (df['datetime'] < year_to_datetime(latest+1))]
        year_blocks.append( ((str(earliest)+"to"+ str(latest)), all_years))
    return year_blocks, maxyear

