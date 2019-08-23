#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


pd.__version__


# In[2]:


import sys, sqlite3, pandas as pd
files = ['C:/Users/lianj/Desktop/Kaggle competition/Housing price/train.csv', 
         'C:/Users/lianj/Desktop/Kaggle competition/Housing price/train_modify.csv'] #these are the arguments we take
df1 = pd.read_csv(files[0])
df2 = pd.read_csv(files[1])
df3 = (df1 != df2).any(axis=None)
print('Differences in file:', df3)
df3 = (df1 != df2).any(1)
ne_stacked = (df1 != df2).stack()
changed = ne_stacked[ne_stacked]
changed.index.names = ['id', 'col']
print('Differences In:')
print(changed)


# In[3]:


df3 = df1.eq(df2)
print(df3.all())
#print(df3.all(axis=1))
df4 = df3.all(axis=1)
df4 = pd.DataFrame(df4, columns=['Columns'])
print(df4[df4['Columns']==False])


# In[4]:


#This is the correct mismtaching column


conn = sqlite3.connect(':memory:') #we are spinning an SQL db in memory
cur = conn.cursor()
chunksize = 10000
i=0
for file in files:
    i = i+1
    for chunk in pd.read_csv(file, chunksize=chunksize): #load the file in chunks in case its too big
        chunk.columns = chunk.columns.str.replace(' ', '_') #replacing spaces with underscores for column names
        chunk.to_sql(name='file' + str(i), con=conn, if_exists='append')
print('Comparing', files[0], 'to', files[1]) #Compare if all data from File[0] are present in File[1]
cur.execute( '''SELECT * FROM File1
                EXCEPT
                SELECT * FROM File2''')
i=0
for row in cur:
    print(row)
    i=i+1
if i==0: print('No Differences')
print('Comparing', files[1], 'to', files[0]) #Compare if all data from File[1] are present in File[0]
cur.execute( '''SELECT * FROM File2
                EXCEPT
                SELECT * FROM File1''')
i=0
for row in cur:
    print(row)
    i=i+1
if i==0: print('No Differences')
cur.close()


# In[ ]:




