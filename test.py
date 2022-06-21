import requests
data = requests.get(
    "http://universities.hipolabs.com/search?country=madagascar")
print(data.json())
