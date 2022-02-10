import os

import click
import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape


def product_section(index, row):
    env1 = Environment(
        loader=PackageLoader("html_generator"), autoescape=select_autoescape()
    )
    template = env1.get_template("item.html")
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
    img = row["URL / image"]

    return template.render(
        row1=row1,
        row2=row2,
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
    for index, row in category_data.iterrows():
        pro_section = pro_section + product_section(index, row)
    return template.render(CategoryName=key, item=pro_section)


@click.option(
    "--csv_file",
    default="product.csv",
    help="The csv file from where the html file will be generated defult is product.csv",
)
@click.option(
    "--html_file",
    default="advanced.html",
    help="The name of html that will be generated defult is advanced.html",
)
@click.option(
    "--categories",
    default=False,
    help="if True with category row and if False with out category row defult is False",
)
@click.command()
def generate(csv_file, html_file, categories):
    if os.path.isfile("./" + csv_file):
        env = Environment(
            loader=PackageLoader("html_generator"), autoescape=select_autoescape()
        )
        template = env.get_template("index.html")
        df = pd.read_csv(csv_file)
        grouped_df = df.groupby("category")
        with open(html_file, "w") as htmls_file:
            middle = ""
            if categories:
                for key, _item in grouped_df:
                    category_data = grouped_df.get_group(key)
                    middle = middle + category_section(key, category_data)
            else:
                for key, item in df.iterrows():
                    middle = middle + product_section(key, item)
            htmls_file.write(template.render(category=middle))
            htmls_file.close()
        click.echo("Hello World!")
    else:
        click.echo("the csv file " + csv_file + " doest not exist")


if __name__ == "__main__":
    generate()
