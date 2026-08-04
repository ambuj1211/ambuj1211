"""
generate_svg.py

Generate self-hosted SVG statistic cards for:
    1. GitHub
    2. LeetCode
    3. GeeksforGeeks

Input:
    data/github.json
    data/leetcode.json
    data/gfg.json

Output:
    assets/github.svg
    assets/leetcode.svg
    assets/gfg.svg

Author: Brilliant Ambuj
"""

from pathlib import Path
from html import escape
import json
import math


# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATA = ROOT / "data"
ASSETS = ROOT / "assets"

ASSETS.mkdir(parents=True, exist_ok=True)


# ============================================================
# THEME
# ============================================================

BACKGROUND_1 = "#0D1117"
BACKGROUND_2 = "#161B22"

ROW_BACKGROUND = "#21262D"

BORDER = "#30363D"

TITLE = "#58A6FF"

TEXT = "#C9D1D9"
SUBTEXT = "#8B949E"

GREEN = "#3FB950"
GREEN_DARK = "#238636"

BLUE = "#58A6FF"

ORANGE = "#D29922"

RED = "#F85149"

PURPLE = "#A371F7"

YELLOW = "#E3B341"

CYAN = "#39C5CF"

GRAY = "#484F58"


# ============================================================
# JSON UTILITIES
# ============================================================

def load_json(filename):
    """
    Load JSON file.

    Returns an empty dictionary if the file cannot be loaded.
    """

    path = DATA / filename

    if not path.exists():
        print(f"[WARNING] Missing file: {path}")
        return {}

    try:

        with open(path, "r", encoding="utf-8") as fp:
            return json.load(fp)

    except json.JSONDecodeError as error:

        print(f"[ERROR] Invalid JSON: {path}")
        print(error)

        return {}

    except Exception as error:

        print(f"[ERROR] Unable to load: {path}")
        print(error)

        return {}


# ============================================================
# GENERAL HELPERS
# ============================================================

def safe(value, default=0):
    """
    Replace None values with default.
    """

    if value is None:
        return default

    return value


def number(value):
    """
    Format numbers with commas.

    Example:
        123456 -> 123,456
    """

    try:
        return f"{int(value):,}"

    except (TypeError, ValueError):
        return str(value)


def svg_text(value):
    """
    Escape text before inserting into SVG/XML.
    """

    if value is None:
        return "N/A"

    return escape(str(value))


# ============================================================
# LOAD DATA
# ============================================================

github = load_json("github.json")

leetcode = load_json("leetcode.json")

gfg = load_json("gfg.json")


# ============================================================
# BASE SVG CARD
# ============================================================

