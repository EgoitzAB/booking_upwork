import pandas as pd
import numpy as np
import re
#arg = re.compile(r"(\nYou're eligible for a Genius discount.*all you have to do is sign in.)")
#df1 = pd.read_excel('copia_78.xlsx')
#df_1 = pd.read_excel('argentina_second.xlsx')
#print(df1)

df = pd.read_excel("final_english_2000_arg.xlsx")
df1 = df.drop_duplicates(keep='first')
df2 = df1.dropna()




df3 = df2[df2["Description"].str.contains("á|é|í|ó|ú|ñ|ü", case=False) == False]
df4 = df3[df3["Listing_url"].str.contains("á|é|í|ó|ú|ñ|ü", case=False) == False]
df5  = df4[df4["Themes"].str.contains("á|é|í|ó|ú|ñ|ú", case=False) == False]
df6 = df5[df5["Title"].str.contains("á|é|í|ó|ú|ñ|ü", case=False) == False]

df6.to_excel("final_english_2000_arg.xlsx")
