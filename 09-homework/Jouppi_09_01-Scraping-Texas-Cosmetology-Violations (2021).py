#!/usr/bin/env python
# coding: utf-8

# # Texas Cosmetologist Violations
# 
# Texas has a system for [searching for license violations](https://www.tdlr.texas.gov/cimsfo/fosearch.asp). You're going to search for cosmetologists!

# ## Setup: Import what you'll need to scrape the page
# 
# We'll be using Selenium for this, *not* BeautifulSoup and requests.

# In[2]:


import pandas as pd

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from webdriver_manager.chrome import ChromeDriverManager
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; hu-HU; rv:1.7.8) Gecko/20050511 Firefox/1.0.4'}
driver = webdriver.Chrome(ChromeDriverManager().install())


# ## Starting your search
# 
# Starting from [here](https://www.tdlr.texas.gov/cimsfo/fosearch.asp), search for cosmetologist violations for people with the last name **Nguyen**.

# In[3]:


driver.get("https://www.tdlr.texas.gov/cimsfo/fosearch.asp")


# In[4]:


driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/section/div/div/table/tbody/tr/td/form/table/tbody/tr[3]/td/select/option[10]").click()


# In[5]:


driver.find_element(By.ID, "pht_lnm").send_keys("Nguyen")


# In[6]:


driver.find_element(By.NAME, "B1").click()


# In[ ]:





# ## Scraping
# 
# Once you are on the results page, do this. **I step you through things bit by bit, so it's going to be a little different than we did in class.** Also, no `pd.read_html` allowed because this isn't actual tabular data!
# 
# > You can use either Selenium by itself or Selenium+BeautifulSoup to scrape the results page. The choice is up to you!

# ### Loop through each result and print the entire row
# 
# Okay wait, maybe not, i's a heck of a lot of rows. Use `[:10]` to only do the first ten! For example, if you saved the table rows into `results` you might do something like this:
# 
# ```python
# for result in results[:10]:
#     print(result)
# ```
# 
# Although you'd want to print out the text from the row (I give example output below).
# 
# > *Tip: If you're using Selenium, `By.TAG_NAME` is used if you don't have a class or ID. If you're using BeautifulSoup, just do your normal thing.*

# In[7]:


# SELENIUM WAY
rows = driver.find_elements(By.TAG_NAME, "tr")
rows
for row in rows[:10]:
    cells = row.find_elements(By.TAG_NAME, "td")
    for cell in cells:
        print(cell.text)


# In[8]:


# BEAUTIFUL SOUP WAY ... formatting is v different
from bs4 import BeautifulSoup
doc = BeautifulSoup(driver.page_source)

rows = doc.find_all("tr")
rows

for row in rows[:10]:
    cells = row.find_all("td")
    for cell in cells:
        print(cell.text)


# In[ ]:





# The result should look something like this:
# 
# ```
# Name and Location Order Basis for Order
# NGUYEN, THANH
# City: FRISCO
# County: COLLIN
# Zip Code: 75034
# 
# 
# License #: 790672
# 
# Complaint # COS20210004784 Date: 11/16/2021
# 
# Respondent is assessed an administrative penalty in the amount of $1,875. Respondent failed to clean and sanitize whirlpool foot spas as required at the end of each day, the Department is charging 2 violations; Respondent operated a cosmetology salon without the appropriate license.
# NGUYEN, LONG D
# City: SAN SABA
# County: SAN SABA
# Zip Code: 76877
# ```

# ### Loop through each result and print each person's name
# 
# You'll get an error because the first one doesn't have a name. How do you make that not happen?! If you want to ignore an error, you use code like this:
# 
# ```python
# try:
#    # try to do something
# except:
#    print("It didn't work')
# ```
# 
# It should help you out. If you don't want to print anything when there's an error, you can type `pass` instead of the `print` statement.
# 
# **Why doesn't the first one have a name?**
# 
# Output should look like this:
# 
# ```
# Doesn't have a name
# NGUYEN, THANH
# NGUYEN, LONG D
# NGUYEN, LUCIE HUONG
# NGUYEN, CHINH
# NGUYEN, JIMMY
# ```
# 
# * *Tip: The name has a class you can use. The class name is reused in a lot of places, but because it's the first one you don't have to worry about that!*
# * *Tip: Instead of searching across the entire page – `driver.find_element` or `doc.select_one` – you should be doing your searching just inside of each **row** (I used this technique in the beginning of class with BeautifulSoup when we were scraping the books page)* 

# In[9]:


rows = driver.find_elements(By.TAG_NAME, "tr")
rows
for row in rows[0:10]:
    try:
        name = row.find_element(By.TAG_NAME,"span")
        print(name.text)
    except:
        print("no name :(")


# In[10]:


# BEAUTIFUL SOUP WAY
from bs4 import BeautifulSoup
doc = BeautifulSoup(driver.page_source)

rows = doc.find_all("tr")
rows

for row in rows[:10]:
    try:
        print(row.find("span").text)
    except:
        print("Doesn't have a name")


