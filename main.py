# import library
from typing import Union
from pydantic import BaseModel
import streamlit as st
import pymongo
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import toml
import pandas as pd

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    uri = st.secrets['mongo']['uri']
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client
client = init_connection()

# global variables, specify db and collection to get and post to
db = client["automation"]
collection = db["date"]

# Get the current date and time, this will be the data that we will be working with and can be replaced with any other data
def date():
    current_datetime = datetime.now()
    # format to provide standard time %I and AM or PM %p
    formatted_datetime = current_datetime.strftime("%m-%d-%Y %I:%M:%S.%f %p")
    print(current_datetime)
    print(formatted_datetime)
    return formatted_datetime
formatted_datetime = date()

# Insert data into MongoDB
def insert_data(time):
    data = {"timestamp": time}
    collection.insert_one(data)
insert_data(formatted_datetime)

# obtain the udpated database information for end-user viewing
# Uses st.cache_data to only rerun when the query changes
def get_data(db,connection):
    items = collection.find()
    items = list(items)  # make hashable for st.cache_data
    #create dataframe
    df = pd.DataFrame(items, columns= ['_id', 'timestamp'])
    del df['_id']
    return df
df = get_data(db,collection)

# print results for user at end-location
st.write("""This table is fully automated. 
            The timestamp data is being updated everytime the code is run.
            The data is then stored and updated in a datebase.
            The data is then pulled from the database and presented to the end user.
            Prefect Automation and Orchestration is used to carry out automation step and 
            demonstrates that a no-touch solution is possible.""")
st.dataframe(df)