import pandas as pd
import re




df = pd.read_excel("argentina_first_step.xlsx")
print(df)
df = df.drop_duplicates().dropna()
df.to_excel("Upwork_second_step.xlsx", index=0)
