#!/usr/bin/env python
# coding: utf-8

# ### Do your imports!

# In[3]:


import pandas as pd
import numpy as np
pd.set_option("display.max_columns", None)


# # 311 data analysis
# 
# ## Read in `subset.csv` and review the first few rows
# 
# Even though it's a giant file – gigs and gigs! – it's a subset of the [entire dataset](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9). It covers plenty of years, but not all of the columns.
# 
# If your computer is struggling (which it will!) or you are impatient, feel free to use `nrows=` when reading it in to speed up the process by only reading in a subset of columns. Pull in at least a few million, or a couple years back.

# In[4]:


df = pd.read_csv('subset.csv')


# ### Where the subset came from
# 
# If you're curious, I took the [original data](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9/data) and clipped out a subset by using the command-line tool [csvkit](https://csvkit.readthedocs.io/en/latest/).
# 
# First I inspected the column headers:
# 
# ```bash
# $ csvcut -n 311_Service_Requests_from_2010_to_Present.csv 
# ```
# 
# Then I selected the columns I was interested in and saved it to a file.
# 
# ```bash
# $ csvcut -c 1,2,3,4,5,6,7,8,9,10,16,17,20,26,29 311_Service_Requests_from_2010_to_Present.csv > subset.csv
# ```
# 
# This was much much much much faster than doing it in Python.

# ## We want more columns!
# 
# **Right now we don't see all of the columns.** For example, mine has `...` between the **Incident Address** column and the **City** column. Go up to the top where you imported pandas, and add a `pd.set_option` line that will allow you to view all of the columns of the dataset.

# In[4]:


df.head()


# ## We hate those column names!
# 
# Change the column names to be tab- and period-friendly, like `df.created_date` instead of `df['Created Date']`

# In[5]:


df.columns = df.columns.str.lower().str.replace(" ", "_")
df.head()

# Much better :)


# # Dates and times
# 
# ## Are the datetimes actually datetimes?
# 
# We're going to be doing some datetime-y things, so let's see if the columns that look like dates are actually dates.

# In[12]:


df.dtypes


# ## In they aren't datetimes, convert them
# 
# The ones we're interested in are as follows:
# 
# * Created Date
# * Closed Date
# 
# You have two options to convert them:
# 
# 1. Do it like we did in class, but **overwrite the existing string columns with the new datetime versions**
# 2. Find an option with `read_csv` to automatically read certain columns as dates! Use the shift+tab trick to read the `read_csv` docs to uncover it. Once you find it, you'll set it to be the **list of date-y columns**.
# 
# They're both going to take forever if you do them wrong, but can be faster with a few tricks. For example, using `pd.to_datetime` can be sped up significantly be specifying the format of the datestring.
# 
# For example, if your datetime was formatted as `YYYY-MM-DD HH:MM:SS AM`, you could use the following:
# 
# ```
# df.my_datetime = pd.to_datetime(df.my_datetime, format="%Y-%m-%d %I:%M:%S %p")
# ```
# 
# It's unfortunately much much much faster than the `read_csv` technique. And yes, [that's `%I` and not `%H`](https://strftime.org/).
# 
# > *Tip: What should happen if it encounters an error or missing data?*

# In[6]:


df.closed_date = pd.to_datetime(df.closed_date, format="%m/%d/%Y %I:%M:%S %p", errors='coerce')
df.created_date = pd.to_datetime(df.created_date, format="%m/%d/%Y %I:%M:%S %p", errors='coerce')
df


# In[74]:





# ## According to the dataset, which month of the year has the most 311 calls?
# 
# The kind of answer we're looking for is "January," not "January 2021"

# In[ ]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[14]:


# I chose dt.month because it would pull out just the numberic value for the month
# (and not the year which would complicate things)
# Then I did a value count to see number of repetition of the month values.
# Most calls were June.
df.created_date.dt.month.value_counts().sort_values(ascending=False)


# ## Plot the 311 call frequency over our dataset on a _weekly_ basis
# 
# To make your y axis start at zero, use `ylim=(0,100000)` when doing `.plot`. But replace the `1000` with a large enough value to actually see your data nicely!

# In[15]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[16]:


# Used resample and size which adds up for me the number of records that occur during a week
# Leaving the ylim max at 100000 because it looks good to me
df.resample("W", on="created_date").size().plot(ylim=[0,100000])


