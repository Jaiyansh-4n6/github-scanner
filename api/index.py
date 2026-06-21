from flask import Flask, Response
import requests
from bs4 import BeautifulSoup
from src.generate_svg import generate_svg
import re
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

@app.route("/")
def scanner():

    username = "Jaiyansh-4n6"

    url = f"https://github.com/users/{username}/contributions"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    generated_at = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S IST")

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
    
    active_days = sum(
        1 for item in contribution_data
        if item["level"] > 0
    )

    days = sorted(
        contribution_data,
        key=lambda x: x["date"]
    )

    longest_streak = 0
    current_streak = 0
    streak = 0
    longest_start = ""
    longest_end = ""
    temp_start = ""

    for day in days:
        if day["level"] > 0:
            if streak == 0:
                temp_start = day["date"]
            streak += 1

            if streak > longest_streak:
                longest_streak = streak
                longest_start = temp_start
                longest_end = day["date"]

        else:
            streak = 0

    current_end = ""
    current_start = ""

    for day in reversed(days):
        if day["level"] > 0:
            if current_streak == 0:
                current_end = day["date"]

            current_streak += 1
            current_start = day["date"]

        else:
            break

    current_start = datetime.strptime(current_start, "%Y-%m-%d").strftime("%b %d")
    current_end = datetime.strptime(current_end, "%Y-%m-%d").strftime("%b %d")

    longest_start = datetime.strptime(longest_start, "%Y-%m-%d").strftime("%b %d")
    longest_end = datetime.strptime(longest_end, "%Y-%m-%d").strftime("%b %d")

    svg = generate_svg(contribution_data, total_contributions, generated_at,
                    month_labels, current_streak, longest_streak, active_days,
                    current_start, current_end, longest_start, longest_end)

    return Response(
        svg,
        mimetype="image/svg+xml"
    )