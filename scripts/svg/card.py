from .colors import *


class SVGCard:

    def __init__(self, width, height):

        self.width = width

        self.height = height

        self.data = []

        self.start()

    def start(self):

        self.data.append(f"""
<svg
xmlns="http://www.w3.org/2000/svg"
width="{self.width}"
height="{self.height}"
viewBox="0 0 {self.width} {self.height}">
""")

        self.data.append(f"""

<rect
x="0"
y="0"
rx="20"
width="{self.width}"
height="{self.height}"
fill="{BACKGROUND}"/>

<rect
x="5"
y="5"
rx="18"
width="{self.width-10}"
height="{self.height-10}"
fill="{CARD}"
stroke="{BORDER}"
stroke-width="2"/>

""")

    def title(self, text):

        self.data.append(f"""

<text
x="30"
y="50"
font-size="28"
font-family="Segoe UI"
font-weight="bold"
fill="{TITLE}">

{text}

</text>

""")

    def item(self, y, label, value):

        self.data.append(f"""

<text
x="40"
y="{y}"
font-size="20"
fill="{TEXT}">

{label}

</text>

<text
x="{self.width-40}"
y="{y}"
font-size="20"
text-anchor="end"
fill="{GREEN}"
font-weight="bold">

{value}

</text>

""")

    def save(self, path):

        self.data.append("</svg>")

        with open(path, "w", encoding="utf8") as fp:

            fp.write("".join(self.data))