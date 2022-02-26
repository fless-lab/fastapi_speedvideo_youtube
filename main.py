#Let's go...
from itertools import product
from typing import Optional
from xxlimited import new
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


#Let's create the first route of out api..The index.
@app.get("/")
def index():
    return {"msg":"Hello ... this is the entry point of our API, the first route."}

#et's run it..That's it..We've created our first endpoint..the index


#Let's create our product model
class Product(BaseModel):
    name:str
    price:float
    description:Optional[str]=None #Let's make this optional
    
#create a new class    
class UpdateProduct(BaseModel):
    name:Optional[str]=None
    price:Optional[float]=None
    description:Optional[str]=None #Let's make this optional

"""
Look at this scenario... we have a cart and we want to add to it our products...
We can ADD products to this cart,
DELETE, UPDATE and LIST(GET) all add products...

That's what we'll implement here...
We'll write route for all those operations....
OK..Let's go...But befor starting, we will create out DB...here, as an exemple, we'l not use a real DB, we'll use an array..
"""


db = [
{
    "name":"eggs",
    "price":9.99,
    "description":"This are eggs"
},
{
    "name":"bottle",
    "price":3.99,
    "description":"This are bottles"
}
    
] #Our products DB.

#Route to liste all our products...
@app.get("/products")
def get_products():
    return db

#Let's add some data to ou db
#OKay cool..Product list endpoint done.

"""
Now we want to get a specific product...
"""
#using it id
@app.get("/products_by_id/{product_id}")
def get_product_by_id(product_id:int):
    #Let's fix this error.
    if(product_id>=len(db)):
        return {"Error":"Product Not Found"}
    return db[product_id]

#Okay ...Fixed...when somebidy try to get a product which not exist id db, we return a not found error

#Let's get a specific project using it name.
@app.get("/products_by_name/{product_name}")
def get_product_by_name(product_name:str):
    for product in db:
        if product["name"] == product_name:
            return product;
    return {"Error":f"Product {product_name} Not Found"}

#Okay..this error was thrown because we have not yet the product model...which will allow us to get it properties.
#Instead or using a dict we are using array ..so 


#NICE.. that is working well

"""
NEXT STEP : Add element to our db.


Let's take a look on the docs..

FastApi provides a doc for ou APIs
"""

#here, we are defining an endpoint for the post method. we wanna add product ro out db.. so 

@app.post("/add_product")
def add_product(product:Product):
    db.append(product)#we append it to our db...
    return product


"""
OK DONE.Let's go to the next Step : UPDATE
"""

@app.put("/update_product")
def update_product(newProduct:Product,oldProductId:int):
    oldProduct = db[oldProductId]
    #To update all the product, we have to to some thing like ...
    db[oldProductId]=newProduct
    return newProduct


#With that we've update the product at index 1 (2nd product).

"""
But with this, we cannot modify only some properties. to be able to do that, let go this way.
"""

@app.put("/update_some_properties")
#instead of give it the type Product, we'll create a new type. Because in the Product Class , only description is optionnal but here we want something 
#with which we can modify every thing we want.
def update_sp(newProduct:UpdateProduct,oldProductId:int):
    if(oldProductId>=len(db)):
        return {"Error":"Product Not Found"}
    #We can modify all we want now.
    oldProduct = db[oldProductId]
    if newProduct.name!=None:
        oldProduct["name"]=newProduct.name
    if newProduct.price!=None:
        oldProduct["price"]=newProduct.price
    if newProduct.description!=None:
        oldProduct["description"]=newProduct.description
        
    """
    Error explanation:
    
    the newProduct type is dict ... so we have to get it properties by using data.property...
    """    

    return newProduct


"""
The last Operation is the delete one.
"""

@app.delete("/products/")
#we will get the id of the product to delete
def delete_product(id:int=Query(...,description="The id of the product to delete...")):
    if id>=len(db):
        return {"Error":"Product not found"}
    del db[id]#delete the product.
    return {"msg":"Product deleted successfully"}



