# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt



tki_data = pd.read_csv("/Users/elwadgedleh/Downloads/octagon_dataset.csv")

print(tki_data.head())
missingvalues= tki_data.isnull().sum()
all_patients=tki_data.loc[(tki_data.Prov=="ALL") & (tki_data.Con_ACT == "ALL") & (tki_data.Sex == "ALL") & (tki_data.Age == "ALL")]

all_patientTxC = all_patients.loc[(all_patients.Measure=="Tx") | (all_patients.Measure=="censored")]

all_patients_monthlyCon=all_patientTxC.iloc[:,5:]

x= ((all_patients_monthlyCon.iloc[0,1] - all_patients_monthlyCon.iloc[0,2]) / all_patients_monthlyCon.iloc[0,1])


to_graph1=all_patients_monthlyCon
to_graph2= all_patients_monthlyCon


print("---------------------------------------------------")
for x in range (40):
    if (x==0): 
        diff= 0
        to_graph1[ str(x)] = diff
    else: 
        diff= all_patients_monthlyCon.iloc[1,x]/all_patients_monthlyCon.iloc[0,x-1]
        to_graph1[str(x)] = diff
    
    
   
   

print("Based on Previous")
print(to_graph1.iloc[0,40:])
print("Total monthly rates")
graphTrial= to_graph1.iloc[0,40:]
print(graphTrial.sum())
plt.figure(figsize=(16,9))
sns.set_palette(sns.color_palette('hls', 7))
plt.title("Proportion of Participants that Discontinue Treatment Over Time, monthly", fontsize=30)
plt.xlabel("Month",fontsize=20)
plt.ylabel("Discontinuity Rate", fontsize=20)
sns.lineplot(data=graphTrial, sort=False)

