import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Drop table in SQLite if it already exist
c.execute('DROP TABLE IF EXISTS raw_data')

# Create table in SQLite to hold data
c.execute('''CREATE TABLE raw_data 
             (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT)''')

# Insert sample data  
c.executemany("INSERT INTO raw_data VALUES (?, ?, ?, ?)", 
              [(1, 'John', 36, 'Male'), 
               (2, 'Sarah', 17, 'Female')])
# Commit changes
conn.commit() 

# Read data from SQLite into Pandas DataFrame
df = pd.read_sql_query("SELECT * from raw_data", conn)

print(df)

# Clean the data (processing steps would go here)
#
df['age_group'] = pd.cut(df.age, bins=[0, 18, 35, 100], 
                         labels=['Youth', 'Young Adult', 'Middle Aged'])

# Export cleaned DataFrame back to SQLite table
df.to_sql('clean_data', conn, if_exists='replace') 

print(df)
# Close connection
conn.close()

# Now the cleaned data is available in the SQLite database 

#Data Analyst and Data Scientist Role
# for further analysis, reporting, dashboarding etc