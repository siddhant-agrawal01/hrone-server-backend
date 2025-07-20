from fastapi import APIRouter, HTTPException, Query, Path, status
from typing import Optional
from app.schemas.schemas import (
    OrderCreateSchema,
    OrderListResponseSchema,
    OrderResponseSchema
)
from app.services.order_service import OrderService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreateSchema):
    """Create a new order"""
    try:
        order_id = await OrderService.create_order(order)
        return {"id": order_id}
    except ValueError as e:
        logger.error(f"Validation error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )

@router.get("/{user_id}", response_model=OrderListResponseSchema)
async def get_user_orders(
    user_id: str = Path(..., description="User ID to get orders for"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip")
):
    """Get orders for a specific user with pagination"""
    try:
        result = await OrderService.get_user_orders(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        return result
    except Exception as e:
        logger.error(f"Error getting user orders: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve orders"
        )