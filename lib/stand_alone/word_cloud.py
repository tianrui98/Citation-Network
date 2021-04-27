"""
This module is used for generating word clouds for each cluster based on patent titles and abstracts.
It is not integrated into the main program because this operation is optional.

For the format of cluster list please see data/sample_clusters.xlsx
Make sure that the column headings are exactly like the sample,
and if multiple sheets exist in the excel file, put the earliest period firs, and the overall period last. 
"""

import pandas as pd
from datetime import datetime
import math
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os

def year_segment_wc (df,earliest,latest,num) :
    """
    Divide the data into year blocks
    Return: year blocks containing the description of the time frame and the sliced dataframe
    """
    df['datetime'] = df['Earliest publication date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    size = math.floor((latest-earliest+1)/num)
    def year_to_datetime (year):
        yearstring = str(year) + "-01-01"
        res = datetime.strptime(yearstring,'%Y-%m-%d')
        return res
    year_blocks =[]
    startyear = earliest
    endyear = earliest + size
    for _ in range(0,num):
        start = year_to_datetime(startyear)
        end = year_to_datetime(endyear)
        slice = df.loc[(df['datetime'] >= start) & (df['datetime'] < end)]
        describe = str(startyear)+"to"+ str(endyear-1)
        year_blocks.append((describe,slice))
        startyear += size
        endyear += size
    #add the big time frame if subgroup is larger than 1
    if num >1 :
        all_years = df.loc[(df['datetime'] >= year_to_datetime(earliest)) & (df['datetime'] < year_to_datetime(latest+1))]
        year_blocks.append( ((str(earliest)+"to"+ str(latest)), all_years))
    return year_blocks

def map_color (cluster):
    """
    Give each word cloud a unique colour palette
    Return: name of the color palette
    """

    colors = ['copper','gist_earth','viridis', 'twilight_shifted', 'Set1','Set2', 'Set3', 'Dark2']
    i = int(cluster-1) % len(colors)
    return colors[i]

def make_wordcloud (text, cluster):
    """
    Make wordcloud. Remove stop words
    Return: wordcloud for one cluster
    """

    cm = map_color (cluster)
    stopwords = set(STOPWORDS)
    stopwords.update(["present","method","based","using","used","device","invention","obtain",
                    "obtained","obtaining","lease", "includes",
                    "provided", "least one","set","determined","determine","determining",
                    "include","including", "wherein","one","following","steps",
                    "system","first","apparatus","according","second","thereof","methods"])
    # Create and generate a word cloud image:
    wordcloud = WordCloud(max_font_size=90,
                            max_words=100,
                            width=800,
                            height=600,
                            stopwords = stopwords,
                            background_color="white",
                            colormap = cm ).generate(text)
    return wordcloud


def plot_wordcloud (wordcloud,save_path,period,cluster,text):
    """
    Display the generated image and save to the output folder
    """

    plt.figure(figsize=(20, 15))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(str(save_path + period +"_cluster"+str(cluster)+"_"+text+".png"))
    plt.close()



def extract_companies (t):
    """
    extract top 100 company names for each year block
    Return: a list of tuples (companies in the cluster, cluster name)
    """

    clusters = list(t['Cluster'].unique())
    res = []
    for c in clusters:
        companies= t.loc[t.Cluster == c]["Company"].tolist()
        res.append((companies,c))
    return res


def concatenate_texts (companies,df,col):
    """
    concatenate top 100 companies' abstract and titles
    Return: (string, string)
    """

    sub = df.loc[df[col].isin(companies)]
    abstracts_ls = list(map((lambda x: str(x)),sub['Abstract'].tolist()))
    abstracts = " ".join(abstracts_ls)
    titles_ls = list(map((lambda x: str(x)),sub['Title'].tolist()))
    titles = " ".join(titles_ls)
    titles_n_abstracts = abstracts + " " + titles
    return titles, titles_n_abstracts


def make_wc_for_periods (periods,year_blocks,save_path,col):
    """
    make a word cloud for each year block
    """

    for i in range(len(year_blocks)):
        description,sub = year_blocks[i]
        period = periods[i]
        for companies, cluster in period:
            title , title_n_abstract  = concatenate_texts (companies,sub,col)
            wc1 = make_wordcloud (title,cluster)
            plot_wordcloud (wc1,save_path,description,cluster,"title")
            wc2 = make_wordcloud (title_n_abstract,cluster)
            plot_wordcloud (wc2,save_path,description,cluster,"title&abstract")

def run_word_cloud (cluster_excel, save_path, df_path,col):
    """
    Read clusters and extract the list of companies from each cluster.
    Make a word cloud for each cluster based on patent title or title & abract
    Output saved to the output folder
    """
    df = pd.read_csv (df_path, index_col= 0)
    #import cluster list
    xls = pd.ExcelFile(cluster_excel)
    #process dataframe
    earliest = int(input ("What's the earliest year?: "))
    latest = int(input ("What's the latest year?: "))
    num = int(input("How many sub-periods?: "))
    year_blocks = year_segment_wc (df,earliest,latest,num)
    periods = []
    num = len(year_blocks)
    for i in range(num):
        sheet = pd.read_excel(xls,i)
        periods.append(extract_companies(sheet))
    path = str(save_path +"/word_cloud/")
    if not os.path.exists(path):
        os.makedirs(path)
    make_wc_for_periods (periods,year_blocks,path,col)

    return None

if __name__ == "__main__":
    cluster_excel = input("Enter the path to the excel file with clusters: \n")
    save_path = input("Enter the path to the output folder:\n")
    df_path = input("Enter the path to the data (with .csv)(cleaned & merged):\n")
    
    column = input("which column are we using: \n1: Current assignees\n2: Inventors\n")
    if column == "1":
        col = "Current assignees"
    else:
        col = "Inventors"
    run_word_cloud(cluster_excel, save_path, df_path,col)

def test_word_cloud ():
    run_word_cloud ("test/test_cluster.xlsx", "test/test_output","test/test_data.csv", "Inventors")
