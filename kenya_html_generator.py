import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape


def product_section(index, row):
    env1 = Environment(
        loader=PackageLoader("kenya_html_generator"), autoescape=select_autoescape()
    )
    template = env1.get_template("kenya_item.html")
    row1 = False
    row2 = False
    if (index % 2) == 0:
        row1 = True
    else:
        row2 = True
    product_name = row["Name"]
    unit_price = row["Unit price"]
    currency = row["Currency"]
    code = row["Short code"]
    img = ""
    if row["category"] == "Afrigas":
        img = "scr/afrigas.webp"
    elif row["category"] == "K-Gas":
        img = "scr/k-gas.webp"
    elif row["category"] == "Total":
        img = "scr/total.webp"
    else:
        img = "scr/other.webp"

    return template.render(
        row1=row1,
        row2=row2,
        ItemName=product_name,
        UnitPrice=str(unit_price),
        currency=currency,
        ShortCode=code,
        img=img,
    )


env = Environment(
    loader=PackageLoader("kenya_html_generator"), autoescape=select_autoescape()
)
template = env.get_template("kenya_index.html")

df = pd.read_csv("KenyaProduct.csv")


with open("index.html", "w") as html_file:
    middle = ""
    for key, item in df.iterrows():
        middle = middle + product_section(key, item)

    html_file.write(template.render(category=middle))
    html_file.close()
