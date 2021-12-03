#!/usr/bin/env python
# coding: utf-8

# ## Logging on
# 
# Use Selenium to visit https://webapps1.chicago.gov/buildingrecords/ and accept the agreement.
# 
# > Think about when you use `.find_element...` and when you use `.find_elementSSS...`

# In[1]:


import pandas as pd

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


driver = webdriver.Chrome(ChromeDriverManager().install())


# In[3]:


driver.get("https://webapps1.chicago.gov/buildingrecords/")


# In[4]:


# Accept the agreement
driver.find_element(By.ID, "rbnAgreement1").click()
# Click submit
driver.find_element(By.ID, "submit").click()


# In[ ]:





# In[ ]:





# ## Searching
# 
# Search for **400 E 41ST ST**.

# In[5]:


# Input Search
driver.find_element(By.ID, "fullAddress").send_keys("400 E 41ST ST")
# Click Submit
driver.find_element(By.ID, "submit").click()


# In[ ]:





# ## Saving tables with pandas
# 
# Use pandas to save a CSV of all **permits** to `Permits - 400 E 41ST ST.csv`. Note that there are **different sections of the page**, not just one long permits table.
# 
# > - *Tip: When using `.read_html`, try using `flavor='lxml'` and comparing the results to `flavor='html5lib'`. Which works better?*
# > - *Tip: You might need to install `html5lib` using `pip`. If so, you'll need to restart the notebook using **Kernel > Restart** before it will work.*

# In[6]:


table = driver.find_element(By.ID, "resultstable_permits")
table
df = pd.read_html(table.get_attribute('outerHTML'),flavor='html5lib')[0]
df


# In[7]:


df.to_csv("Permits - 400 E 41ST ST.csv", index=False)


# In[8]:


pd.read_csv("Permits - 400 E 41ST ST.csv")


# ## Saving tables the long way
# 
# Save a CSV of all DOB inspections to `Inspections - 400 E 41ST ST.csv`.
# 
# This is more complicated than the last one becuse **we also need to save the URL to the inspection** (see how the inspection number is a link?). As a result, you won't be able to use pandas! Instead, you'll need to use a loop and create a list of dictionaries.
# 
# You can use Selenium or you can feed the source to BeautifulSoup. You should have approximately 160 rows.
# 
# You'll probably need to find the table first, then the rows inside, then the cells inside of each row. You'll probably use lots of list indexing. I might recommend XPath for finding the table.
# 
# *Tip: If you get a "list index out of range" error, it's probably due to an issue involving `thead` vs `tbody` elements. What are they? What are they for? What's in them? There are a few ways to troubleshoot it.*

# In[9]:


# Get the table
table = driver.find_element(By.ID, "resultstable_inspections")

# Get the rows
rows = table.find_elements(By.TAG_NAME, "tr")

# Create a list:

inspections = []
# For each row:
for row in rows[1:]:
    
    # Create a dictionary
    data = {}
    # Get the cells
    cells = row.find_elements(By.TAG_NAME, "td")
    
    # Get the link
    link = cells[0].find_element(By.TAG_NAME, "a")
    data['inspection_num'] = link.text
    data['url'] = link.get_attribute('href')
    
    # For the rest of the cells get the text
    data['date'] = cells[1].text
    data['status'] = cells[2].text
    data['type_description'] = cells[3].text
    inspections.append(data)
inspections


# In[10]:


df = pd.DataFrame(inspections)
df.to_csv("Inspections - 400 E 41ST ST.csv", index=False)


# In[11]:


df = pd.read_csv("Inspections - 400 E 41ST ST.csv")
df


# In[ ]:





# ### Bonus preview of Wednesday's content
# 
# **You prrrrrobably shouldn't do this one unless you want a real challenge.**
# 
# If you click the inspection number, it'll open up a new window that shows you details of the violations from that visit. Count the number of violations for each visit and save it in a new column called **num_violations**.
# 
# Save this file as `Inspections - 400 E 41ST ST - with counts.csv`.
# 
# Since clicking the link opens in a new window, we have to say "Hey Selenium, pay attention to that new window!" We do that with `driver.switch_to.window(driver.window_handles[-1])` (each window gets a `window_handle`, and we're just asking the driver to switch to the last one.). A rough sketch of what your code will look like is here:
# 
# ```python
# # Click the link that opens the new window
# 
# # Switch to the new window/tab
# driver.switch_to.window(driver.window_handles[-1])
# 
# # Do your scraping in here
# 
# # Close the new window/tab
# driver.close()
# 
# # Switch back to the original window/tab
# driver.switch_to.window(driver.window_handles[0])
# ```
# 
# You'll want to play around with them individually before you try it with the whole set - the ones that pass are very different pages than the ones with violations! There are a few ways to get the number of violations, some easier than others.

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




