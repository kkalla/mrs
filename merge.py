# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 22:46:07 2017

@author: gyujin
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from matplotlib import pyplot as plt
import seaborn as sns
import re
import math
from collections import Counter

from subprocess import check_output

df_train = pd.read_csv('data/train.csv')
df_test = pd.read_csv('data/test.csv')
df_songs = pd.read_csv('data/songs.csv')
df_members = pd.read_csv('data/members.csv')


# info
df_train.info()
df_members.info()

# null value

df_train.isnull().sum()
df_members.isnull().sum()


# merge dfs

df_train_members = pd.merge(df_train, df_members, on='msno', how='inner')
df_train_merged = pd.merge(df_train_members, df_songs, on='song_id', how='outer')

df_test_members = pd.merge(df_test, df_members, on='msno', how='inner')
df_test_merged = pd.merge(df_test_members, df_songs, on='song_id', how='outer')

del df_train_members
del df_test_members

del df_songs
del df_members

# check length merge df & original df

df_train_merged = df_train_merged[pd.notnull(df_train_merged['msno'])]
df_test_merged = df_test_merged[pd.notnull(df_test_merged['msno'])]

print(len(df_train))
print(len(df_train_merged))

print(len(df_test))
print(len(df_test_merged))

# merged info & visualization

df_train_merged.info()

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
# def barchart fun
def bar_chart(feature):
    good = df_train_merged[df_train_merged['target']==1][feature].value_counts()
    bad = df_train_merged[df_train_merged['target']==0][feature].value_counts()
    df = pd.DataFrame([good,bad])
    df.index = ['good','bad']
    df.plot(kind='bar',stacked=True, figsize=(10,5))
    
# barchart source_system_tab, source_screen_name, source_type    
bar_chart('source_system_tab')
bar_chart('source_screen_name')
bar_chart('source_type')
bar_chart('gender')
bar_chart('city')
bar_chart('bd')

print(len(df_train))
print(len(df_train_merged))

print(len(df_test))
print(len(df_test_merged))

#--- before that save unique columns in train and test set separately ---
df_train_target = df_train_merged['target'].astype(np.int8)
df_test_id = df_test_merged['id']

#--- now dropping those columns from respective dfs ---
df_train_merged.drop('target', axis=1, inplace=True)
df_test_merged.drop('id', axis=1, inplace=True)

df_train_merged['is_train'] = 1
df_test_merged['is_train'] = 0

## handeling missing value
cols_missing_val_train = df_train_merged.columns[df_train_merged.isnull().any()].tolist()
print(cols_missing_val_train)

cols_missing_val_test = df_test_merged.columns[df_test_merged.isnull().any()].tolist()
print(cols_missing_val_test)

#source_system_tab

df_train_merged.source_system_tab = df_train_merged.source_system_tab.fillna('others')
df_test_merged.source_system_tab = df_test_merged.source_system_tab.fillna('others')

# source_screen_name
source_screen_name_uniq_train = list(df_train_merged.source_screen_name.unique())
source_screen_name_uniq_test = list(df_test_merged.source_screen_name.unique())

#--- common values ---
print(set(source_screen_name_uniq_train) & set(source_screen_name_uniq_test))

#--- different values ---
print(set(source_screen_name_uniq_train) ^ set(source_screen_name_uniq_test))   
df_train_merged.source_screen_name = df_train_merged.source_screen_name.fillna('other_sources')
df_test_merged.source_screen_name = df_test_merged.source_screen_name.fillna('other_sources')

df_test_merged['source_screen_name'] = df_test_merged['source_screen_name'].replace(['People local', 'People global'], 'other_sources')

# source_type
df_train_merged.source_type = df_train_merged.source_type.fillna('other_types')
df_test_merged.source_type = df_test_merged.source_type.fillna('other_types')

# gender
df_test_merged.gender = df_test_merged.gender.fillna('unknown')
df_train_merged.gender = df_train_merged.gender.fillna('unknown')

# song_length
df_train_merged['song_length'].fillna((df_train_merged['song_length'].mean()), inplace=True)
df_test_merged['song_length'].fillna((df_test_merged['song_length'].mean()), inplace=True)

# language

df_train_merged.language = df_train_merged.language.fillna(0)
df_test_merged.language = df_test_merged.language.fillna(0)

# genre_ids

#--- List containing unique genre_ids from column inclusive of combinations ---
genre = df_train_merged.genre_ids.unique().tolist()

#--- List containing unique individual genre_ids ---
genre_new = []

for i in range(len(genre)):
    if (type(genre[i]) == str):      #--- to avoid the nan type---
        lw = genre[i].split('|')
        #lw = re.findall(r"[^|]+", genre[i])
        for j in range(len(lw)):
            genre_new.append(lw[j])
            
print(len(genre_new))
print(len(set(genre_new)))
 
