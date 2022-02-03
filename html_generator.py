import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape


def product_section(row):
    env1 = Environment(
        loader=PackageLoader("html_generator"), autoescape=select_autoescape()
    )
    template = env1.get_template("item.html")

    product_name = row["name"]
    unit_price = row["unit_price"]
    currency = row["currency"]
    code = row["short_code"]
    img = row["img"]

    return template.render(
        ItemName=product_name,
        UnitPrice=str(unit_price),
        currency=currency,
        ShortCode=code,
        img=img,
    )


def category_section(key, category_data):

    env1 = Environment(
        loader=PackageLoader("html_generator"), autoescape=select_autoescape()
    )
    template = env1.get_template("category.html")

    pro_section = ""
    for _index, row in category_data.iterrows():
        pro_section = pro_section + product_section(row)
    return template.render(CategoryName=key, item=pro_section)


env = Environment(
    loader=PackageLoader("html_generator"), autoescape=select_autoescape()
)
template = env.get_template("index.html")

df = pd.read_csv("product.csv")

grouped_df = df.groupby("category")


with open("advanced.html", "w") as html_file:
    middle = ""
    for key, _item in grouped_df:
        category_data = grouped_df.get_group(key)
        middle = middle + category_section(key, category_data)

    html_file.write(template.render(category=middle))
    html_file.close()
