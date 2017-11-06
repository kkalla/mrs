import pandas as pd
train = pd.read_csv('C:\\Users\\gyujin\\Desktop\\kaggle data\\train.csv')
members = pd.read_csv('C:\\Users\\gyujin\\Desktop\\kaggle data\\members.csv')

# info
train.info()
members.info()

# null value

train.isnull().sum()
members.isnull().sum()

# visualization

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
# def barchart fun
def bar_chart(feature):
    good = train[train['target']==1][feature].value_counts()
    bad = train[train['target']==0][feature].value_counts()
    df = pd.DataFrame([good,bad])
    df.index = ['good','bad']
    df.plot(kind='bar',stacked=True, figsize=(10,5))
    
# barchart source_system_tab, source_screen_name, source_type    
bar_chart('source_system_tab')
bar_chart('source_screen_name')
bar_chart('source_type')
