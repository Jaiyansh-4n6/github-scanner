# src/parse_contri.py
from bs4 import BeautifulSoup
import json

with open("contributions.svg", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

cells = soup.select("td[data-date]")

data = []

for cell in cells:
    data.append({
        "date": cell["data-date"],
        "level": int(cell["data-level"])
    })

with open("contributions.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Found {len(data)} days")