# ## What time of day (by hour) is the least common for 311 complains? The most common?
# 

# In[17]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[ ]:





# In[18]:


# Pulled out the hour ALONE by using dt. 
# I think resample would give me date hour by day and that's too much data.
# Did a value counts to get number of repetitions of the hour value
# Most were created at midnight, which could be because 00:00:00 might be being used as a NA value
# Least common time of day was 4 a.m.
df.created_date.dt.hour.value_counts()


# ### Make a graph of the results
# 
# * Make sure the hours are in the correct order
# * Be sure to set the y-axis to start at 0
# * Give your plot a descriptive title

# In[19]:


df.created_date.dt.hour.value_counts().sort_index().plot(ylim=[0, 5000000],title ="311 calls by hour of the day")


# # Agencies
# 
# ## What agencies field the most complaints in the dataset? Get the top 5.
# 
# Use the `agency` column for this one.

# In[20]:


# Get the agency column
# Do a value_counts()
df.agency.value_counts().head()


# ## What are each of those agencies?
# 
# Define the following five acronyms:
# 
# * NYPD
# * HPD
# * DOT
# * DSNY
# * DEP

# In[21]:


# NYPD: New York Police Department
# HPD: Department of Housing Preservation and Development
# DOT: Department of Transportation
# DSNY: Department of Sanitation
# DEP: Department of Environmental Protection


# ## What is the most common complaint to HPD?

# In[22]:


# Why did you pick these columns to calculate the answer?


# In[23]:


# Complaint type will give me a generic complaint. 
# The descriptor will give me more detail. They might also vary more.
# I'm interested in the broader category for now.
# Filtering the data to only include Agency == HPD
# Doing a value count on the complaint type
# Most complaints deal with heating and hot water.
df[df.agency == 'HPD'].complaint_type.value_counts()


# ## What are the top 3 complaints to each agency?
# 
# You'll want to use the weird confusing `.groupby(level=...` thing we learned when reviewing the homework.

# In[24]:


pd.reset_option("display.max_rows")
df.groupby('agency').complaint_type.value_counts().groupby(level=0).nlargest(3)


# ## What is the most common kind of residential noise complaint?
# 
# The NYPD seems to deal with a lot of noise complaints at homes. What is the most common subtype?

# In[25]:


# Why did you pick these columns to calculate the answer?


# In[26]:


# I looked at the complaint_type column to see which broader categories existed. 
# They didn't seem particularly specific, so I decided to look at the descriptor column to get more info
df[df.complaint_type.str.contains("noise", case=False, na=False)].complaint_type.value_counts()


# In[27]:


# I searched the descriptor column for the word noise 
# and found it interesting that specifically construction noise is a big issue.
# See Construction Before/After hours, Construction Equipment and Jack Hammering
df[df.descriptor.str.contains("noise", case=False,na=False)].descriptor.value_counts()


# ## What time of day do "Loud Music/Party" complaints come in? Make it a chart!

# In[28]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[29]:


#Find the Loud Music/Party descriptor
df[df.descriptor == "Loud Music/Party"].head()


# In[30]:


# Take filtered df
# Get the hour using dt, because I'm only interested in the hour value not the date
# Count repetition of the hour values
# Most complaints come in from 10pm - Midnight
df[df.descriptor == "Loud Music/Party"].created_date.dt.hour.value_counts().sort_values(ascending=False)


# In[31]:


df[df.descriptor == "Loud Music/Party"].created_date.dt.hour.value_counts().sort_index().plot()


# ## When do people party hard?
# 
# Make a monthly chart of Loud Music/Party complaints since the beginning of the dataset. Make it count them on a biweekly basis (every two weeks).

# In[32]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[33]:


df[df.descriptor == "Loud Music/Party"].resample("2W", on="created_date").size().plot()


# ## People and their bees
# 
# Sometimes people complain about bees! Why they'd do that, I have no idea. It's somewhere in "complaint_type" – can you find all of the bee-related complaints?

# In[34]:


# Search the complaint type column for mentions of 'bee'
# do a value count to see which categories exist
df[df.complaint_type.str.contains("bee", case=False, na=False)].complaint_type.value_counts()


# ### What month do most of the complaints happen in? I'd like to see a graph.

