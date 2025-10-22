from pydantic import BaseModel
from typing import Optional


class ProductModel(BaseModel):
    
    category_id:int
    name:str
    quantity:int
    price:float

    class Config:
        from_attributes=True

class CategoryModel(BaseModel):
    id:int
    name:str

class OrderModel(BaseModel):
    id:int
    product_id:int
    user_id:int
    firstname:str
    lastname:str
    address:str

    class Config:
        from_attributes= True

class UserModel(BaseModel):
    id:int
    name:str
    firstname:str
    lastname:str
    email:str

