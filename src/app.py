import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Fetch the webpage
url = 'https://ycharts.com/companies/TSLA/revenues'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
response = requests.get(url, headers=headers)

# Check if the request was successful

if response.status_code != 200:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    exit()

print("RESPONSE STATUS IS: ", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all('table', class_='table')

dataframes = []

# parse each table
for i, table in enumerate(tables):
    print(f"Table {i + 1}: ")

    thead = table.find('thead')
    if thead:
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]
    else:
        headers = None

    #Extract table rows
    rows = table.find('tbody').find_all('tr')
    table_data = []
    for row in rows:
        columns = [td.text.strip() for td in row.find_all('td')]
        table_data.append(columns)

    df = pd.DataFrame(table_data, columns=headers)
    dataframes.append(df)

    print("Table {i+1} DataFrame: ")
    print(df)
    print("\n")

    combined_df = pd.concat(dataframes, ignore_index=True)
    print("Combined DataFrame: ")
    print(combined_df)