letter_counts = Counter(genre_new)
dfoo = pd.DataFrame.from_dict(letter_counts, orient='index')
dfoo.plot(kind='bar', figsize=(30,15), title = 'Distribution of frequency of genre_ids')

genre = df_train_merged.genre_ids.unique().tolist()

genre_new = []
for i in range(len(genre)):
    if (type(genre[i]) == str):
        lw = genre[i].split('|')
        #lw = re.findall(r"[^|]+", genre[i])
        for j in range(len(lw)):
            genre_new.append(lw[j])

print('Number of unique genre ids in train set: ',len(genre))

genre_new = set(genre_new)
print('Number of unique genre ids after splitting them individually: ', len(genre_new))

print('Genre ids used in combination with other genres: ', len(set(genre) & set(genre_new)))
#print('Genre ids NOT present in both train set OR after splitting: ', len(set(genre) ^ set(genre_new)))

print('Genre ids not used in combination with other genres', len(genre_new - (set(genre) & set(genre_new))))

genre_test = df_test_merged.genre_ids.unique().tolist()

genre_test_new = []
for i in range(len(genre_test)):
    if (type(genre_test[i]) == str):
        lw = genre_test[i].split('|')
        #lw = re.findall(r"[^|]+", genre[i])
        for j in range(len(lw)):
            genre_test_new.append(lw[j])

print('Number of unique genre ids in train set: ',len(genre_test))

genre_test_new = set(genre_test_new)
print('Number of unique genre ids after splitting them individually: ', len(genre_test_new))

print('Genre ids used in combination with other genres: ', len(set(genre_test) & set(genre_test_new)))
#print('Genre ids NOT present in both train set OR after splitting: ', len(set(genre) ^ set(genre_new)))

print('Genre ids not used in combination with other genres', len(genre_test_new - (set(genre_test) & set(genre_test_new))))

#--- combination of genre_ids in train and test ---
print('Genre_ids combinations present in both train and test set: ', len(set(genre_test) & set(genre)))

print('Genre_ids combinations present in test but not in train set: ', len(set(genre_test) - (set(genre_test) & set(genre))))
#--- Intersection between unique genre_ids in train and test set ---
print('Genre_ids present in both train and test set: ', len(set(genre_test_new) & set(genre_new)))

print('New genre_ids present in both train or test set: ', len(set(genre_test_new) ^ set(genre_new)))

print('Total number of unique genre_ids present in both train and test set: ', len(set(genre_test_new) | set(genre_new)))
print('rows without Nan values:', df_train_merged.genre_ids.count())      
print('rows with Nan values: ', len(df_train_merged) - df_train_merged.genre_ids.count() )    

genre = df_train_merged[['song_id', 'genre_ids']]          #--- df containing all song id and artists ---
genre_wo_nan = genre.drop_duplicates().ix[~df_train_merged['genre_ids'].isnull(), :]       #--- df with unique song id and artist name where artist name is not nana
genre_w_nan = genre.drop_duplicates().ix[df_train_merged['genre_ids'].isnull(), :]          #--- df with unique song id and artist name where artist name is nan

#--- if it is zero means there are no intersections between 
print('Whether intersections are present or not : ',np.intersect1d(genre_wo_nan['song_id'], genre_w_nan['song_id']) )

df_train_merged.genre_ids = df_train_merged.genre_ids.fillna('no_genre_id')
df_test_merged.genre_ids = df_test_merged.genre_ids.fillna('no_genre_id')

# composer

composer = df_train_merged.composer.unique().tolist()

composer_new = []
for i in range(len(composer)):
    if (type(composer[i]) == str):
        lw = composer[i].split('|')
        #lw = re.findall(r"[^|]+", genre[i])
        for j in range(len(lw)):
            composer_new.append(lw[j])

print('Number of unique composers in train set: ',len(composer))

composer_new = set(composer_new)
print('Number of unique composers after splitting them individually: ', len(composer_new))

print('composers in combination with other composers: ', len(set(composer) & set(composer_new)))
#print('Genre ids NOT present in both train set OR after splitting: ', len(set(genre) ^ set(genre_new)))

print('composers not in combination with other composers', len(composer_new - (set(composer) & set(composer_new))))

composer_test = df_test_merged.composer.unique().tolist()

composer_test_new = []
for i in range(len(composer_test)):
    if (type(composer_test[i]) == str):
        lw = composer_test[i].split('|')
        #lw = re.findall(r"[^|]+", genre[i])
        for j in range(len(lw)):
            composer_test_new.append(lw[j])

print('Number of unique composers in train set: ',len(composer_test))

composer_test_new = set(composer_test_new)
print('Number of unique composers after splitting them individually: ', len(composer_test_new))

