"""
Function to export all publication numbers of the cleaned & merged dataset in txt files.
User can upload the txt files to the online database to retrieve additional information
"""
import pandas as pd

def ExportPublicationNumbers (csv,save_path):
    #make multiple documents each 46k long
    df = pd.read_csv(csv)
    num = df['Earliest publication number'].to_list()
    chunks = [num[x:x+46000] for x in range(0, len(num), 46000)]
    for c in range(len(chunks)): 
        path = save_path +'/'+ "publication_number_"+str(c)+ '.txt'
        with open(path, 'w') as f:
            for item in chunks[c]:
                f.write(item + "\n")
    return None

if __name__ == "__main__":
    csv = input("Enter the path to the csv file (with extension):\n")
    path = input("Enter the path to the output folder:\n")
    ExportPublicationNumbers (csv, path)