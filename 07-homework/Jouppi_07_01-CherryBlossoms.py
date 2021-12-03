#!/usr/bin/env python
# coding: utf-8

# # Cherry Blossoms!
# 
# If we travel back in time, [cherry blossoms](https://en.wikipedia.org/wiki/Cherry_blossom) were once in full bloom! We don't live in Japan or DC, but in non-COVID times we also have the [Brooklyn Botanic Garden's annual festival](https://www.bbg.org/visit/event/sakura_matsuri_2020).
# 
# We'll have to make up for it with data-driven cherry blossoms instead. Once upon a time [Data is Plural](https://tinyletter.com/data-is-plural) linked to [a dataset](http://atmenv.envi.osakafu-u.ac.jp/aono/kyophenotemp4/) about when the cherry trees blossom each year. It's completely out of date, but it's quirky in a real nice way so we're sticking with it.
# 
# ## 0. Do all of your importing/setup stuff

# In[13]:


get_ipython().system('pip install xlrd')


# In[1]:


import pandas as pd
import numpy as np
pd.set_option("display.max_columns", None)
df = pd.read_excel("KyotoFullFlower7.xls", header=25, na_values=["-"])
df

#Added header to tell pandas which row to find the column names in.


# ## 1. Read in the file using pandas, and look at the first five rows

# In[22]:


df.head(5)


# ## 2. Read in the file using pandas CORRECTLY, and look at the first five rows
# 
# Hrm, how do your column names look? Read the file in again but this time add a parameter to make sure your columns look right.
# 
# **TIP: The first year should be 801 AD, and it should not have any dates or anything.**

# In[23]:


df.head()


# ## 3. Look at the final five rows of the data

# In[25]:


df.tail()


# ## 4. Add some more NaN values

# It looks like you should probably have some NaN/missing values earlier on in the dataset under "Reference name." Read in the file *one more time*, this time making sure all of those missing reference names actually show up as `NaN` instead of `-`.

# In[28]:


# Added na_values = ["-"] to tell pandas to read the - as NaN.
df.head()


# In[2]:


# I am also going to clean up the headers to make this easier
df.columns = df.columns.str.lower().str.replace(" ", "_")
df.columns = df.columns.str.lower().str.replace("-", "_")
df.columns = df.columns.str.lower().str.replace("(","")
df.columns = df.columns.str.lower().str.replace(")","")
df.head()


# In[ ]:





# ## 4. What source is the most common as a reference?

# In[5]:


# Looking for the source code that has the highest count. 
# Used normalize to get the percentage of the total.
# 3.0 is the most common source
df.source_code.value_counts(normalize=True) * 100


# ## 6. Filter the list to only include columns where the `Full-flowering date (DOY)` is not missing
# 
# If you'd like to do it in two steps (which might be easier to think through), first figure out how to test whether a column is empty/missing/null/NaN, get the list of `True`/`False` values, and then later feed it to your `df`.

# In[4]:


# I really wasn't sure whether you wanted us to create a temporary table 
# or take these out all together from the dataset
# using dropna to drop the records that have NaN in the full_flowering_date_doy column
# testing it by saving it to a test variable and doing a value count on 'isna'
# there are no "True"s, so I think it worked.
natest = df.dropna(subset=['full_flowering_date_doy'])
natest.full_flowering_date_doy.isna().value_counts()


# In[19]:


# Saving it to my dataframe
df = df.dropna(subset=['full_flowering_date_doy'])


# ## 7. Make a histogram of the full-flowering date

# In[20]:


# Taking the flowering date - DOY and making a histogram
df.full_flowering_date_doy.hist()


# ## 8. Make another histogram of the full-flowering date, but with 39 bins instead of 10

# In[23]:


df.full_flowering_date_doy.hist(bins=39)


# ## 9. What's the average number of days it takes for the flowers to blossom? And how many records do we have?
# 
# Answer these both with one line of code.

# In[13]:


df.full_flowering_date_doy.describe()


# ## 10. What's the average days into the year cherry flowers normally blossomed before 1900?
# 
# 

# In[36]:


# Filter the data down to ad < 1900
# Take the mean of the date_doy column
# Before 1900, cherry flowers were blooming 105 days into the year on average
df[df.ad < 1900].full_flowering_date_doy.mean()


# ## 11. How about after 1900?

# In[66]:


# Filter the data down to date_doy > 1900
# Take the mean of the date_doy column
# After 1900, cherry flowers were blooming 100 days into the year on average
df[df.ad > 1900].full_flowering_date_doy.mean()


# ## 12. How many times was our data from a title in Japanese poetry?
# 
# You'll need to read the documentation inside of the Excel file.

# In[67]:


# 4: title in Japanese poetry
# Do a value counts on data type code to find number of records with "4" in that column
# going back to df for this one, in case filtering out NaNs missed some records
df.data_type_code.value_counts()


# In[84]:


# Or I could have done this if I wanted a very narrow picture
df[df.data_type_code == 4].shape


# ## 13. Show only the years where our data was from a title in Japanese poetry

