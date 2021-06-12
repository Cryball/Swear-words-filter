import pandas as pd
import numpy as np
import function_filter


df = pd.read_csv("app/all_func/entertainment_anime_short.csv")
val = df['1'].to_numpy()
makeitastring = ''.join(map(str, val))
result = function_filter.filter.filter(makeitastring)
print(result.count('fuck'))
