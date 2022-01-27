import pandas as pd


def product_section(row):
    product_top = """
    <div class="layout-inline row">
          <div class="col-sm col-pro layout-inline">
             <p>
    """
    product_name = row["name"]
    before_price = """
    </p>
          </div>
          <div class="col-sm col-price col-numeric align-center " id="price">
            <p>
    """

    unit_price = row["unit_price"]

    before_currency = """
    </p>
          </div>
    <div class="col-sm col-vat align-center">
      <p>
      """

    currency = row["currency"]

    before_code = """
          </p>
          </div>
          <div class="col-sm col-qty layout-inline" id=" """

    code = row["short_code"]

    product_bottum = """">
            <a href="#" class="qty qty-minus">-</a>
              <input type="numeric" value="0" />
            <a href="#" class="qty qty-plus">+</a>
          </div>
          <div class="col-sm col-total col-numeric align-center id="pro-total">
          <p> 0.00</p>
          </div>
     </div>
    """

    return (
        product_top
        + product_name
        + before_price
        + str(unit_price)
        + before_currency
        + currency
        + before_code
        + code
        + product_bottum
    )


def category_section(key, category_data):
    category_top = """
    <div class="layout-inline row cat">
    <div class="col-sm col-pro layout-inline">
    <p>
    """
    category_bottom = """
    </P>
    </div>
    </div>
    """
    pro_section = """"""
    for _index, row in category_data.iterrows():
        pro_section = pro_section + product_section(row)
    return category_top + key + category_bottom + pro_section


df = pd.read_csv("product.csv")

grouped_df = df.groupby("category")


html_file = open("advanced.html", "w")

top = """
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <link rel="stylesheet" href="style.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  </head>
  <body>
    <div class=" container-md">
      <div class="cart transition is-open">
        <a href="#" class="btn btn-update">Buy</a>
        <div class="table">
      <!-- product header -->
        <div class="layout-inline row th">
          <div class="col-sm col-pro">Product</div>
          <div class="col-sm col-price align-center ">
          Price
          </div>
          <div class="col-sm align-center align-center">Currency</div>
          <div class="col-sm col-qty align-center">QTY</div>
          <div class="col-sm align-center">Total</div>
        </div>
      <!-- product start in -->
      """


middle = """"""

for key, _item in grouped_df:

    category_data = grouped_df.get_group(key)

    middle = middle + category_section(key, category_data)


bottum = """
     <!-- product ends in here -->
       <div class="tf">
          <div class="row layout-inline ">
           <div class="col-sm align-center">
             <p>Total</p>
           </div>
           <div class="col-sm col-numeric align-center">
           <p id="over-all">0.00</p>
          </div>
         </div>
       </div>
       </div>
    <a href="#" class="btn btn-update">Buy</a>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
    <script src="script.js"></script>
  </body>
</html>

"""
message = top + middle + bottum
html_file.write(message)
html_file.close()
