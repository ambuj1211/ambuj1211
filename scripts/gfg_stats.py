"""
gfg_stats.py

Fetch publicly available GeeksforGeeks profile information.

Output:
    data/gfg.json
"""

import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "brilliantambuj59"

URL = f"https://www.geeksforgeeks.org/user/{USERNAME}/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}


def extract_number(text: str):
    digits = "".join(ch for ch in text if ch.isdigit())
    if digits:
        return int(digits)
    return None


def main():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    output = {
        "username": USERNAME,
        "profile_url": URL,
        "coding_score": None,
        "institute_rank": None,
        "problems_solved": None,
    }

    text = soup.get_text(" ", strip=True)

    if "Coding Score" in text:

        idx = text.find("Coding Score")

        snippet = text[idx:idx + 80]

        output["coding_score"] = extract_number(snippet)

    if "Institute Rank" in text:

        idx = text.find("Institute Rank")

        snippet = text[idx:idx + 80]

        output["institute_rank"] = extract_number(snippet)

    if "Problem" in text:

        idx = text.find("Problem")

        snippet = text[idx:idx + 120]

        output["problems_solved"] = extract_number(snippet)

    Path("data").mkdir(exist_ok=True)

    with open("data/gfg.json", "w", encoding="utf8") as fp:
        json.dump(output, fp, indent=4)

    print("=" * 50)
    print("GeeksforGeeks profile downloaded")
    print("=" * 50)

    for key, value in output.items():
        print(f"{key:20}: {value}")

    print("=" * 50)


if __name__ == "__main__":
    main()