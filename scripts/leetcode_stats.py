"""
leetcode_stats.py

Fetch LeetCode statistics using GraphQL API
Save output to data/leetcode.json
"""

import json
from pathlib import Path

import requests

USERNAME = "brilliantambuj5"

URL = "https://leetcode.com/graphql"

QUERY = """
query getUserProfile($username: String!) {

  matchedUser(username: $username) {

    username

    profile {
      ranking
      reputation
      starRating
    }

    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }

    badges {
      displayName
    }

  }
}
"""

variables = {
    "username": USERNAME
}

response = requests.post(
    URL,
    json={
        "query": QUERY,
        "variables": variables
    },
    timeout=30
)

response.raise_for_status()

result = response.json()

user = result["data"]["matchedUser"]

if user is None:
    raise Exception("LeetCode user not found.")

stats = {}

for item in user["submitStats"]["acSubmissionNum"]:
    stats[item["difficulty"]] = item["count"]

profile = user["profile"]

badges = [
    badge["displayName"]
    for badge in user.get("badges", [])
]

output = {

    "username": USERNAME,

    "ranking": profile["ranking"],

    "reputation": profile["reputation"],

    "star_rating": profile["starRating"],

    "total_solved": stats.get("All", 0),

    "easy": stats.get("Easy", 0),

    "medium": stats.get("Medium", 0),

    "hard": stats.get("Hard", 0),

    "badges": badges

}

Path("data").mkdir(exist_ok=True)

with open("data/leetcode.json", "w", encoding="utf8") as f:
    json.dump(output, f, indent=4)

print("=" * 50)
print("LeetCode statistics downloaded successfully")
print("=" * 50)

print(f"Username      : {USERNAME}")
print(f"Total Solved  : {output['total_solved']}")
print(f"Easy          : {output['easy']}")
print(f"Medium        : {output['medium']}")
print(f"Hard          : {output['hard']}")
print(f"Ranking       : {output['ranking']}")
print(f"Reputation    : {output['reputation']}")
print(f"Badges        : {len(badges)}")

print("=" * 50)