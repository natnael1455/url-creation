import pandas as pd


def product_section(row):
    product_top = """
    <div class="layout-inline row">
        
          <div class="col col-pro layout-inline">
             <p>
    """
    product_name = row["name"]
    before_price = """
    </p>
          </div>
        
          <div class="col col-price col-numeric align-center ">
            <p>
    """

    unit_price = row["unit_price"]

    before_currency = """
    </p>
          </div>
    <div class="col col-vat">
      <p>
      """

    currency = row["currency"]

    before_code = """
    
          </p>
          </div>
          <div class="col col-qty layout-inline" id=" """

    code = row["short_code"]

    product_bottum = """">
          
            <a href="#" class="qty qty-minus">-</a>
              <input type="numeric" value="0" />
            <a href="#" class="qty qty-plus">+</a>
          </div>
        
          
          <div class="col col-total col-numeric">               
            <p id="total"></p>
          </div>
     </div>
    """
    message = (
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
    return message


def category_section(key, category_data):
    category_top = """
    <div class="layout-inline row cat">
    <div class="col col-pro layout-inline">
    <p>
    """
    category_bottom = """
    </P>
    </div>
    </div>
    """
    pro_section = """"""
    for index, row in category_data.iterrows():
        pro_section = pro_section + product_section(row)

    message = category_top + key + category_bottom + pro_section
    return message


df = pd.read_csv("product.csv")

grouped_df = df.groupby("category")


f = open("advanced.html", "w")

top = """
<html>
  <head>
    <link rel="stylesheet" href="style.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    
  </head>
  <body>
    <div class="container">
      <div class="heading">
        <h1>
          <span class="shopper">s</span> Shopping Cart
        </h1>
    
        <a href="#" class="visibility-cart transition is-open">X</a>    
      </div>
  
      <div class="cart transition is-open">
    
        <a href="#" class="btn btn-update">Update cart</a>
    
    
        <div class="table">
      <!-- product header -->

        <div class="layout-inline row th">
          <div class="col col-pro">Product</div>
          <div class="col col-price align-center "> 
             Price
          </div>
          <div class="col align-center">Currency</div>
          <div class="col col-qty align-center">QTY</div>
          <div class="col">Total</div>
        </div>
      <!-- product start in here -->
      """


middle = """"""

for key, item in grouped_df:

    category_data = grouped_df.get_group(key)

    middle = middle + category_section(key, category_data)


bottum = """
        
      <!-- product ends in here 2-->
      
       <div class="tf">
         <div class="row layout-inline">
           <div class="col">
             <p>VAT</p>
           </div>
           <div class="col"></div>
         </div>
         <div class="row layout-inline">
           <div class="col">
             <p>Shipping</p>
           </div>
           <div class="col"></div>
         </div>
          <div class="row layout-inline">
           <div class="col">
             <p>Total</p>
           </div>
           <div class="col"></div>
         </div>
       </div>         
  </div>
    
    <a href="#" class="btn btn-update">Update cart</a>
  
    </div>
   
    <script src="script.js"></script>
  </body>
</html>

"""
message = top + middle + bottum
f.write(message)
f.close()

