#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigating Medical Appointment No Shows in Brazil 
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# > In this project we will be analyzing data associated with medical appointment no shows in Brazil.  In particular, we will focus on finding trends amongst those who showed up to their appointments and see how they differ from those who did not show up to their appoinntmments.  This report is focused on the question of whether or not patients show up to their medical appointments or not. 

# Questions this dataset will answer:
#     What is the current show up rate?
#     Does age or gender have a correlation with the amount of No-shows?
#     Highest five neighbourhoods in terms of the number of no-show appointments?
#     Does day of the week affect no show rate?

# In[13]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > **Tip**: In this section of the report, we will load in the data, check for cleanliness, and then trim and clean our dataset for analysis. 
# ### General Properties

# In[15]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df = pd.read_csv("noshowappointments-kagglev2-may-2016.csv")
df.head()


# In[58]:


df.shape


# In[59]:


df.info()


# The dataset includes 14 columns and 110527 data rows

# In[60]:


df.describe()


# In the above description table we see that we have an age of -1.  JJust speculating this can be an appointmment for an unnborn fetus but because there is nnot data explainingthis anommyuly, we will delete the entry when we clean our data.  It also looks like no one under the age of 55 opted sms reminders.

# In[61]:


df.hist(figsize=(14,8))


# Looking at the histograms above we can more clearly see that this data set contains categorical and quantitative data.
# Categorical Data: Gender, Diabetes, Alcoholism, Handcap, SMS_received, No-show
# Quantitative Data: PatientId, AppointmentID, Age, ScheduledDay, AppointmentDay

# In[2]:


df.unique()


# ### Data Cleaning (Replace this with more specific notes!)

# In[62]:


# After discussing the structure of the data and any problems that need to be
#   cleaned, perform those cleaning steps in the second part of this section.
df.isnull().sum()


# In[63]:


# Check for duplicate rows 
df.duplicated().sum()


# In[64]:


# Check for duplicate appointmentID
sum(df.AppointmentID.duplicated())


# In[65]:


sum(df.PatientId.duplicated())


# In the above cell there appears to be duplicated patient id's. we wil dive in further and look at the value counts

# In[66]:


df.PatientId.value_counts().head()


# With this we can see that the patient’s row does have repeated rows and that some patients booked multiple medical appointments.  The top five patients booking 369 appointments alone.  This is interesting information as we can possibly get feedback from the top patients coming back to see how to improve processes.  

# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# ### What is the current show up rate?

# In[81]:


def PropByVar(df, variable):
    df_pie = df[variable].value_counts()
    ax = df_pie.plot.pie(autopct='%0.1f%%');
    ax.set_title(variable + ' (%) (Per appointment)');

PropByVar(df, 'No-show')


# ### Does age or gender have a correlation with the amount of No-shows?

# In[67]:


# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings.
fig, ax = plt.subplots(figsize=(15,10))
df['Gender Numeric'] = df['Gender'].map({'F':1,'M':0})
df['No show Numeric'] = df['No-show'].map({'Yes':1,'No':0})
sns.heatmap(df.corr(), cmap='Paired' ,ax=ax, annot=True);


# Looking at the heatmap above we can see there is no real correlation between age or gender.  According to the heatmap there is no correlation between age and no-show appointments.  We will delve into these statistics to see if there still might be insight into our question.  On a secondary note, we can see a correlation between age and hypertension and between age and diabetes.  We can also see a correlation between hypertension and diabetes as well.  Although this data does not pertain to our question, it is still insightful.

# In[68]:


df.Gender.value_counts()


# We can see that there are more female patients than male.  Even though there is a huge difference between the genders in the data set, I wonder which gender has the most no-shows.  But first let us see how many no-shows we have.

# Its important to note that 'No' in this dataset means that they showed upto their appointment while 'Yes' means that they did not show up.

# In[69]:


df.groupby('No-show')['Gender'].value_counts()


# Delving into the gender statistics we can see that women have more no shows than males.  This is expected as there were almost twice as any female patients.  Sinnce there is such a huge difference between the genders let us see if both males and females have no shows inn the same proportions.

# Next let us investigate what age groups tend to miss the most appointments.  My hypothesis before delving into the data is that younger people tend to miss the most appointments due to maturity or poor time management skills.  Before going into more detail, I would like to see the average age of the people who make and miss their appointments.

# In[72]:


df.groupby('No-show').Age.mean()


# In[73]:


df.groupby('No-show').Age.mean().loc['Yes']


# We see that the average age of those who miss their appointments are younger than those who make there appointments. Now lets look at which ages have the most no-shows.

# In[83]:


df.groupby('No-show').Age.value_counts()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


# In[74]:


df.groupby('No-show').Age.value_counts()


# When first pulling the data, Python truncated the data but I decided to override this so I can see how many appointments each age missed.  Looking at the cell above we can see the top 14 ages that missed appointments were all under 33 which is lower than the mean age.  But the interesting part is that the top 3 ages that missed appointments were all under 18 with the top 2 being 0 and 1.  I am assuming the ages 0 and 1 are babies so the responsibility of showing up would be on the parents.  These new findings raise the question of how we can we possibly make it easier for parents to make their children's appointments.  Transportation can be an issue, taking time from work could also be a cause for these missed appointments

# <a id='conclusions'></a>
# ## Conclusions
# In conclusion we found that the show up rate to appointments is 79.81%.  When looking into the data we saw that most of these No-shows came from women because there is a disproportionate number of women compared to men.  But even with this huge discrepancy we saw that men and women missed their appointments in almost the same proportion.  20% of women missed their appointments while 19% of men missed their appointments.  This led me to believe that if maybe gender did not play a role age did.  My assumption was that younger patients would miss their appointments due too poor time management and immaturity.  So, I decided to look at the average age of the people who showed up and compare it to those who missed their appointments.  Once I found the average age of both no shows and those who showed up, it supported the idea that younger patients tend to miss their appointments with the average of no shows being 34 and the average age of those who kept their appointments was 37.  On the surface this looks to be the answer, but I decided to delve deeper into the statistics and see what age missed the most appointments.  Upon further inspection we saw that the top 3 ages that missed appointments were under the age of 18 and the top 2 were ages 0 and 1.  It looks like children or minors tend to miss the most appointments.  Being a newborn parent, age 0 and 1, can be difficult maybe things like work, other children, and time led to these parents missing the appointment.  Due to the limitations of this dataset and the high-level inquiry into the data, we cannot draw concrete conclusions.  We did however find new insights into the data. 

# In[ ]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

