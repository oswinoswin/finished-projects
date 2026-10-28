import pandas as pd
import bs4
import os
print(os.getcwd())
for i in range(44):
    with open(f"../data/{i}.txt", "r") as f:
        advert_text = f.read()
        print(advert_text)

