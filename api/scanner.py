import requests
from bs4 import BeautifulSoup
from src.generate_svg import generate_svg


def handler(request):

    username = "Jaiyansh-4n6"

    url = f"https://github.com/users/{username}/contributions"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    cells = soup.select("td[data-date]")

    contribution_data = []

    for cell in cells:
        contribution_data.append({
            "date": cell["data-date"],
            "level": int(cell["data-level"])
        })

    svg = generate_svg(contribution_data)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "image/svg+xml"
        },
        "body": svg
    }