# In[69]:


df[df.data_type_code == 4]


# ## 14. Graph the full-flowering date (DOY) over time

# In[70]:


# going back to ffd to graf the full flowering doy over time
# Going to pull out the full flowering DOY
# plot it and define x = ad and y = FFDOY

df.full_flowering_date_doy.plot(x='ad',y='full_flowering_date_doy')


# ## 15. Smooth out the graph
# 
# It's so jagged! You can use `df.rolling` to calculate a rolling average.
# 
# The following code calculates a **10-year mean**, using the `AD` column as the anchor. If there aren't 20 samples to work with in a row, it'll accept down to 5. Neat, right?
# 
# (We're only looking at the final 5)

# In[75]:


#changing this to my filtered dataframe
df.rolling(10, on='ad', min_periods=5)['full_flowering_date_doy'].mean().tail()


# In[38]:


df['rolling_date'] = df.rolling(20, on='ad', min_periods=5)['full_flowering_date_doy'].mean().tail()
df.rolling_date.plot(x='ad', y='full_flowering_date_doy', ylim=(80,120))


# Use the code above to create a new column called `rolling_date` in our dataset. It should be the 20-year rolling average of the flowering date. Then plot it, with the year on the x axis and the day of the year on the y axis.
# 
# Try adding `ylim=(80, 120)` to your `.plot` command to make things look a little less dire.

# ### 16. Add a month column
# 
# Right now the "Full-flowering date" column is pretty rough. It uses numbers like '402' to mean "April 2nd" and "416" to mean "April 16th." Let's make a column to explain what month it happened in.
# 
# * Every row that happened in April should have 'April' in the `month` column.
# * Every row that happened in March should have 'March' as the `month` column.
# * Every row that happened in May should have 'May' as the `month` column.
# 
# There are **at least two ways to do this.**
# 
# #### WAY ONE: The bad-yet-simple way
# 
# If you don't want to use `pd.to_datetime`, you can use this as an sample for updating March. It finds everything with a date less than 400 and assigns `March` to the `month` column:
# 
# ```python
# df.loc[df['Full-flowering date'] < 400, 'month'] = 'March'
# ```
# 
# #### WAY TWO: The good-yet-complicated way
# 
# * When you use `pd.to_datetime`, if pandas doesn't figure it out automatically you can also pass a `format=` argument that explains what the format is of the datetime. You use [the codes here](https://strftime.org/) to mark out where the days, months, etc are. For example, `2020-04-09` would be converted using `pd.to_datetime(df.colname, "format='%Y-%m-%d")`.
# * `errors='coerce'` will return `NaN` for missing values. By default it just yells "I don't know what to do!!!"
# * And remember how we used `df.date_column.dt.month` to get the number of the month? For the name, you use `dt.strftime` (string-formatted-time), and pass it [the same codes](https://strftime.org/) to tell it what to do. For example, `df.date_column.dt.strftime("%Y-%m-%d")` would give you `"2020-04-09"`.

# In[5]:


# create a new column entitled date_time
# day of month as a zero padded decimal %d
# month as a decimal number %m
df.full_flowering_date = pd.to_datetime(df.full_flowering_date, format = "%m%d")


# In[6]:


df.full_flowering_date


# In[18]:


# Struggled to figure out what you were saying earlier so I did it in a couple of steps.
# Pulled the month out of the ffd column and saved it to a new column
# Took the the month and gave it a name using this code I found on stack overflow. :/
df['month'] = df.full_flowering_date.dt.month
df['month'] = pd.to_datetime(df.month, format='%m').dt.month_name()
df


# In[ ]:





# ### 17. Using your new column, how many blossomings happened in each month?

# In[19]:


# do a value count on month column
df.month.value_counts()


# ### 18. Graph how many blossomings happened in each month.

# In[20]:


#Meh?
df.month.value_counts().plot(kind='bar')


# In[21]:


#Not great for this categorical data
#Sort index doesn't work because these are strings
df.month.value_counts().sort_index().plot()


# In[83]:


#ugh
df.month.value_counts().plot(kind='pie')


# ### 19. Adding a day-of-month column
# 
# Now we're going to add a new column called `day_of_month.` It might be a little tougher than it should be since the `Full-flowering date` column is a *float* instead of an integer.
# 
# *Tip: If your method involves `.astype(int)` it isn't going to work since it's missing data, you can add `.dropna().astype(int)` instead.*

# In[85]:


#my column doesn't appear to have missing data?
df.full_flowering_date.isna().value_counts()


# In[90]:


df['day_of_month']=df.full_flowering_date.dt.day
df.day_of_month.dtypes


# In[ ]:





# ### 20. Adding a date column
# 
# If you don't have one yet, take the `'month'` and `'day_of_month'` columns and combine them in order to create a new column called `'date'`. You could alternatively use `.dt.strftime` as mentioned above.

# In[94]:


df['date'] = df.full_flowering_date.dt.strftime("%m-%d")
df


# In[ ]:





# # YOU ARE DONE.
# 
# And **incredible.**

# In[ ]:




