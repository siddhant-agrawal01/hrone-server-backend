from pydantic import BaseModel, Field
from typing import List, Optional
import bson

class SizeSchema(BaseModel):
    size: str
    quantity: int = Field(ge=0)

class ProductCreateSchema(BaseModel):
    name: str
    price: float = Field(gt=0)
    sizes: List[SizeSchema]

class ProductResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    name: str
    price: float
    sizes: List[SizeSchema] = []

    class Config:
        populate_by_name = True
        json_encoders = {bson.ObjectId: str}

class ProductListResponseSchema(BaseModel):
    data: List[ProductResponseSchema]
    page: dict

class OrderItemSchema(BaseModel):
    productId: str
    qty: int = Field(gt=0)

class OrderCreateSchema(BaseModel):
    userId: str
    items: List[OrderItemSchema]

class ProductDetailsSchema(BaseModel):
    name: str
    id: str

class OrderItemResponseSchema(BaseModel):
    productDetails: ProductDetailsSchema
    qty: int

class OrderResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    items: List[OrderItemResponseSchema]
    total: float

    class Config:
        populate_by_name = True
        json_encoders = {bson.ObjectId: str}

class OrderListResponseSchema(BaseModel):
    data: List[OrderResponseSchema]
    page: dict