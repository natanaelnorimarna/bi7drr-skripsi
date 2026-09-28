import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Membaca data BI7DRR (Bank Indonesia 7 Days Reverse Repo Rate)
df = pd.read_csv('BI-7Day-RR (CSV)')
r_data = df['BI-7Day-RR'].values