# ## Loop through each result, printing each violation description ("Basis for order")
# 
# Your results should look something like:
# 
# ```
# Doesn't have a violation
# Respondent failed to clean and sanitize whirlpool foot spas as required at the end of each day, the Department is charging 2 violations; Respondent operated a cosmetology salon without the appropriate license.
# Respondent failed to keep a record of the date and time of each foot spa daily or bi-weekly cleaning and if the foot spa was not used, the Department is charging 2 violations; Respondent failed to clean, disinfect, and sterilize manicure and pedicure implements after each use; Respondent failed to clean and disinfect manicure tables prior to use for each client.
# ...
# ```
# 
# > - *Tip: You'll get an error even if you're ALMOST right - which row is causing the problem?*
# > - *Tip: If you're using Selenium by itself, you can get the HTML of something by doing `.get_attribute('innerHTML')` – that way it'll look like BeautifulSoup when you print it. It might help you diagnose your issue!*
# > - *Tip: Or I guess you could just skip the one with the problem...*

# In[11]:


rows = driver.find_elements(By.TAG_NAME, "tr")
for row in rows[0:10]:
    try:
        cells = row.find_elements(By.TAG_NAME, "td")
        print(cells[2].text)
    except:
        print("no complaint")


# In[12]:


# BEAUTIFUL SOUP WAY
# I couldn't loop through the list because the first part was empty 
# (NO TDs in the header row)
# so I just skipped the first row. 
for row in rows[1:10]:
    cells = row.find_all("td")
    print(cells[2].text)


# ## Loop through each result, printing the complaint number
# 
# Output should look like this:
# 
# ```
# Doesn't have a complaint number
# COS20210004784
# COS20210009745
# COS20210011484
# ...
# ```
# 
# - *Tip: Think about the order of the elements. Can you count from the opposite direction than you normally do?*

# In[13]:


# SELENIUM WAY
# Why can't we just skip the first row?
rows = driver.find_elements(By.TAG_NAME, "tr")
rows
for row in rows[:10]:
    try:
        cells = row.find_elements(By.TAG_NAME, "td")
        first_cell = cells[0].find_elements(By.TAG_NAME,"span")
        print(first_cell[-1].text)
    except:
        print("doesn't work")


# ## Saving the results
# 
# ### Loop through each result to create a list of dictionaries
# 
# Each dictionary must contain
# 
# - Person's name
# - Violation description
# - Violation number
# - License Numbers
# - Zip Code
# - County
# - City
# 
# Create a new dictionary for each result (except the header).
# 
# Based on what you print out, the output might look something like:
# 
# ```
# This row is broken: Name and Location Order Basis for Order
# {'name': 'NGUYEN, THANH', 'city': 'FRISCO', 'county': 'COLLIN', 'zip_code': '75034', 'complaint_no': 'COS20210004784', 'license_numbers': '790672', 'complaint': 'Respondent failed to clean and sanitize whirlpool foot spas as required at the end of each day, the Department is charging 2 violations; Respondent operated a cosmetology salon without the appropriate license.'}
# {'name': 'NGUYEN, LONG D', 'city': 'SAN SABA', 'county': 'SAN SABA', 'zip_code': '76877', 'complaint_no': 'COS20210009745', 'license_numbers': '760420, 1620583', 'complaint': 'Respondent failed to keep a record of the date and time of each foot spa daily or bi-weekly cleaning and if the foot spa was not used, the Department is charging 2 violations; Respondent failed to clean, disinfect, and sterilize manicure and pedicure implements after each use; Respondent failed to clean and disinfect manicure tables prior to use for each client.'}
# ```
# 
# > *Tip: If you want to ask for the "next sibling," you can't use `find_next_sibling` in Selenium, you need to use `element.find_element_by_xpath("following-sibling::div")` to find the next div, or `element.find_element_by_xpath("following-sibling::*")` to find the next anything.

# In[14]:


rows = driver.find_elements(By.TAG_NAME, "tr")
dataset = []
for row in rows[0:10]:
    try:
        data = {}
        cells = row.find_elements(By.TAG_NAME, "td")
        info = cells[0].find_elements(By.TAG_NAME,"span")
        data['name'] = info[0].text
        data['city'] = info[2].text
        data['county'] = info[4].text
        data['zip'] = info[6].text
        data['license_num'] = info[8].text
        data['complaint'] = info[10].text
        dataset.append(data)
    except:
        print("This row is broken:", row.text)
dataset


# ### Save that to a CSV named `output.csv`
# 
# The dataframe should look something like...
# 
# |index|name|city|county|zip_code|complaint_no|license_numbers|complaint|
# |---|---|---|---|---|---|---|---|
# |0|NGUYEN, THANH|FRISCO|COLLIN|75034|COS20210004784|790672|Respondent failed to clean and sanitize whirlp...|
# |1|NGUYEN, LONG D|SAN SABA|SAN SABA|76877|COS20210009745|760420, 1620583|Respondent failed to keep a record of the date...|
# 
# 
# - *Tip: If you send a list of dictionaries to `pd.DataFrame(...)`, it will create a dataframe out of that list!*

# In[15]:


import pandas as pd
df = pd.DataFrame(dataset)
df


# In[17]:


df.to_csv("nguyen_cosmetologists_complaints2.csv", index=False)


# ### Open the CSV file and examine the first few. Make sure you didn't save an extra weird unnamed column.

# In[18]:


df = pd.read_csv("nguyen_cosmetologists_complaints2.csv")
df

