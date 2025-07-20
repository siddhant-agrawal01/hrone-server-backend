from pydantic import BaseModel, Field, validator
from typing import List, Optional
import bson
from datetime import datetime

class SizeSchema(BaseModel):
    size: str
    quantity: int = Field(ge=0)

class ProductCreateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(gt=0)
    sizes: List[SizeSchema] = Field(..., min_items=1)
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

class ProductResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    name: str
    price: float
    sizes: List[SizeSchema] = []
    createdAt: Optional[datetime] = None

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
        json_encoders = {bson.ObjectId: str}

class ProductListResponseSchema(BaseModel):
    data: List[ProductResponseSchema]
    page: dict

class OrderItemSchema(BaseModel):
    productId: str
    qty: int = Field(gt=0)

class OrderCreateSchema(BaseModel):
    userId: str = Field(..., min_length=1)
    items: List[OrderItemSchema] = Field(..., min_items=1)
    
    @validator('userId')
    def user_id_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('User ID cannot be empty')
        return v.strip()

class ProductDetailsSchema(BaseModel):
    name: str
    id: str

class OrderItemResponseSchema(BaseModel):
    productDetails: ProductDetailsSchema
    qty: int

class OrderResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    userId: str
    items: List[OrderItemResponseSchema]
    totalAmount: float
    createdAt: Optional[datetime] = None
    status: Optional[str] = "created"

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
        json_encoders = {bson.ObjectId: str}

class OrderListResponseSchema(BaseModel):
    data: List[OrderResponseSchema]
    page: dict