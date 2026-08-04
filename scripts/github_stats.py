"""
github_stats.py

Fetch GitHub profile statistics and save them to data/github.json
"""

import json
from pathlib import Path

from github import Github

# ==========================
# CONFIGURATION
# ==========================

USERNAME = "ambuj1211"

# Optional:
# Create a Personal Access Token (PAT) and set it as an environment variable:
#   GITHUB_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
#
# Without a token, the script still works but GitHub rate limits requests.

import os

TOKEN = os.getenv("GITHUB_TOKEN")

# ==========================
# CONNECT TO GITHUB
# ==========================

if TOKEN:
    github = Github(TOKEN)
else:
    github = Github()

user = github.get_user(USERNAME)

# ==========================
# BASIC PROFILE INFO
# ==========================

profile = {
    "username": user.login,
    "name": user.name,
    "bio": user.bio,
    "company": user.company,
    "location": user.location,
    "blog": user.blog,
    "followers": user.followers,
    "following": user.following,
    "public_repos": user.public_repos,
}

# ==========================
# REPOSITORIES
# ==========================

repos = list(user.get_repos())

total_stars = 0
languages = {}

repository_data = []

for repo in repos:

    total_stars += repo.stargazers_count

    try:
        repo_languages = repo.get_languages()

        for lang, bytes_used in repo_languages.items():
            languages[lang] = languages.get(lang, 0) + bytes_used

    except Exception:
        pass

    repository_data.append({
        "name": repo.name,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "language": repo.language,
        "url": repo.html_url,
    })

# Sort repositories by stars

repository_data.sort(
    key=lambda x: x["stars"],
    reverse=True
)

# Sort languages

languages = dict(
    sorted(
        languages.items(),
        key=lambda x: x[1],
        reverse=True
    )
)

# ==========================
# FINAL DATA
# ==========================

output = {
    "profile": profile,
    "total_stars": total_stars,
    "languages": languages,
    "repositories": repository_data,
}

# ==========================
# SAVE JSON
# ==========================

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

output_file = data_dir / "github.json"

with open(output_file, "w", encoding="utf-8") as fp:
    json.dump(output, fp, indent=4)

print("=" * 50)
print("GitHub statistics downloaded successfully!")
print("=" * 50)

print(f"User           : {profile['username']}")
print(f"Followers      : {profile['followers']}")
print(f"Following      : {profile['following']}")
print(f"Repositories   : {profile['public_repos']}")
print(f"Total Stars    : {total_stars}")
print(f"Languages      : {len(languages)}")
print(f"Saved File     : {output_file}")

print("=" * 50)