class SVGCard:

    WIDTH = 620

    HEADER_HEIGHT = 78

    ROW_HEIGHT = 50

    FOOTER_HEIGHT = 45

    def __init__(self, title, filename, accent=BLUE):

        self.title = title

        self.filename = filename

        self.accent = accent

        self.rows = []

    # --------------------------------------------------------

    def add(self, label, value, color=None):

        if color is None:
            color = GREEN

        self.rows.append(
            {
                "label": label,
                "value": value,
                "color": color
            }
        )

    # --------------------------------------------------------

    def generate_header(self, height):

        return f"""
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{self.WIDTH}"
    height="{height}"
    viewBox="0 0 {self.WIDTH} {height}"
>

<defs>

    <linearGradient
        id="background"
        x1="0%"
        y1="0%"
        x2="100%"
        y2="100%"
    >

        <stop
            offset="0%"
            stop-color="{BACKGROUND_1}"
        />

        <stop
            offset="100%"
            stop-color="{BACKGROUND_2}"
        />

    </linearGradient>


    <filter id="shadow">

        <feDropShadow
            dx="0"
            dy="4"
            stdDeviation="5"
            flood-opacity="0.25"
        />

    </filter>

</defs>


<rect
    x="2"
    y="2"
    width="{self.WIDTH - 4}"
    height="{height - 4}"
    rx="18"

    fill="url(#background)"

    stroke="{BORDER}"

    stroke-width="2"
/>


<text
    x="30"
    y="48"

    font-family="Segoe UI, Arial, sans-serif"

    font-size="28"

    font-weight="700"

    fill="{self.accent}"
>

    {svg_text(self.title)}

</text>


<line
    x1="25"
    y1="66"

    x2="{self.WIDTH - 25}"
    y2="66"

    stroke="{BORDER}"

    stroke-width="1"
/>

"""

    # --------------------------------------------------------

    def generate_rows(self):

        result = ""

        y = 105

        for row in self.rows:

            label = svg_text(row["label"])

            value = svg_text(number(row["value"]))

            color = row["color"]

            result += f"""

<rect
    x="22"
    y="{y - 29}"

    width="{self.WIDTH - 44}"

    height="40"

    rx="10"

    fill="{ROW_BACKGROUND}"
/>


<text
    x="42"
    y="{y}"

    font-family="Segoe UI, Arial, sans-serif"

    font-size="18"

    fill="{TEXT}"
>

    {label}

</text>


<rect
    x="{self.WIDTH - 120}"
    y="{y - 23}"

    width="80"

    height="28"

    rx="14"

    fill="{color}"
/>


<text
    x="{self.WIDTH - 80}"
    y="{y - 3}"

    text-anchor="middle"

    font-family="Segoe UI, Arial, sans-serif"

    font-size="15"

    font-weight="700"

    fill="#FFFFFF"
>

    {value}

</text>

"""

            y += self.ROW_HEIGHT

        return result

    # --------------------------------------------------------

    def generate_footer(self, height):

        return f"""

<line
    x1="25"

    y1="{height - 38}"

    x2="{self.WIDTH - 25}"

    y2="{height - 38}"

    stroke="{BORDER}"
/>


<text
    x="{self.WIDTH / 2}"

    y="{height - 15}"

    text-anchor="middle"

    font-family="Segoe UI, Arial, sans-serif"

    font-size="12"

    fill="{SUBTEXT}"
>

    Updated automatically using GitHub Actions

</text>


</svg>
"""

    # --------------------------------------------------------

    def save(self):

        height = (
            self.HEADER_HEIGHT
            + len(self.rows) * self.ROW_HEIGHT
            + self.FOOTER_HEIGHT
        )

        svg = self.generate_header(height)

        svg += self.generate_rows()

        svg += self.generate_footer(height)

        path = ASSETS / self.filename

        path.write_text(
            svg,
            encoding="utf-8"
        )

        print(f"[CREATED] {path}")


# ============================================================
# GITHUB CARD
# ============================================================

def generate_github():

    profile = github.get(
        "profile",
        {}
    )

    languages = github.get(
        "languages",
        {}
    )

    card = SVGCard(
        "GitHub",
        "github.svg",
        BLUE
    )

    card.add(
        "Followers",
        safe(profile.get("followers")),
        BLUE
    )

    card.add(
        "Following",
        safe(profile.get("following")),
        PURPLE
    )

    card.add(
        "Public Repositories",
        safe(profile.get("public_repos")),
        GREEN
    )

    card.add(
        "Total Stars",
        safe(github.get("total_stars")),
        YELLOW
    )

    card.add(
        "Languages",
        len(languages),
        CYAN
    )

    card.save()


# ============================================================
# LEETCODE CARD
# ============================================================

def generate_leetcode():

    card = SVGCard(
        "LeetCode",
        "leetcode.svg",
        ORANGE
    )

    card.add(
        "Total Solved",
        safe(leetcode.get("total_solved")),
        GREEN
    )

    card.add(
        "Easy",
        safe(leetcode.get("easy")),
        CYAN
    )

    card.add(
        "Medium",
        safe(leetcode.get("medium")),
        ORANGE
    )

    card.add(
        "Hard",
        safe(leetcode.get("hard")),
        RED
    )

    card.add(
        "Ranking",
        safe(
            leetcode.get("ranking"),
            "N/A"
        ),
        PURPLE
    )

    card.save()


