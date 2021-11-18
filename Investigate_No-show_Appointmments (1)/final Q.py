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

# In[6]:


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

# In[7]:


get_ipython().system('dir')


# In[8]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df = pd.read_csv("noshowappointments-kagglev2-may-2016.csv")
df.head()


# In[9]:


df.shape


# In[10]:


df.info()


# The dataset includes 14 columns and 110527 data rows

# In[11]:


df.describe()


# In the above description table we see that we have an age of -1.  JJust speculating this can be an appointmment for an unnborn fetus but because there is nnot data explainingthis anommyuly, we will delete the entry when we clean our data.  It also looks like no one under the age of 55 opted sms reminders.

# In[12]:


df.hist(figsize=(14,8))


# Looking at the histograms above we can more clearly see that this data set contains categorical and quantitative data.
# Categorical Data: Gender, Diabetes, Alcoholism, Handcap, SMS_received, No-show
# Quantitative Data: PatientId, AppointmentID, Age, ScheduledDay, AppointmentDay

# ### Data Cleaning (Replace this with more specific notes!)

# In[13]:


# After discussing the structure of the data and any problems that need to be
#   cleaned, perform those cleaning steps in the second part of this section.
df.isnull().sum()


# In[14]:


# Check for duplicate rows 
df.duplicated().sum()


# In[15]:


# Check for duplicate appointmentID
sum(df.AppointmentID.duplicated())


# In[16]:


sum(df.PatientId.duplicated())


# In the above cell there appears to be duplicated patient id's. we wil dive in further and look at the value counts

# In[17]:


df.PatientId.value_counts().head()


# With this we can see that the patient’s row does have repeated rows and that some patients booked multiple medical appointments.  The top five patients booking 369 appointments alone.  This is interesting information as we can possibly get feedback from the top patients coming back to see how to improve processes.  

# In[18]:


df.nunique()


# Here we can see 81 unique neighborhoods as well as 27 unique appointment days.

# In[19]:


df['AppointmentDay'].min(), df['AppointmentDay'].max()


# The first appointment day recorded in this dataset is 4/29/16 and the last day recorded is 6/8/16.  This shows that in 40 days there were 110,527 appointments.

# Next we will change the date and time to the proper format.

# In[20]:


columns = ['ScheduledDay', 'AppointmentDay']
for column in columns:
    df[column] = pd.to_datetime(pd.to_datetime(df[column]).dt.date)

print(df.dtypes)
df.head()


# Next let us find if there are anymore negative values in the data set.

# In[21]:


negative_age = df.query('Age < 0')
negative_age


# Ok it appears to be only one negative value.  This maybe human error so we will go ahead and delete it so it doesnt scue the data.

# In[22]:


df.drop(negative_age.index, inplace=True)
df.query('Age < 0')


# Here we can see we sucessfully dropped the negative value from the dataset

# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# ### What is the current show up rate?

# In[23]:


def PropByVar(df, variable):
    df_pie = df[variable].value_counts()
    ax = df_pie.plot.pie(autopct='%0.1f%%');
    ax.set_title(variable + ' (%) (Per appointment)');

PropByVar(df, 'No-show')


# In[24]:


base_color = sns.color_palette()[0]
sns.countplot(data = df, x = 'No-show', color = base_color)
plt.title('Paitents Show Status')
plt.xticks([0, 1], ['Show Up', 'No Show'])
plt.xlabel('Stauts')
plt.ylabel('Number of Patients');


# ### Does age or gender have a correlation with the amount of No-shows?

# In[25]:


# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings.
fig, ax = plt.subplots(figsize=(15,10))
df['Gender Numeric'] = df['Gender'].map({'F':1,'M':0})
df['No show Numeric'] = df['No-show'].map({'Yes':1,'No':0})
sns.heatmap(df.corr(), cmap='Paired' ,ax=ax, annot=True);


# Looking at the heatmap above we can see there is no real correlation between age or gender.  According to the heatmap there is no correlation between age and no-show appointments.  We will delve into these statistics to see if there still might be insight into our question.  On a secondary note, we can see a correlation between age and hypertension and between age and diabetes.  We can also see a correlation between hypertension and diabetes as well.  Although this data does not pertain to our question, it is still insightful.

# In[26]:


df.Gender.value_counts()


# We can see that there are more female patients than male.  Even though there is a huge difference between the genders in the data set, I wonder which gender has the most no-shows.  But first let us see how many no-shows we have.

