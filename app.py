import csv
import numpy as np
import pandas as pd
import json
from io import BytesIO
# Deployment Libraries
import streamlit as st

#Title
st.title('ETL Demo')
st.write('CSV to Json')


# Upload the file
uploaded_file = st.file_uploader("Choose your file CSV:", type=['csv'], accept_multiple_files = False)


## Converting df to csv
def convert_df(df):
   return df.to_csv().encode('utf-8')

# Function to Split a Feature
def split(Feature_Name, New_Name1, New_Name2):
    df = pd.read_csv('Transformed_20220419_new_orders_to_rpac.csv')
    df[[New_Name1, New_Name2]] = df[Feature_Name].str.split(",", 1, expand = True)
    csv = df.to_csv('Transformed_20220419_new_orders_to_rpac.csv', index = None)
    #json = df.to_json("20220419_new_orders_to_rpac.json", orient = 'records')

    return df

# Function to apply padding
def Npad(NOS):
    lis = []
    s = ""
    n = int(NOS)
    for i in range(0, n):
        ele = " "
        lis.append(ele)
    srt = s.join(lis)
    return srt

def add_pad(PFeature_name, NOS):
    lst = list(PFeature_name)
    s = Npad(NOS)
    lis = []
    for i in lst:
        ss = s + "" + i
        lis.append(ss)
    return lis

def apply_pad(PFeature_name, New_Name, NOS):
    try:
        df = pd.read_csv('Transformed_20220419_new_orders_to_rpac.csv')
        if PFeature_name == New_Name:
            st.error("Enter the name different from feature name")
        L = add_pad(df[PFeature_name], NOS)
        df[New_Name] = L
        csv = df.to_csv('Transformed_20220419_new_orders_to_rpac.csv', index = None)
        #json = df.to_json("20220419_new_orders_to_rpac.json", orient = 'records')

        return df
    except:
        df = pd.read_csv("20220419_new_orders_to_rpac.csv")
        if PFeature_name == New_Name:
            st.error("Enter the name different from feature name")
        L = add_pad(df[PFeature_name], NOS)
        df[New_Name] = L
        csv = df.to_csv('Transformed_20220419_new_orders_to_rpac.csv', index = None)
        #json = df.to_json("20220419_new_orders_to_rpac.json", orient = 'records')

        return df

#Buttons
st.sidebar.title('User Controls')

st.sidebar.write('Input for Split Function')
Feature_Name = st.sidebar.text_input(label = 'Enter the Feature Name Which You Want to Split')
New_Name1 = st.sidebar.text_input(label = 'Enter the Name for New Feature 1')
New_Name2 = st.sidebar.text_input(label = 'Enter the Name for New Feature 2')

st.sidebar.write('Input for Padding Function')
PFeature_Name = st.sidebar.text_input(label = 'Enter the Feature Name Which You Want to Add Padding')
New_Name = st.sidebar.text_input(label = 'Enter the Name for New Feature')
NOS  = st.sidebar.text_input(label = 'Enter the No of Padding You Want')


if uploaded_file is not None:
    #Converting the file into DataFrame
    CSV = pd.read_csv(uploaded_file)

    #Printing the csv
    st.markdown('Original CSV')
    st.write(CSV.head())  

    #Extracting the csv
    def extract():
        file = open(uploaded_file.name)
        reader = csv.DictReader(file)
        lis = []
        for row in reader:
            lis.append(row)
        #Creating a DataFrame
        df = pd.DataFrame(lis)
        return df

    #Transforming CSV
    def transform(df):
        #Groupby on Similiar Group
        df['Quantity'] = df['Quantity'].astype('str') 
        df = df.groupby('hr_order_number').agg({'Hrid':'first','Location Name':'first','Attention':'first','Address 1':'first',
                                            'Address 2':'first','City':'first','State':'first','Zipcode':'first','Country':'first',
                                            'Phone':'first','Email':'first','Quantity':', '.join,'Item Code1':', '.join,
                                            'Item Code2':'first','Item Code3':'first','Item Code4':'first'}).reset_index()
        csv = df.to_csv('Transformed_20220419_new_orders_to_rpac.csv', index = None)
        #json = df.to_json("20220419_new_orders_to_rpac.json", orient = 'records')

        return df

    #Tranforming
    
    if st.sidebar.button("Transform"):
        try:
            df = transform(extract())
            st.markdown('Transformed CSV')
            st.write(df.head())
            #Download
            csv_dwnld = convert_df(df)
            st.download_button("Press to Download", csv_dwnld,"Transformed.csv","text/csv",key='download-csv')
            st.write()

        except ValueError:
            st.error("Please Input Number Value")

        except KeyError:
            st.error("Feature Does not Exist")

        except AttributeError:
            pass
    
    if st.sidebar.button("Split A Feature"):
        try:
            df = split(Feature_Name, New_Name1, New_Name2)
            st.markdown('Splited CSV')
            st.write(df.head())
            #Download
            csv_dwnld = convert_df(df)
            st.download_button("Press to Download", csv_dwnld,"Transformed.csv","text/csv",key='download-csv')

        except ValueError:
            st.error("Please Input Number Value")

        except KeyError:
            st.error("Feature Does not Exist")

        except AttributeError:
            pass

    if st.sidebar.button("ADD a Padding"):
        try:
            df = apply_pad(PFeature_Name, New_Name, NOS)
            st.markdown('Padded CSV')
            st.write(df.head())
            #Download
            csv_dwnld = convert_df(df)
            st.download_button("Press to Download", csv_dwnld,"Transformed.csv","text/csv",key='download-csv')

        except ValueError:
            st.error("Please Input Number Value")

        except KeyError:
            st.error("Feature Does not Exist")

        except AttributeError:
            pass
    try:
        with open("20220419_new_orders_to_rpac.json", "r") as f:
            data_columns = json.load(f)
            st.write(data_columns[:1])

    except:
        pass
else:
    st.write('Please Upload a File')

