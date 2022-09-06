import bonobo
import csv
import argparse
import numpy as np
import pandas as pd
# Uploading a File
'''
ap = argparse.ArgumentParser(conflict_handler="resolve")
#ap.set_conflict_handler("resolve")
#parser = OptionParser(conflict_handler="resolve")
ap.add_argument("-i", "--csv", required=True,
    help="path to input csv")

ap.add_argument("-r", "--output_file_name", required=True,
    help="path to output file")
args = vars(ap.parse_args())
'''

#Extracting the csv
def extract():
    file = open("20220419_new_orders_to_rpac.csv")
    reader = csv.DictReader(file)
    lis = []
    for row in reader:
        lis.append(row)
    #Creating a DataFrame
    df = pd.DataFrame(lis)
    yield df

#Transforming CSV
def transform(df):
    #Groupby on Similiar Group
    df['Quantity'] = df['Quantity'].astype('str') 
    df1 = df.groupby('hr_order_number').agg({'Hrid':'first','Location Name':'first','Attention':'first','Address 1':'first',
                                        'Address 2':'first','City':'first','State':'first','Zipcode':'first','Country':'first',
                                        'Phone':'first','Email':'first','Quantity':', '.join,'Item Code1':', '.join,
                                        'Item Code2':'first','Item Code3':'first','Item Code4':'first'}).reset_index()
    # Saving the Result in csv
    df1[["Quantity1","Quantity2"]] = df1['Quantity'].str.split(",", 1, expand = True)
    df1[["Item Code1_1","Item Code1_2"]] = df1['Item Code1'].str.split(",", 1, expand = True)
    df2 = df1.drop("Quantity", axis = 'columns')
    output = df2.to_json("20220419_new_orders_to_rpac.json",orient = 'records')


graph = bonobo.Graph(
    extract,
    transform
    )


# The __main__ block actually execute the graph.
if __name__ == '__main__':
    bonobo.run(graph)