# Its important to note that 'No' in this dataset means that they showed upto their appointment while 'Yes' means that they did not show up.

# In[27]:


df.groupby('No-show')['Gender'].value_counts()


# Delving into the gender statistics we can see that women have more no shows than males.  This is expected as there were almost twice as any female patients.  Sinnce there is such a huge difference between the genders let us see if both males and females have no shows inn the same proportions.

# Next let us investigate what age groups tend to miss the most appointments.  My hypothesis before delving into the data is that younger people tend to miss the most appointments due to maturity or poor time management skills.  Before going into more detail, I would like to see the average age of the people who make and miss their appointments.

# In[28]:


bin_edges = np.arange(0, df['Age'].max()+5, 5)
plt.hist(data = df, x = 'Age', bins = bin_edges)
plt.xlabel('Age')
plt.title('Distribution of Patients Age');


# As we can see based on this histogram, most of the patients tend to be on the younger.

# In[29]:


df.groupby('No-show').Age.mean()


# In[30]:


df.groupby('No-show').Age.mean().loc['Yes']


# We see that the average age of those who miss their appointments are younger than those who make there appointments. Now lets look at which ages have the most no-shows.

# In[31]:


df.groupby('No-show').Age.value_counts()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


# In[32]:


df.groupby('No-show').Age.value_counts()


# When first pulling the data, Python truncated the data but I decided to override this so I can see how many appointments each age missed.  Looking at the cell above we can see the top 14 ages that missed appointments were all under 33 which is lower than the mean age.  But the interesting part is that the top 3 ages that missed appointments were all under 18 with the top 2 being 0 and 1.  I am assuming the ages 0 and 1 are babies so the responsibility of showing up would be on the parents.  These new findings raise the question of how we can we possibly make it easier for parents to make their children's appointments.  Transportation can be an issue, taking time from work could also be a cause for these missed appointments

# Question 3: What neighbourhoods have the highest no show rate?

# In[64]:


# no show appointments
df["No-show"]= df["No-show"]=='Yes'

# plot a horizontal bar chart
plt.figure(figsize = [8, 4])
cat_order = df.Neighbourhood.value_counts().index[:5]
sns.countplot(data = pd.read_csv("noshowappointments-kagglev2-may-2016.csv"), y = 'Neighbourhood', color = base_color, order = cat_order)
plt.title('Highest 5 Neighbourhoods in Terms of The Number of No Show Appointments')
plt.xlabel('Number of No Show Appointments')
plt.ylabel('Neighbourhood');


# In[68]:


week_day = df.AppointmentDay.dt.weekday
weekday_counts = df.week_day.value_counts()
weekday_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

no_show_perc_weekday = df.groupby('week_day').no_show.mean() * 100

# plot a line plot
plt.figure(figsize = [8, 4])
sns.lineplot(x = no_show_perc_weekday.index,  y = no_show_perc_weekday, marker='o')
plt.title('The Percentages of No Show Appointments Based on The Day of The Week')
plt.xticks(np.arange(0, 6+1, 1), weekday_labels)
plt.xlabel('Appointment Day')
plt.ylabel('No Show Percentage');


# <a id='conclusions'></a>
# ## Conclusions
# In conclusion we found that the show up rate to appointments is 79.81%.  When looking into the data we saw that most of these No-shows came from women because there is a disproportionate number of women compared to men.  But even with this huge discrepancy we saw that men and women missed their appointments in almost the same proportion.  20% of women missed their appointments while 19% of men missed their appointments.  This led me to believe that if maybe gender did not play a role age did.  My assumption was that younger patients would miss their appointments due too poor time management and immaturity.  So, I decided to look at the average age of the people who showed up and compare it to those who missed their appointments.  Once I found the average age of both no shows and those who showed up, it supported the idea that younger patients tend to miss their appointments with the average of no shows being 34 and the average age of those who kept their appointments was 37.  On the surface this looks to be the answer, but I decided to delve deeper into the statistics and see what age missed the most appointments.  Upon further inspection we saw that the top 3 ages that missed appointments were under the age of 18 and the top 2 were ages 0 and 1.  It looks like children or minors tend to miss the most appointments.  Being a newborn parent, age 0 and 1, can be difficult maybe things like work, other children, and time led to these parents missing the appointment.  Due to the limitations of this dataset and the high-level inquiry into the data, we cannot draw concrete conclusions.  We did however find new insights into the data. 

# In[ ]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

