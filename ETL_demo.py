import csv
import numpy as np
import pandas as pd
import json

# Deployment Libraries
import streamlit as st

#Title
st.title('ETL Demo')
st.write('CSV to Json')

# Function to Split a Feature

def split(Feature_Name, New_Name1, New_Name2):
    df = pd.read_csv('Transformed_20220419_new_orders_to_rpac.csv')
    df[[New_Name1, New_Name2]] = df[Feature_Name].str.split(",", 1, expand = True)
    csv = df.to_csv('Transformed_20220419_new_orders_to_rpac.csv', index = None)
    json = df.to_json("20220419_new_orders_to_rpac.json", orient = 'records')
    return df

# Function to apply padding
def pad(PFeature_Name):
    lis = list(PFeature_Name)
    lis.insert(2, " ")
    s = ""
    for i in lis:
        s += i
    return s

# Function to call the padding function
def apply_pad(PFeature_Name, New_Name):
    df = pd.read_csv('Transformed_20220419_new_orders_to_rpac.csv')
    df[New_Name] = df[PFeature_Name].apply(pad)
    csv = df.to_csv('Transformed_20220419_new_orders_to_rpac.csv', index = None)
    json = df.to_json("20220419_new_orders_to_rpac.json", orient = 'records')
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

# Upload the file
uploaded_file = st.file_uploader("Choose your file CSV:", type=['csv'], accept_multiple_files = False)

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
        json = df.to_json("20220419_new_orders_to_rpac.json", orient = 'records')

        return df

    #Tranforming
    if st.sidebar.button("Transform"):
        df = transform(extract())
        st.markdown('Transformed CSV')
        st.write(df.head())
        st.write()

    if st.sidebar.button("Split A Feature"):
        df = split(Feature_Name, New_Name1, New_Name2)
        st.markdown('Splited CSV')
        st.write(df.head())

    if st.sidebar.button("ADD a Padding"):
        df = apply_pad(PFeature_Name,New_Name)
        st.markdown('Padded CSV')
        st.write(df.head())

   try:
        with open("20220419_new_orders_to_rpac.json", "r") as f:
            data_columns = json.load(f)
            st.write(data_columns[:1])
    except:
        pass
        
else:
    st.write('Please Upload a File')