# In[45]:


# Filter complaint type column to Harboring Bees/Wasps
# Pull out the month with dt on created date
# Do a value count to get the number of recurrences of the month value
# August has the highest number of bee related complaints

df[df.complaint_type == "Harboring Bees/Wasps"].created_date.dt.month.value_counts()


# In[46]:


# Sort the index
# Plot
df[df.complaint_type == "Harboring Bees/Wasps"].created_date.dt.month.value_counts().sort_index().plot()


# ### Are the people getting in trouble usually beekeepers or not beekeepers?

# In[41]:


# saving this filtered df to it's own variable so I can keep things straight
# searching the descriptor column for "not a" **Please note the misspelling of beekeeper in the dataset**
# doing a value_counts on the descriptor column to make sure there's no other spelling of beekeeper/beekeper
# or other descriptor with "not a" in it.
bees = df[df.complaint_type == "Harboring Bees/Wasps"]
bees[bees.descriptor.str.contains("not a", case=False, na=False)].descriptor.value_counts()


# In[49]:


# Now that I know what category I'm looking for I will do a value counts on the descriptor column
# To get a percentage of the total

bees.descriptor.value_counts(normalize=True, ascending=False) * 100

# ~80% of the time, non-beekeepers are getting into trouble


# # Math with datetimes
# 
# ## How long does it normally take to resolve a 311 complaint?
# 
# Even if we didn't cover this in class, I have faith that you can guess how to calculate it.

# In[47]:


# Subtract the date it was closed from the date it was created
df.closed_date - df.created_date


# Save it as a new column called `time_to_fix`

# In[51]:


df['time_to_fix'] = df.closed_date - df.created_date
df


# ## Which agency has the best time-to-fix time?

# In[53]:


# Group by agency
# Get the mean time_to_fix
df.groupby(by='agency').time_to_fix.mean().sort_values(ascending=False)


# In[54]:


# Mean can be deceptive because of outliers.
# Let's look at median
df.groupby(by='agency').time_to_fix.median().sort_values(ascending=False)

# OK WEEELLL This could mean a lot of things 
# IT most likely doesn't mean that these agencies respond to problems quickly
# HRA and 311 close cases in less than one minute
# Followed by EDC and NYPD which close cases in roughly an hour
# But we also have no idea how this has changed over time since the data spans from 2010 to present.


# ## Maybe we need some more information...
# 
# I might want to know how big our sample size is for each of those, maybe the high performers only have one or two instances of having requests filed!
# 
# ### First, try using `.describe()` on the time to fix column after your `groupby`.

# In[55]:


df.groupby(by='agency').time_to_fix.describe()


# ### Now, an alternative
# 
# Seems a little busy, yeah? **You can also do smaller, custom aggregations.**
# 
# Try something like this:
# 
# ```python
# # Multiple aggregations of one column
# df.groupby('agency').time_to_fix.agg(['median', 'size'])
# 
# # You can also do something like this to reach multiple columns
# df.groupby('agency').agg({
#     'time_to_fix': ['median', 'size']
# })
# 

# In[56]:


df.groupby('agency').time_to_fix.agg(['median', 'size'])


# In[57]:


df.groupby('agency').agg({
    'time_to_fix': ['median', 'size']
})


# ## Seems weird that NYPD time-to-close is so fast. Can we break that down by complaint type?
# 
# Remember the order: 
# 
# 1. Filter
# 2. Group
# 3. Grab a column
# 4. Do something with it
# 5. Sort

# In[60]:


# Get NYPD filtered Agency column
# Do a group by complaint type
# Get the median time-to-close for each complaint type
# Sort descending
# Looks like responding to a dead/dying tree and a 
# Street condition complaint that they responded to 146 years before it happened
# Might be throwing the mean off
df[df.agency == 'NYPD'].groupby(by='complaint_type').time_to_fix.median().sort_values(ascending=False)


# In[61]:


# Let's try that fancy describe thing
df[df.agency == 'NYPD'].groupby(by='complaint_type').time_to_fix.agg(['median', 'size'])


# ## Back to median fix time for all agencies: do these values change based on the borough?
# 
# First, use `groupby` to get the median time to fix per agency in each borough. You can use something like `pd.set_option("display.max_rows", 200)` if you can't see all of the results by default!

