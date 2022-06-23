import requests
data = requests.get(
    "https://api.disneyapi.dev/characters?page=2")
print(data.json())
