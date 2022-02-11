import csv
import sys
from itertools import groupby

import click
from jinja2 import Environment, PackageLoader, select_autoescape

sys.tracebacklimit = 0


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


def head_check(csvreader):
    headercheck = [
        "Name",
        "category",
        "Unit price",
        "Currency",
        "Short code",
        "Description",
        "URL / image",
    ]
    header = []
    header = next(csvreader)
    if set(headercheck).issubset(set(header)):
        click.echo("header muches the format")
    else:
        raise Exception("header of the csv file does not match the format")
    return header


def csv_body(header, file_csv):
    people_list = []
    headers_list = []

    index = 0
    for line in file_csv:

        if index > 0:
            people_dict = {}
            for idx, elem in enumerate(headers_list):
                people_dict[elem] = line[idx]
            people_list.append(people_dict)
        else:
            headers_list = header
        index += 1
    return people_list


def category_section(key, category_data):
    env1 = Environment(
        loader=PackageLoader("html_generator"), autoescape=select_autoescape()
    )
    template = env1.get_template("category.html")

    pro_section = ""
    index = 0
    for row in category_data:
        pro_section = pro_section + product_section(index, row)
        index += 1
    return template.render(CategoryName=key, item=pro_section)


def key_func(key):
    return key["category"]


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
    click.echo("trying to open " + csv_file)
    try:
        with open(csv_file) as file_csv:
            click.echo(csv_file + " is opened")
            csvreader = csv.reader(file_csv)
            header = head_check(csvreader)
            csv_data = csv_body(header, csvreader)
            env = Environment(
                loader=PackageLoader("html_generator"), autoescape=select_autoescape()
            )
            template = env.get_template("index.html")
            click.echo("cretating " + html_file)
            with open(html_file, "w") as htmls_file:
                middle = ""
                if categories:
                    csv_data = sorted(csv_data, key=key_func)

                    for key, value in groupby(csv_data, key_func):
                        middle = middle + category_section(key, value)
                else:
                    key = 0
                    for value in csv_data:
                        middle = middle + product_section(key, value)
                        key += 1
                htmls_file.write(template.render(category=middle))
                click.echo(html_file + " created")
                htmls_file.close()
    except FileNotFoundError:
        click.echo(csv_file + " not found")
    except Exception as ex:
        click.echo(ex)


if __name__ == "__main__":
    generate()
