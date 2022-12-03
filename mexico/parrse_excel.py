import pandas as pd
import numpy as np
import re
#arg = re.compile(r"(\nYou're eligible for a Genius discount.*all you have to do is sign in.)")
#df1 = pd.read_excel('copia_78.xlsx')
#df_1 = pd.read_excel('argentina_second.xlsx')
#print(df1)

df_1 = pd.read_excel("Third_step.xlsx")
df = pd.read_excel('mexico_first_step.xlsx')
df1 = df.drop_duplicates(keep='first')
df2 = df1.dropna()
print(df2)
#df_1 = df_1.str.contains('ñ', regex=False)
#df_arg = pd.concat([df_new, df_1_new], axis=0)
#df = df[df["Description"].str.contains("ñ|Ñ") == False]
#df = df[df["Listing_url"].str.contains("ñ|Ñ") == False]
#df = df[df["Themes"].str.contains("ñ|Ñ") == False]
#df = df[df["Title"].str.contains("ñ|Ñ") == False]
#df_1 = df1[df1["Description"].str.contains("ñ|Ñ|á|é|í|ó|ú") == False]
#df_1 = df1[df1["Listing_url"].str.contains("ñ|Ñ|á|é|í|ó|ú") == False]
#df_1 = df1[df1["Themes"].str.contains("ñ|Ñ|á|é|í|ó|ú") == False]
#df_1 = df1[df1["Title"].str.contains("ñ|Ñ|á|é|í|ó|ú") == False]
df3 = df2[df2["Description"].str.contains("á|é|í|ó|ú|ñ|ü", case=False) == False]
df4 = df3[df3["Listing_url"].str.contains("á|é|í|ó|ú|ñ|ü", case=False) == False]
df5  = df4[df4["Themes"].str.contains("á|é|í|ó|ú|ñ|ü", case=False) == False]
df6 = df5[df5["Title"].str.contains("á|é|í|ó|ú|ñ|ü", case=False) == False]

#df_1 = df_1.drop_duplicates()
#print(df_1)
print(df6)
new_df = pd.concat([df6, df_1], axis=0)
print(new_df)
new_df1 = new_df.drop_duplicates(keep='first').dropna()
print(new_df1)



new_df1.to_excel('Third_step.xlsx')
