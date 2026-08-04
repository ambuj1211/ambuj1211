"""
update_readme.py

Reads JSON data from:
    data/github.json
    data/leetcode.json
    data/gfg.json

Uses:
    templates/README.template.md

Generates:
    README.md
"""

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
TEMPLATE_DIR = ROOT / "templates"

README_TEMPLATE = "README.template.md"
OUTPUT_README = ROOT / "README.md"


def load_json(filename):
    path = DATA_DIR / filename

    if not path.exists():
        print(f"Missing file: {path}")
        return {}

    with open(path, "r", encoding="utf-8") as fp:
        return json.load(fp)


def main():

    github = load_json("github.json")
    leetcode = load_json("leetcode.json")
    gfg = load_json("gfg.json")

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = env.get_template(README_TEMPLATE)

    markdown = template.render(
        github=github,
        leetcode=leetcode,
        gfg=gfg
    )

    OUTPUT_README.write_text(
        markdown,
        encoding="utf-8"
    )

    print("=" * 60)
    print("README generated successfully")
    print("=" * 60)
    print(OUTPUT_README)
    print("=" * 60)


if __name__ == "__main__":
    main()