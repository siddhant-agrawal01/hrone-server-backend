from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from app.schemas.schemas import (
    ProductCreateSchema, 
    ProductListResponseSchema, 
    ProductResponseSchema
)
from app.services.product_service import ProductService
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreateSchema):
    """Create a new product"""
    try:
        product_data = await ProductService.create_product(product)
        
        if "_id" in product_data:
            product_data["id"] = product_data["_id"]
            del product_data["_id"]
        
        return product_data
    except ValidationError as e:
        logger.error(f"Validation error creating product: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )

@router.get("/", response_model=ProductListResponseSchema)
async def get_products(
    name: Optional[str] = Query(None, description="Filter by product name (partial search)"),
    size: Optional[str] = Query(None, description="Filter by size availability"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip")
):
    """Get products with optional filtering and pagination"""
    try:
        result = await ProductService.get_products(
            name=name,
            size=size,
            limit=limit,
            offset=offset
        )
        return result
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve products"
        )