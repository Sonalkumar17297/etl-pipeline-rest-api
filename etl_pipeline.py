#!/usr/bin/env python
# coding: utf-8


import requests

response = requests.get('https://jsonplaceholder.typicode.com/users')
users_data = response.json()




print(users_data[0])



response = requests.get('https://jsonplaceholder.typicode.com/posts')
posts_data = response.json()


print(posts_data[0])


import pandas as pd

users_df = pd.DataFrame(users_data)
posts_df = pd.DataFrame(posts_data)

print(users_df.head())
print(posts_df.head())



users_df['city'] = users_df['address'].apply(lambda x: x['city'])
users_df['company_name'] = users_df['company'].apply(lambda x: x['name'])
users_df['zipcode'] = users_df['address'].apply(lambda x: x['zipcode'])
users_df[['id', 'name', 'city', 'company_name','zipcode']]



users_clean = users_df[['id', 'name', 'username', 'email', 'city', 'company_name', 'zipcode']]



users_clean.head()

result = posts_df.merge(
    users_clean,
    left_on='userId',
    right_on='id',
    how='left'
)

result = result.rename(columns={'id_x': 'post_id', 'id_y': 'user_id'})


print(result.columns)



final_df = result[['user_id', 'name', 'city', 'company_name', 'post_id', 'title']]


final_df.head()


import sqlite3

conn = sqlite3.connect('project1.db')   # creates a database FILE
final_df.to_sql('user_posts', conn, if_exists='replace', index=False)


check = pd.read_sql('SELECT * FROM user_posts LIMIT 5', conn)
print(check)


# Which city's users post the most?


query = """
SELECT city, COUNT(*) AS post_count
FROM user_posts
GROUP BY city
ORDER BY post_count DESC;
"""

result = pd.read_sql(query, conn)
print(result)


# Find each company_name and how many TOTAL posts their employees have written, sorted highest to lowest.


query2 = """
SELECT company_name, COUNT(*) AS post_count
FROM user_posts
GROUP BY company_name
ORDER BY post_count DESC;
"""

result2 = pd.read_sql(query2, conn)
print(result2)


# Find the user (name) who has written the MOST posts overall — just the top 1 user.

query3 = """
SELECT name, COUNT(*) AS post_count
FROM user_posts
GROUP BY name
ORDER BY post_count DESC limit 1;
"""

result3 = pd.read_sql(query3, conn)
print(result3)
