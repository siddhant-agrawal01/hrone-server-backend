from fastapi import APIRouter, HTTPException, Query, Path, status
from typing import Optional
from app.schemas.schemas import (
    OrderCreateSchema,
    OrderListResponseSchema,
    OrderResponseSchema
)
from app.services.order_service import OrderService
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=OrderResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreateSchema):
    """Create a new order"""
    try:
        order_data = await OrderService.create_order(order)
        return order_data
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            logger.error(f"Product not found error creating order: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        else:
            logger.error(f"Validation error creating order: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
    except ValidationError as e:
        logger.error(f"Validation error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
        logger.info(f"Fetching orders for user: {user_id}, limit: {limit}, offset: {offset}")
        
        result = await OrderService.get_user_orders(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        
        logger.info(f"Successfully retrieved {len(result.get('data', []))} orders for user {user_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error getting user orders for user {user_id}: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve orders: {str(e)}"
        )