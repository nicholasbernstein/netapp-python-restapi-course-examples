```python
import requests
news_url = "http://68k.news/"

response = requests.get(news_url)
t=response.text
f = open("news.html", "w")
f.write(t)
f.close()
```

If you have several python modules, you can list them in  a file called "requirements.txt"

## rest api example

```python
import requests
import json
from beautifultable import BeautifulTable

# there's a lot of results, so we'll narrow it down
uid = 1

# this is a site that provides a public rest api with fake data
api_url="https://jsonplaceholder.typicode.com/todos/?userid=" + uid

# use the requestions module to get the response from the site
response = requests.get(api_url)

# use the response.json output to create a dict from the json output
todoDict = response.json()

# This is just something so we can see that we're really getting data
# to do something with
table = BeautifulTable()
table.columns.headers = ["Todo", "done"]
for item in todoDict:
    table.rows.append([item['title'], item['completed']])
print(table)
```