# In[ ]:


#I honestly don't know how to do it this way.


# ### Or, use another technique!

# We talked about pivot table for a hot second in class, but it's (potentially) a good fit for this situation:
# 
# ```python
# df.pivot_table(
#     columns='what will show up as your columns',
#     index='what will show up as your rows',
#     values='the column that will show up in each cell',
#     aggfunc='the calculation(s) you want dont'
# )
# ```

# In[65]:


df.pivot_table(
    columns = 'borough',
    index = 'agency',
    values = 'time_to_fix',
    aggfunc = np.median)


# ### Use the pivot table result to find the worst-performing agency in the Bronx, then compare with Staten Island
# 
# Since it's a dataframe, you can use the power of `.sort_values` (twice!). Do any of the agencies have a large difference between the two?

# In[67]:


# SORT BY BRONX DESCENDING
# Worst performing agency is TLC
df.pivot_table(
    columns = 'borough',
    index = 'agency',
    values = 'time_to_fix',
    aggfunc = np.median).sort_values(by='BRONX', ascending=False)


# In[68]:


# SORT BY STATEN ISLAND DESCENDING
# Worst performing agency is TLC
df.pivot_table(
    columns = 'borough',
    index = 'agency',
    values = 'time_to_fix',
    aggfunc = np.median).sort_values(by='STATEN ISLAND', ascending=False)


# ## What were the top ten 311 types of complaints on Thanksgiving 2020? Are they different than the day before Thanksgiving?
# 
# **Finding exact dates is awful, honestly.** While you can do something like this to ask for rows after a specific date:
# 
# ```python
# df[df.date_column >= '2020-01-01']
# ```
# 
# You, for some reason, can't ask for an **exact match** unless you're really looking for exactly at midnight. For example, this won't give you what you want:
# 
# ```python
# df[df.date_column == '2020-01-01']
# ```
# 
# Instead, the thing you need to do is this:
# 
# ```python
# df[(df.date_column >= '2020-01-01') & (df.date_column < '2020-01-02']
# ```
# 
# Everything that starts at midnight on the 1st but *is still less than midnight on the 2nd**.

# In[72]:


# Filter down to the day
# Do a Complaint Type value count
df[(df.created_date >= '2020-11-26') & (df.created_date < '2020-11-27')].complaint_type.value_counts().sort_values(ascending=False).head(10)


# ## What is the most common 311 complaint types on Christmas day?
# 
# And I mean *all Christmas days*, not just in certain years)
# 
# * Tip: `dt.` and `&` are going to be your friend here
# * Tip: If you want to get fancy you can look up `strftime`
# * Tip: One of those is much much faster than the other

# In[10]:


# I did the first three years and then stopped...
df[(df.created_date >= '2020-12-25') & (df.created_date < '2020-12-26') | (df.created_date >= '2019-12-25') & (df.created_date < '2019-12-26') | (df.created_date >= '2018-12-25') & (df.created_date < '2018-12-26')].complaint_type.value_counts(normalize=True)


# In[ ]:





# # Stories
# 
# Let's approach this from the idea of **having stories and wanting to investigate them.** Fun facts:
# 
# * Not all of these are reasonably answered with what our data is
# * We only have certain skills about how to analyzing the data
# * There are about six hundred approaches for each question
# 
# But: **for most of these prompts there are at least a few ways you can get something interesting out of the dataset.**

# ## Fireworks and BLM
# 
# You're writing a story about the anecdotal idea that the summer of the BLM protests there were an incredible number of fireworks being set off. Does the data support this?
# 
# What assumptions is your analysis making? What could make your analysis fall apart?

# In[81]:


#find the complaint types about fireworks
df[df.complaint_type.str.contains("firework", case=False, na=False)].complaint_type.value_counts()


# In[85]:


# Plot the monthly count of Illegal Fireworks complaint over time
fireworks = df[df.complaint_type == 'Illegal Fireworks']
fireworks.resample("M", on="created_date").size().plot()


# In[86]:


# Plotting the size to get a closer look at those numbers
fireworks.resample("M", on="created_date").size()
# At this point I would copy this data and manually add, because I don't know the simplest way to add the specific months I'm interested in
# Summer = June, July and August
# Summer 2018 = 212 complaints
# Summer 2019 = 811 complaints
# Summer 2020 = 48,187 complaints

