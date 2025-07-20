import bson
from typing import List, Optional, Dict, Any
from app.database.connection import get_collection
from app.schemas.schemas import OrderCreateSchema, OrderItemSchema
from app.services.product_service import ProductService
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class OrderService:
    
    @staticmethod
    async def create_order(order_data: OrderCreateSchema) -> Dict[str, Any]:
        """Create a new order and return full order details"""
        try:
            collection = await get_collection("orders")
            
            total_amount = 0.0
            validated_items = []
            
            for item in order_data.items:
                product = await ProductService.get_product_by_id(item.productId)
                if not product:
                    raise ValueError(f"Product with ID {item.productId} not found")
                
                item_total = product["price"] * item.qty
                total_amount += item_total
                
                validated_items.append({
                    "productId": item.productId,
                    "qty": item.qty,
                    "price": product["price"],
                    "name": product["name"]
                })
            
            order_dict = {
                "userId": order_data.userId,
                "items": validated_items,
                "totalAmount": total_amount,
                "createdAt": datetime.utcnow(),
                "status": "created"
            }
            
            result = await collection.insert_one(order_dict)
            
            created_order = await collection.find_one({"_id": result.inserted_id})
            
            formatted_items = []
            for item in created_order["items"]:
                formatted_items.append({
                    "productDetails": {
                        "name": item["name"],
                        "id": item["productId"]
                    },
                    "qty": item["qty"]
                })
            
            return {
                "id": str(created_order["_id"]),
                "userId": created_order["userId"],
                "items": formatted_items,
                "totalAmount": created_order["totalAmount"],
                "createdAt": created_order["createdAt"]
            }
            
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise
    
    @staticmethod
    async def get_user_orders(
        user_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get orders for a specific user with pagination"""
        try:
            collection = await get_collection("orders")
            
            filter_query = {"userId": user_id}
            
            total_count = await collection.count_documents(filter_query)
            
            cursor = collection.find(filter_query).skip(offset).limit(limit).sort("_id", -1)
            orders = await cursor.to_list(length=limit)
            
            formatted_orders = []
            for order in orders:
                formatted_items = []
                for item in order["items"]:
                    formatted_items.append({
                        "productDetails": {
                            "name": item["name"],
                            "id": item["productId"]
                        },
                        "qty": item["qty"]
                    })
                
                formatted_orders.append({
                    "_id": str(order["_id"]),
                    "items": formatted_items,
                    "total": order.get("totalAmount", order.get("total", 0))
                })
            
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
                "data": formatted_orders,
                "page": page_info
            }
            
        except Exception as e:
            logger.error(f"Error getting user orders: {e}")
            raise