# ============================================================
# DONUT CHART UTILITIES
# ============================================================

def polar_to_cartesian(cx, cy, radius, angle):

    angle_rad = math.radians(
        angle - 90
    )

    return (

        cx + radius * math.cos(angle_rad),

        cy + radius * math.sin(angle_rad)

    )


# ------------------------------------------------------------

def describe_arc(
    cx,
    cy,
    radius,
    start_angle,
    end_angle
):

    start = polar_to_cartesian(
        cx,
        cy,
        radius,
        end_angle
    )

    end = polar_to_cartesian(
        cx,
        cy,
        radius,
        start_angle
    )

    large_arc_flag = (

        "0"

        if end_angle - start_angle <= 180

        else "1"

    )

    return f"""
M {start[0]} {start[1]}

A {radius} {radius}

0

{large_arc_flag}

0

{end[0]} {end[1]}
"""


# ============================================================
# GFG ADVANCED CARD
# ============================================================

def generate_gfg():

    width = 620

    height = 470

    coding_score = safe(
        gfg.get("coding_score")
    )

    problems = safe(
        gfg.get("problems_solved")
    )

    institute_rank = safe(
        gfg.get("institute_rank"),
        "N/A"
    )

    articles = safe(
        gfg.get("articles_published")
    )


    # --------------------------------------------------------
    # Difficulty distribution
    # --------------------------------------------------------

    school = safe(
        gfg.get("school")
    )

    basic = safe(
        gfg.get("basic")
    )

    easy = safe(
        gfg.get("easy")
    )

    medium = safe(
        gfg.get("medium")
    )

    hard = safe(
        gfg.get("hard")
    )


    distribution = [

        ("School", school, PURPLE),

        ("Basic", basic, CYAN),

        ("Easy", easy, GREEN),

        ("Medium", medium, ORANGE),

        ("Hard", hard, RED),

    ]


    total_distribution = sum(

        item[1]

        for item in distribution

        if isinstance(
            item[1],
            (int, float)
        )

    )


    # --------------------------------------------------------
    # SVG start
    # --------------------------------------------------------

    svg = f"""
<svg
xmlns="http://www.w3.org/2000/svg"

width="{width}"

height="{height}"

viewBox="0 0 {width} {height}"
>


<defs>


<linearGradient
id="gfgBackground"

x1="0%"

y1="0%"

x2="100%"

y2="100%"
>


<stop
offset="0%"
stop-color="{BACKGROUND_1}"
/>


<stop
offset="100%"
stop-color="{BACKGROUND_2}"
/>


</linearGradient>


</defs>


<rect

x="2"

y="2"

width="{width - 4}"

height="{height - 4}"

rx="18"

fill="url(#gfgBackground)"

stroke="{BORDER}"

stroke-width="2"

/>


<text

x="30"

y="48"

font-family="Segoe UI, Arial, sans-serif"

font-size="28"

font-weight="700"

fill="{GREEN}"

>

GeeksforGeeks

</text>


<line

x1="25"

y1="66"

x2="595"

y2="66"

stroke="{BORDER}"

/>


<text

x="30"

y="105"

font-family="Segoe UI, Arial, sans-serif"

font-size="19"

font-weight="600"

fill="{TEXT}"

>

Problems Overview

</text>

"""


    # --------------------------------------------------------
    # Donut background
    # --------------------------------------------------------

    cx = 170

    cy = 225

    radius = 78


    svg += f"""

<circle

cx="{cx}"

cy="{cy}"

r="{radius}"

fill="none"

stroke="{GRAY}"

stroke-width="18"

opacity="0.35"

/>

"""


    # --------------------------------------------------------
    # Donut segments
    # --------------------------------------------------------

    if total_distribution > 0:

        current_angle = 0

        gap = 2

        for label, value, color in distribution:

            if not value:
                continue

            percentage = value / total_distribution

            angle = percentage * 360

            start_angle = current_angle + gap

            end_angle = current_angle + angle - gap


            if end_angle > start_angle:

                path = describe_arc(

                    cx,

                    cy,

                    radius,

                    start_angle,

                    end_angle

                )


                svg += f"""

<path

d="{path}"

fill="none"

stroke="{color}"

stroke-width="18"

stroke-linecap="round"

/>

"""


            current_angle += angle


    # --------------------------------------------------------
    # Donut center
    # --------------------------------------------------------

    svg += f"""

<text

x="{cx}"

y="{cy - 5}"

text-anchor="middle"

font-family="Segoe UI, Arial, sans-serif"

font-size="34"

font-weight="700"

fill="{TEXT}"

>

{svg_text(number(problems))}

</text>


<text

x="{cx}"

y="{cy + 25}"

text-anchor="middle"

font-family="Segoe UI, Arial, sans-serif"

font-size="14"

fill="{SUBTEXT}"

>

Problems Solved

</text>

"""


    # --------------------------------------------------------
    # Legend
    # --------------------------------------------------------

    legend_x = 325

    legend_y = 135


    for label, value, color in distribution:

        svg += f"""

<circle

cx="{legend_x}"

cy="{legend_y - 5}"

r="6"

fill="{color}"

/>


<text

x="{legend_x + 18}"

y="{legend_y}"

font-family="Segoe UI, Arial, sans-serif"

font-size="16"

fill="{TEXT}"

>

{svg_text(label)}

</text>


<text

x="555"

y="{legend_y}"

text-anchor="end"

font-family="Segoe UI, Arial, sans-serif"

font-size="16"

font-weight="700"

fill="{color}"

>

{svg_text(number(value))}

</text>

"""

        legend_y += 34


    # --------------------------------------------------------
    # Bottom statistics
    # --------------------------------------------------------

    stats = [

        (
            "Coding Score",
            coding_score,
            GREEN
        ),

        (
            "Problems Solved",
            problems,
            BLUE
        ),

        (
            "Institute Rank",
            institute_rank,
            ORANGE
        ),

        (
            "Articles Published",
            articles,
            PURPLE
        )

    ]


    x_positions = [

        85,

        235,

        385,

        535

    ]


    for x, item in zip(
        x_positions,
        stats
    ):

        label, value, color = item


        svg += f"""

<rect

x="{x - 65}"

y="345"

width="130"

height="75"

rx="12"

fill="{ROW_BACKGROUND}"

/>


<text

x="{x}"

y="375"

text-anchor="middle"

font-family="Segoe UI, Arial, sans-serif"

font-size="20"

font-weight="700"

fill="{color}"

>

{svg_text(number(value))}

</text>


<text

x="{x}"

y="400"

text-anchor="middle"

font-family="Segoe UI, Arial, sans-serif"

font-size="11"

fill="{SUBTEXT}"

>

{svg_text(label)}

</text>

"""


    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    svg += f"""

<text

x="{width / 2}"

y="450"

text-anchor="middle"

font-family="Segoe UI, Arial, sans-serif"

font-size="12"

fill="{SUBTEXT}"

>

Updated automatically using GitHub Actions

</text>


</svg>

"""


    path = ASSETS / "gfg.svg"

    path.write_text(
        svg,
        encoding="utf-8"
    )


    print(
        f"[CREATED] {path}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("Generating SVG profile cards")
    print("=" * 60)

    generate_github()

    generate_leetcode()

    generate_gfg()

    print("=" * 60)

    print(
        "SVG cards generated successfully."
    )

    print("=" * 60)

    print()


if __name__ == "__main__":

    main()