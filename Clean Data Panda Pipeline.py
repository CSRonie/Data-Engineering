import sqlite3
import pandas as pd


conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS Customer')


df = pd.read_excel(r"C:\Users\My PC\Downloads\Data Eng\Customer Call List.xlsx")

df.to_sql('RawCustomer', conn, if_exists='replace') 

#Retain 1 row of all duplicates
df = df.drop_duplicates()

#Remove Column
df = df.drop(columns="Not_Useful_Column")

#Strip Usage
df['Last_Name'] = df['Last_Name'].str.strip("123._/ ")

#Regex Usage
df['Phone_Number'] = df['Phone_Number'].str.replace('[^a-zA-Z0-9]','',regex=True)

#Clean Phone Number
df['Phone_Number'] = df['Phone_Number'].apply(lambda x: str(x))
df['Phone_Number'] = df['Phone_Number'].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])
df['Phone_Number'] = df['Phone_Number'].str.replace('nan--','')
df['Phone_Number'] = df['Phone_Number'].str.replace('Na--','')


#Clean Paying Customer and Do not Contact Column
df["Paying Customer"] = df["Paying Customer"].str.replace('Yes','Y')
df["Paying Customer"] = df["Paying Customer"].str.replace('No','N')
df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace('Yes','Y')
df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace('No','N')


#remove Nan or text Nan
df = df.replace('N/a','')
df = df.replace('NaN','')
df=df.fillna('')


#remove do not contact customer
for x in df.index:
    if df.loc[x, "Do_Not_Contact"] == 'Y':
        df.drop(x, inplace=True)

#remove do not contact customer for no response
for x in df.index:
    if df.loc[x, "Do_Not_Contact"] == '':
        df.drop(x, inplace=True)

#reset index
df = df.reset_index(drop=True)


# Export cleaned DataFrame back to SQLite table
df.to_sql('Customer', conn, if_exists='replace') 

# Close connection
conn.close()

print(df)
