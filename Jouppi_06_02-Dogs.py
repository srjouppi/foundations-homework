#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd
import numpy as np


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[61]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", nrows=30000, na_values=["Unknown", "unknown", "UNKNOWN", "NO NAME"])
df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[6]:


df.shape


# In[7]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[ ]:


# Each row is an dog. 
# "Vaccinated" tells whether or not the dog is up-to-date on its vaccinations. 
# "Animal Dominant Color" tells the predominant color of the dog.


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# In[8]:


# What is the gender breakdown of NYC dogs?
# Who is the oldest dog in thisdata set?
# What are the most common breeds in this dataset?
# What is the average gap in time between application and license issue? What are the outliers?


# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[21]:


df['Primary Breed'].value_counts().sort_values(ascending=False).head(10)


# In[22]:


df[df['Primary Breed'] == 'Unknown']


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[25]:


df['Guard or Trained'].value_counts(normalize=True) * 100


# ## What are the actual numbers?

# In[26]:


df['Guard or Trained'].value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[27]:


df['Guard or Trained'].value_counts(dropna = False)


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[32]:


df['Guard or Trained'] = df['Guard or Trained'].replace(np.nan, "No")
df['Guard or Trained'].value_counts()


# ## What are the top dog breeds for guard dogs? 

# In[34]:


df[df['Guard or Trained'] == "Yes"]['Primary Breed'].value_counts().sort_values(ascending=False)


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[36]:


df['Year'] = df['Animal Birth'].apply(lambda birth: birth.year)
df.head(5)


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[38]:


df['Age'] = 2021 - df.Year
df.head(5)


# # Joining data together

# In[ ]:





# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[40]:


hoods = pd.read_csv("zipcodes-neighborhoods.csv")
hoods.head(5)


# In[57]:


merged = df.merge(hoods, left_on='Owner Zip Code', right_on='zip')
merged.head()


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[58]:


#BRONX
merged[merged['borough'] == 'Bronx']['Animal Name'].value_counts().sort_values(ascending=False).head(10)


# In[59]:


#BROOKLYN
merged[merged['borough'] == 'Brooklyn']['Animal Name'].value_counts().sort_values(ascending=False).head(10)


# In[60]:


#BROOKLYN
merged[merged['neighborhood'] == 'Upper East Side']['Animal Name'].value_counts().sort_values(ascending=False).head(10)


# In[ ]:


value_counts()


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[66]:


merged.groupby(by = 'neighborhood')['Primary Breed'].value_counts(normalize=True) * 100


# In[ ]:





# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[68]:


df.groupby(by = "Animal Gender")['Spayed or Neut'].value_counts(normalize=True) * 100


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[ ]:





# ## How many dogs are in each borough? Plot it in a graph.

# In[ ]:





# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[ ]:





# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[ ]:





# ## What percentage of dogs are not guard dogs?

# In[ ]:




