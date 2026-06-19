import requests

USERNAME = "Jaiyansh-4n6"

url = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(url)

print("Status:", response.status_code)

with open("contributions.svg", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Saved contributions.svg")