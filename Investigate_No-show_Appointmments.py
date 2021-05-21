#!/usr/bin/env python
# coding: utf-8

# > **Tip**: Welcome to the Investigate a Dataset project! You will find tips in quoted sections like this to help organize your approach to your investigation. Before submitting your project, it will be a good idea to go back through your report and remove these sections to make the presentation of your work as tidy as possible. First things first, you might want to double-click this Markdown cell and change the title so that it reflects your dataset and investigation.
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
# > **Tip**: In this project we will be analyzing data associated with medical appointment no shows in Brazil.  In particular, we will focus on finding trends amongst those who showed up to their appointments and see how they differ from those who did not show up to their appoinntmments.  This report is focused on the question of whether or not patients show up to their medical appointments or not. 

# In[2]:


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
# > **Tip**: In this section of the report, you will load in the data, check for cleanliness, and then trim and clean your dataset for analysis. Make sure that you document your steps carefully and justify your cleaning decisions.
# 
# ### General Properties

# In[3]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df = pd.read_csv('noshowappointments-kagglev2-may-2016.csv')
df.head()


# In[4]:


df.shape


# In[5]:


df.info()


# In[6]:


df.describe()


# In the above description table we see that we have an age of -1.  JJust speculating this can be an appointmment for an unnborn fetus but because there is nnot data explainingthis anommyuly, we will delete the entry when we clean our data.  It also looks like no one under the age of 55 opted sms reminders.

# In[7]:


df.hist(figsize=(14,8))


# Looking at the histograms above we can more clearly see that this data set contains categorical and quantitative data.
# Categorical Data: Gender, Diabetes, Alcoholism, Handcap, SMS_received, No-show
# Quantitative Data: PatientId, AppointmentID, Age, ScheduledDay, AppointmentDay

# > **Tip**: You should _not_ perform too many operations in each cell. Create cells freely to explore your data. One option that you can take with this project is to do a lot of explorations in an initial notebook. These don't have to be organized, but make sure you use enough comments to understand the purpose of each code cell. Then, after you're done with your analysis, create a duplicate notebook where you will trim the excess and organize your steps so that you have a flowing, cohesive report.
# 
# > **Tip**: Make sure that you keep your reader informed on the steps that you are taking in your investigation. Follow every code cell, or every set of related code cells, with a markdown cell to describe to the reader what was found in the preceding cell(s). Try to make it so that the reader can then understand what they will be seeing in the following cell(s).
# 
# ### Data Cleaning (Replace this with more specific notes!)

# In[8]:


# After discussing the structure of the data and any problems that need to be
#   cleaned, perform those cleaning steps in the second part of this section.
df.isnull().sum()


# In[9]:


# Check for duplicate rows 
df.duplicated().sum()


# In[10]:


# Check for duplicate appointmentID
sum(df.AppointmentID.duplicated())


# In[11]:


sum(df.PatientId.duplicated())


# In the above cell there appears to be duplicated patient id's. we wil dive in further and look at the value counts

# In[18]:


df.PatientId.value_counts().head()


# In[19]:


no_show = df.No-show == False
show = df.No-show == True


# With this we cann see that the patients row does have repeated rows and that some patients booked multiple mmedical appointments.  The top five patients booking 369 appointments alone.  This is interesting informmation as we can possibly get feedback from the top patients coming back to see how to improve processes.  

# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > **Tip**: Now that you've trimmed and cleaned your data, you're ready to move on to exploration. Compute statistics and create visualizations with the goal of addressing the research questions that you posed in the Introduction section. It is recommended that you be systematic with your approach. Look at one variable at a time, and then follow it up by looking at relationships between variables.
# 
# ### Research Question 1 (Replace this header name!)

# In[13]:


# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings.
fig, ax = plt.subplots(figsize=(15,10))
sns.heatmap(df.corr(), cmap='Paired' ,ax=ax, annot=True);


# Looking at the heatmap above we can see a correlation between age and hypertension and between age and diabetes.  We can also see a correlation between hypertension and diabetes as well.  This heatmap although informative doesnnt help us towards our question of no show medical appointments. 

# In[14]:


no_show = df.Show-up == False
show = df.Show-up == True


# In[ ]:





# ### Research Question 2  (Replace this header name!)

# In[ ]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.


# <a id='conclusions'></a>
# ## Conclusions
# 
# > **Tip**: Finally, summarize your findings and the results that have been performed. Make sure that you are clear with regards to the limitations of your exploration. If you haven't done any statistical tests, do not imply any statistical conclusions. And make sure you avoid implying causation from correlation!
# 
# > **Tip**: Once you are satisfied with your work here, check over your report to make sure that it is satisfies all the areas of the rubric (found on the project submission page at the end of the lesson). You should also probably remove all of the "Tips" like this one so that the presentation is as polished as possible.
# 
# ## Submitting your Project 
# 
# > Before you submit your project, you need to create a .html or .pdf version of this notebook in the workspace here. To do that, run the code cell below. If it worked correctly, you should get a return code of 0, and you should see the generated .html file in the workspace directory (click on the orange Jupyter icon in the upper left).
# 
# > Alternatively, you can download this report as .html via the **File** > **Download as** submenu, and then manually upload it into the workspace directory by clicking on the orange Jupyter icon in the upper left, then using the Upload button.
# 
# > Once you've done this, you can submit your project by clicking on the "Submit Project" button in the lower right here. This will create and submit a zip file with this .ipynb doc and the .html or .pdf version you created. Congratulations!

# In[ ]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

