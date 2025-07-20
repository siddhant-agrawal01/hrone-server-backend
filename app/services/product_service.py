import bson
from typing import List, Optional, Dict, Any
from app.database.connection import get_collection
from app.schemas.schemas import ProductCreateSchema, ProductResponseSchema
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ProductService:
    
    @staticmethod
    async def create_product(product_data: ProductCreateSchema) -> Dict[str, Any]:
        """Create a new product and return full product details"""
        try:
            collection = await get_collection("products")
            
            product_dict = product_data.dict()
            product_dict["createdAt"] = datetime.utcnow()
            
            result = await collection.insert_one(product_dict)
            
            created_product = await collection.find_one({"_id": result.inserted_id})
            
            created_product["id"] = str(created_product["_id"])
            del created_product["_id"]
            
            return created_product
            
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            raise
    
    @staticmethod
    async def get_products(
        name: Optional[str] = None,
        size: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get products with filtering and pagination"""
        try:
            collection = await get_collection("products")
            
            filter_query = {}
            
            if name:
                filter_query["name"] = {"$regex": re.escape(name), "$options": "i"}
            
            if size:
                filter_query["sizes.size"] = size
            
            total_count = await collection.count_documents(filter_query)
            
            cursor = collection.find(filter_query).skip(offset).limit(limit).sort("_id", 1)
            products = await cursor.to_list(length=limit)
            
            for product in products:
                product["_id"] = str(product["_id"])
            
            next_page = (offset // limit) + 2 if offset + limit < total_count else None
            previous_page = (offset // limit) if offset > 0 else None
            
            page_info = {
                "next": next_page,
                "previous": previous_page,
                "limit": limit,
                "offset": offset,
                "total": total_count
            }
            
            return {
                "data": products,
                "page": page_info
            }
            
        except Exception as e:
            logger.error(f"Error getting products: {e}")
            raise
    
    @staticmethod
    async def get_product_by_id(product_id: str) -> Optional[dict]:
        """Get a single product by ID"""
        try:
            collection = await get_collection("products")
            
            if not bson.ObjectId.is_valid(product_id):
                return None
                
            product = await collection.find_one({"_id": bson.ObjectId(product_id)})
            
            if product:
                product["_id"] = str(product["_id"])
            
            return product
            
        except Exception as e:
            logger.error(f"Error getting product by ID: {e}")
            raise