# Ideally I'd like to get the average complaints per summer per year prior to 2020


# In[ ]:


# My analysis assumes that there is not someone maliciously hacking these numbers ie one person creating
# an insanely huge number of complaints. 
# My analysis assumes that there are no duplicates, triplicates, etc....
# My analysis assumes that firework complaints were not being filed in any other category than the Illegal Fireworks category


# ## Sanitation and work slowdowns
# 
# The Dept of Sanitation recently had a work slowdown to protest the vaccine mandate. You'd like to write about past work slowdowns that have caused garbage to pile up in the street, streets to not be swept, etc, and compare them to the current slowdown. You've also heard rumors that it was worse in Staten Island and a few Brooklyn neighborhoods - Marine Park and Canarsie - than everywhere else.
# 
# Use the data to find timeframes worth researching, and note how this slowdown might compare. Also, is there anything behind the geographic issue?
# 
# What assumptions is your analysis making? What could make your analysis fall apart?

# In[15]:


#Looking at common complaint types to DSNY
# Let's just look at missed collection data over time
df[df.agency == "DSNY"].complaint_type.value_counts()


# In[16]:


# Looks like we should look at a period in early 2021
df[df.complaint_type == "Missed Collection (All Materials)"].resample("M", on ="created_date").size().plot()


# In[17]:


df[df.complaint_type == "Dirty Conditions"].resample("M", on ="created_date").size().plot()


# In[18]:


#Looks like a mid 2021 date range would be worth inspecting Re: Street Sweeping
df[df.complaint_type.str.contains("sweeping", case=False, na=False)].resample("M", on ="created_date").size().plot()


# In[ ]:


# It would be worth inspecting previous spikes in complaints
# were they also due to labor shortages or strikes?
# My analysis would require me to go deeper into the descriptor column and to clean up the data more
# I would need to join this data-set with neighborhood-level dataset based on address
# There appear to be some stark drops which makes me wonder whether there were app outages during that period.


# ## Gentrification and whining to the government
# 
# It's said that when a neighborhood gentrifies, the people who move in are quick to report things to authorities that would previously have been ignored or dealt with on a personal basis. Use the data to investigate the concept (two techniques for finding gentrifying area are using census data and using Google).
# 
# What assumptions is your analysis making? What could make your analysis fall apart? Be sure to cite your sources. 

# In[ ]:





# ## 311 quirks
# 
# Our editor tried to submit a 311 request using the app the other day, but it didn't go through. As we all know, news is what happens to your editor! Has the 311 mobile app ever actually stopped working?
# 
# If that's a dead end, maybe you can talk about the differences between the different submission avenues: could a mobile outage disproportionately impact a certain kind of complaint or agency? How about if the phone lines stopped working?
# 
# What assumptions is your analysis making? What could make your analysis fall apart?

# In[ ]:





# ## NYCHA and public funds
# 
# NYC's public housing infrastructure is failing, and one reason is lack of federal funds. While the recent spending bills passed through Congress might be able to help, the feeling is that things have really fallen apart in the past however-many years – as time goes on it gets more and more difficult for the agency in control of things to address issues in a timely manner.
# 
# If you were tasked with finding information to help a reporter writing on this topic, you will **not** reasonably be able to find much in the dataset to support or refute this. Why not? 
# 
# If you wanted to squeeze something out of this dataset anyway, what could an option be? (You might need to bring in another dataset.)

# In[90]:


# No complaint type specifically about NYCHA
df[df.complaint_type.str.contains("NYCHA", case=False, na=False)]


# In[91]:


# No descriptor type specifically about NYCHA
df[df.descriptor.str.contains("NYCHA", case=False, na=False)]


# In[100]:


df[df.agency == 'HPD'].location_type.value_counts()


# In[96]:


# One could look at HPD complaints at addresses that match NYCHA addresses (joining those two data sets)
# This would give a sense of how many complaints are coming in over time (would need to filter the data set to NYCHA locations)
df[df.agency == 'HPD'].resample("Y", on='created_date').size().sort_index().plot()


# In[101]:


# Median Time_to_Fix by year. Seems to be improving? 
# Although it looks like these times were manually entered before 2016
df[df.agency == 'HPD'].resample("Y", on='created_date').time_to_fix.median()