print('composers used in combination with other composers: ', len(set(composer_test) & set(composer_test_new)))
#print('Genre ids NOT present in both train set OR after splitting: ', len(set(genre) ^ set(genre_new)))

print('composers not used in combination with other composers', len(composer_test_new - (set(composer_test) & set(composer_test_new))))

#--- Intersection between unique composers in train and test set ---
print('composers present in both train and test set: ', len(set(composer_test_new) & set(composer_new)))

print('New composers present in both train or test set: ', len(set(composer_test_new) ^ set(composer_new)))

print('Total number of unique composers present in both train and test set: ', len(set(composer_test_new) | set(composer_new)))


print('rows without Nan values:', df_train_merged.composer.count())      
print('rows with Nan values: ', len(df_train_merged) - df_train_merged.composer.count() )    

composer = df_train_merged[['song_id', 'composer']]          #--- df containing all song id and artists ---
composer_wo_nan = composer.drop_duplicates().ix[~df_train_merged['composer'].isnull(), :]       #--- df with unique song id and artist name where artist name is not nana
composer_w_nan = composer.drop_duplicates().ix[df_train_merged['composer'].isnull(), :]          #--- df with unique song id and artist name where artist name is nan

#--- if it is zero means there are no intersections between 
print('Whether intersections are present or not : ',np.intersect1d(composer_wo_nan['song_id'], composer_w_nan['song_id']) )

df_train_merged.composer = df_train_merged.composer.fillna('no_composer')
df_test_merged.composer = df_test_merged.composer.fillna('no_composer')

# artist name
df_train_merged.artist_name = df_train_merged.artist_name.fillna('no_artist')
df_test_merged.artist_name = df_test_merged.artist_name.fillna('no_artist')

# lyricist

lyricist = df_train_merged.lyricist.unique().tolist()

lyricist_new = []
for i in range(len(lyricist)):
    if (type(lyricist[i]) == str):
        lw = lyricist[i].split('|')
        #lw = re.findall(r"[^|]+", genre[i])
        for j in range(len(lw)):
            lyricist_new.append(lw[j])

print('Number of unique lyricists in train set: ',len(lyricist))

lyricist_new = set(lyricist_new)
print('Number of unique lyricists after splitting them individually: ', len(lyricist_new))

print('lyricists in combination with other lyricists: ', len(set(lyricist) & set(lyricist_new)))
#print('Genre ids NOT present in both train set OR after splitting: ', len(set(genre) ^ set(genre_new)))

print('lyricists not in combination with other lyricists', len(lyricist_new - (set(lyricist) & set(lyricist_new))))

lyricist_test = df_test_merged.lyricist.unique().tolist()

lyricist_test_new = []
for i in range(len(lyricist_test)):
    if (type(lyricist_test[i]) == str):
        lw = lyricist_test[i].split('|')
        #lw = re.findall(r"[^|]+", genre[i])
        for j in range(len(lw)):
            lyricist_test_new.append(lw[j])

print('Number of unique lyricists in _test set: ',len(lyricist_test))

lyricist_test_new = set(lyricist_test_new)
print('Number of unique lyricists after splitting them individually: ', len(lyricist_test_new))

print('lyricists in combination with other lyricists: ', len(set(lyricist_test) & set(lyricist_test_new)))
#print('Genre ids NOT present in both train set OR after splitting: ', len(set(genre) ^ set(genre_new)))

print('lyricists not in combination with other lyricists', len(lyricist_test_new - (set(lyricist_test) & set(lyricist_test_new))))

#--- Intersection between unique lyricists in train and test set ---
print('lyricists present in both train and test set: ', len(set(lyricist_test_new) & set(lyricist_new)))

print('New lyricists present in both train or test set: ', len(set(lyricist_test_new) ^ set(lyricist_new)))

print('Total number of unique lyricists present in both train and test set: ', len(set(lyricist_test_new) | set(lyricist_new)))

print('rows without Nan values:', df_train_merged.lyricist.count())      
print('rows with Nan values: ', len(df_train_merged) - df_train_merged.lyricist.count() )    

lyricist = df_train_merged[['song_id', 'lyricist']]          #--- df containing all song id and artists ---
lyricist_wo_nan = lyricist.drop_duplicates().ix[~df_train_merged['lyricist'].isnull(), :]       #--- df with unique song id and artist name where artist name is not nana
lyricist_w_nan = lyricist.drop_duplicates().ix[df_train_merged['lyricist'].isnull(), :]          #--- df with unique song id and artist name where artist name is nan

#--- if it is zero means there are no intersections between 
print('Whether intersections are present or not : ',np.intersect1d(lyricist_wo_nan['song_id'], lyricist_w_nan['song_id']) )

df_train_merged.lyricist = df_train_merged.lyricist.fillna('no_lyricist')
df_test_merged.lyricist = df_test_merged.lyricist.fillna('no_lyricist')
























