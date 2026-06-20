from flask import Flask, Response
import requests
from bs4 import BeautifulSoup
from src.generate_svg import generate_svg
import re
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def scanner():

    username = "Jaiyansh-4n6"

    url = f"https://github.com/users/{username}/contributions"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    generated_at = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

    month_labels = []

    for span in soup.select("span[aria-hidden='true']"):
        text = span.get_text(strip=True)
        if text in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]:
            month_labels.append(text)

    total_contributions = 0
    h2 = soup.select_one("h2")
    if h2:
        text = h2.get_text(strip=True)
        match = re.search(r"(\d+)", text)
        if match:
            total_contributions = int(match.group(1))

    rows = soup.select("tbody tr")
    contribution_data = []
    for row_index, tr in enumerate(rows):
        cells = tr.select("td[data-date]")
        for col_index, cell in enumerate(cells):
            contribution_data.append({
                "row": row_index,
                "col": col_index,
                "date": cell["data-date"],
                "level": int(cell["data-level"])})
    latest_date = max(
    item["date"]
    for item in contribution_data
)

    svg = generate_svg(contribution_data, total_contributions, generated_at, month_labels)

    return Response(
        svg,
        mimetype="image/svg+xml"
    )