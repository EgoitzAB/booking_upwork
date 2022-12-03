import pandas as pd
import re




df = pd.read_excel("mexico_first_step.xlsx")
print(df)
df = df.drop_duplicates().dropna()
df.to_excel("mexico_second_step.xlsx", index=0)
