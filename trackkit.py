
# coding: utf-8

# In[256]:

from bs4 import BeautifulSoup as bs
import urllib2
import pandas as pd
pd.set_option('display.max_columns', None)


csv_data = []

for page_number in range(1,481):
    print "Now analysing page: " , page_number
    target = 'http://www.trackitt.com/usa-immigration-trackers/i140/page/' + str(page_number)
    html = urllib2.urlopen(target)
    soup = bs(html,"html.parser")
    table = soup.find("table",{"id":"myTable01"})
    trs = table.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        temp = []
        for td in tds:
            inner_text = td.text
            strings = inner_text.split("\n")
            temp.extend(strings)
        csv_data.append(temp)
        
csv_data =[x for x in csv_data if len(x) == 30]
for sublist in csv_data:
    del sublist[4]
    del sublist[2]
#print csv_data[0], len(csv_data[0])

ths = trs[0].find_all('th')
table_header = []
for th in ths:
    th_content = th.text.lstrip().rstrip()
    strings = th_content.split("\n")
    table_header.extend(string for string in strings if string)

#print table_header,len(table_header)


# In[280]:

df = pd.DataFrame(csv_data , columns = table_header)


# In[261]:

df.to_csv('trackitt.csv', sep = ',', encoding = 'utf-8')  


# In[493]:

import os
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def get_path(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir,filename)
    return file_path

def read_csv(filepath):
    data = []
    input_file = open(filepath,'rU')
    input_file_object = csv.reader(input_file)
    header = input_file_object.next()
    for row in input_file_object:
        data.append(row)
    data = np.array(data)
    return data
    
def read_as_pd(filepath):
    data_frame = pd.read_csv(filepath)
    return data_frame
    
input_file_path = get_path('trackitt.csv')
data = read_csv(input_file_path)      
df = read_as_pd(input_file_path)


# In[494]:

#df.describe()


# In[495]:

df = df.drop(['Unnamed: 0','Watch','Comments','More',
              'Priority Date','Most Recent LUD','Days Elapsed',
              'Notes','State','Last Updated','Username','Applicant Type',
              'Application Filed','USCIS Notice Date','USCIS Receipt Number',
              'RFE Received Date','Reason for RFE','RFE Replied Date','Case Added to Tracker'],1)


# In[509]:

df.head()


# In[609]:

#df["Nationality"].dropna()


# In[624]:

df = df[df["Nationality"] != "Unknown"]
df = df[df["Nationality"] != "nan"]


# In[625]:

len(df["Nationality"].unique())


# In[690]:

for nation in df["Nationality"].unique():
        


# In[639]:

data_array = df.reset_index().values
len(df)


# In[659]:

total_applicant = 0
pop = {}
for nation in df["Nationality"].unique():
    each_nation = data_array [0::,1] == nation
    total_applicant += len(data_array[each_nation,1])
    pop.update({nation : float(len(data_array[each_nation,1]))})

for key, value in pop.items(): 
    pop[key] = (value / total_applicant ) * 100.
#pop


# In[660]:

import operator
sorted_pop = sorted(pop.items(), key=operator.itemgetter(1))
selected_nationality = dict(sorted_pop[-10:])
print "Population for different nationality :"
print "#######################################"
selected_nationality


# In[689]:

for nation in selected_nationality:
    EB2_for_each_nation = np.logical_and(data_array[0::,1] == nation , data_array[0::,3] == "EB2")
    EB2_NIW_for_each_nation = np.logical_and(data_array[0::,1] == nation , data_array[0::,3] == "EB2-NIW")
    print nation, len(data_array[EB2_for_each_nation]), len(data_array[EB2_NIW_for_each_nation])
    
    
#print EB2_for_each_nation


# In[ ]:




# In[ ]:



