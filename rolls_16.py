from numpy import random
import pandas as pd
result = []
for roll_set in range(0,100000):
    roll_a = random.randint(1,7)
    roll_b = random.randint(1,7)
    temp_result = 6*int((roll_a-1)/2) + roll_b
    if temp_result <= 16: 
        result.append(temp_result)
    

  
df = pd.Series(result).value_counts().reset_index().sort_values('index').reset_index(drop=True)
print(df)
