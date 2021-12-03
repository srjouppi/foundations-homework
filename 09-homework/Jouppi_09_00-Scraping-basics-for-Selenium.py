#!/usr/bin/env python
# coding: utf-8

# # Scraping basics for Selenium
# 
# If you feel comfortable with scraping, you're free to skip this notebook.

# In[ ]:


# Greetings! This is the assignment the way that I filled it out before I watched
# The video tuturial you sent over.
# I went through the tutorial and it made a lot more since. Just figured I would
# Show you how I initially tackled it.


# ## Part 0: Imports
# 
# Import what you need to use Selenium, and start up a new Chrome to use for scraping. You might want to copy from the [Selenium snippets](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-snippets/) page.
# 
# **You only need to do `driver = webdriver.Chrome(...)` once,** every time you do it you'll open a new Chrome instance. You'll only need to run it again if you close the window (or want another Chrome, for some reason).

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


from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; hu-HU; rv:1.7.8) Gecko/20050511 Firefox/1.0.4'}


# In[5]:


driver = webdriver.Chrome(ChromeDriverManager().install())


# In[3]:





# ## Part 1: Scraping by class
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-class.html, printing out the title, subhead, and byline.

# In[14]:


driver.get("http://jonathansoma.com/lede/static/by-class.html") 


# In[ ]:





# In[7]:


doc = BeautifulSoup(driver.page_source)

for title in doc.select(".title"):
    print(title.text)


# In[8]:


for subhead in doc.select(".subhead"):
    print(subhead.text)


# In[9]:


for byline in doc.select(".byline"):
    print(byline.text)


# In[15]:


titles = driver.find_elements(By.CLASS_NAME, "title")
for title in titles:
    print(title.text)


# ## Part 2: Scraping using tags
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-tag.html, printing out the title, subhead, and byline.

# In[17]:


driver.get("http://jonathansoma.com/lede/static/by-tag.html") 
doc = BeautifulSoup(driver.page_source)


# In[18]:


for header in doc.select("h1"):
    print(header.text)


# In[21]:


for subhead in doc.select("h3"):
    print(subhead.text)


# In[22]:


for byline in doc.select("p"):
    print (byline.text)


# In[ ]:





# In[20]:


for item in doc.select("body"):
    print(item.text)


# ## Part 3: Scraping using a single tag
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-list.html, printing out the title, subhead, and byline.
# 
# > **This will be important for the next few:** if you scrape multiples, you have a list. Even though it's Seleninum, you can use things like `[0]`, `[1]`, `[-1]` etc just like you would for a normal list.

# In[23]:


driver.get("http://jonathansoma.com/lede/static/by-list.html") 
doc = BeautifulSoup(driver.page_source)


# In[24]:


for item in doc.select("p"):
    print(item.text)


# In[ ]:





# ## Part 4: Scraping a single table row
# 
# Scrape the content at http://jonathansoma.com/lede/static/single-table-row.html, printing out the title, subhead, and byline.

# In[38]:


driver.get("http://jonathansoma.com/lede/static/single-table-row.html") 
doc = BeautifulSoup(driver.page_source)


# In[26]:


for item in doc.select_one("tr"):
    print(item.text)


# In[27]:


for item in doc.select("td"):
    print(item.text)


# ## Part 5: Saving into a dictionary
# 
# Scrape the content at http://jonathansoma.com/lede/static/single-table-row.html, saving the title, subhead, and byline into a single dictionary called `book`.
# 
# > Don't use pandas for this one!

# In[39]:


book_info = doc.select("td")


book = {}
book['title'] = book_info[0].text
book['subhead'] = book_info[1].text
book['byline'] = book_info[2].text

book


# In[ ]:





# In[ ]:





# ## Part 6: Scraping multiple table rows
# 
# Scrape the content at http://jonathansoma.com/lede/static/multiple-table-rows.html, printing out each title, subhead, and byline.
# 
# > You won't use pandas for this one, either!

# In[40]:


driver.get("http://jonathansoma.com/lede/static/multiple-table-rows.html") 
doc = BeautifulSoup(driver.page_source)


# In[41]:


book_info = doc.select("tr")

for entry in book_info:
    print(entry.text)


# In[ ]:





# ## Part 7: Scraping an actual table
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html, creating a list of dictionaries.
# 
# > Don't use pandas here, either!

# In[43]:


driver.get("http://jonathansoma.com/lede/static/the-actual-table.html") 
doc = BeautifulSoup(driver.page_source)


# In[57]:


# for book in books:
#     rows = book.select("td")
#     print(rows[0].text)
#     print(rows[1].text)
#     print(rows[2].text)
#     print("-----next book-----")
# books[0].select("td")

books = doc.select("tr")

book_dataset = []

for book in books:
    entries = book.select("td")
    book_info = {}
    book_info['title'] = entries[0].text
    book_info['subhead'] = entries[1].text
    book_info['byline'] = entries[2].text
    # Every time through the loop
    # we add another dictionary of a book
    # to our dataset
    book_dataset.append(book_info)
book_dataset


# In[ ]:





# In[ ]:





# ## Part 8: Scraping multiple table rows into a list of dictionaries
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html, creating a pandas DataFrame.
# 
# > There are two ways to do this one! One uses just pandas, the other one uses the result from Part 7.

# In[58]:


df = pd.DataFrame(book_dataset)
df


# In[ ]:





# In[ ]:





# ## Part 9: Scraping into a file
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html and save it as `output.csv`

# In[ ]:





# In[61]:


table = driver.find_element(By.ID, 'booklist')
df = pd.read_html(table.get_attribute('outerHTML'))[0]
df.to_csv("books.csv", index=False)


# In[ ]:




