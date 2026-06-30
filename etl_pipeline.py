#!/usr/bin/env python
# coding: utf-8

# In[40]:


import requests

response = requests.get('https://jsonplaceholder.typicode.com/users')
users_data = response.json()


# In[41]:


print(users_data[0])


# In[42]:


response = requests.get('https://jsonplaceholder.typicode.com/posts')
posts_data = response.json()


# In[43]:


print(posts_data[0])


# In[44]:


import pandas as pd

users_df = pd.DataFrame(users_data)
posts_df = pd.DataFrame(posts_data)

print(users_df.head())
print(posts_df.head())


# In[45]:


users_df['city'] = users_df['address'].apply(lambda x: x['city'])
users_df['company_name'] = users_df['company'].apply(lambda x: x['name'])
users_df['zipcode'] = users_df['address'].apply(lambda x: x['zipcode'])
users_df[['id', 'name', 'city', 'company_name','zipcode']]


# In[46]:


users_clean = users_df[['id', 'name', 'username', 'email', 'city', 'company_name', 'zipcode']]


# In[47]:


users_clean.head()


# In[48]:


result = posts_df.merge(
    users_clean,
    left_on='userId',
    right_on='id',
    how='left'
)

result = result.rename(columns={'id_x': 'post_id', 'id_y': 'user_id'})


# In[49]:


print(result.columns)


# In[50]:


final_df = result[['user_id', 'name', 'city', 'company_name', 'post_id', 'title']]


# In[51]:


final_df.head()


# In[52]:


import sqlite3

conn = sqlite3.connect('project1.db')   # creates a database FILE
final_df.to_sql('user_posts', conn, if_exists='replace', index=False)


# In[53]:


check = pd.read_sql('SELECT * FROM user_posts LIMIT 5', conn)
print(check)


# Which city's users post the most?

# In[54]:


query = """
SELECT city, COUNT(*) AS post_count
FROM user_posts
GROUP BY city
ORDER BY post_count DESC;
"""

result = pd.read_sql(query, conn)
print(result)


# Find each company_name and how many TOTAL posts their employees have written, sorted highest to lowest.

# In[56]:


query2 = """
SELECT company_name, COUNT(*) AS post_count
FROM user_posts
GROUP BY company_name
ORDER BY post_count DESC;
"""

result2 = pd.read_sql(query2, conn)
print(result2)


# Find the user (name) who has written the MOST posts overall — just the top 1 user.

# In[58]:


query3 = """
SELECT name, COUNT(*) AS post_count
FROM user_posts
GROUP BY name
ORDER BY post_count DESC limit 1;
"""

result3 = pd.read_sql(query3, conn)
print(result3)


# In[ ]:




