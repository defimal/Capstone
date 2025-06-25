## importing necessary libraries 

import pandas as pd

df = pd.read_csv("data/raw/test.csv")

## creating a stagging of df to make channges in the files

duplicates = df.duplicated()

##now i will check the total number of rows

print("total number of rows ", duplicates.sum())

## these cod help us to see the duplicate if any :
df_duplicates = df[df.duplicated()]
print(df_duplicates)
## now wwe drop any duplicates in this file 
df_no_duplicates = df.drop_duplicates()

##so now we mad sure there is no duplicates

## next is to remove all trailing spaces 

df = df_no_duplicates.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
print(df)
print(df["country"].unique())
print(df["Country"].value_counts(dropna=False))

