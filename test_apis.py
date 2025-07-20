#!/usr/bin/env python3
"""
Test script to demonstrate all APIs working
Run this after starting the FastAPI server
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_products():
    """Test creating products"""
    print("📦 Testing Product Creation...")
    
    # Create first product
    product1 = {
        "name": "Premium T-Shirt",
        "price": 29.99,
        "sizes": [
            {"size": "S", "quantity": 10},
            {"size": "M", "quantity": 15},
            {"size": "L", "quantity": 8},
            {"size": "XL", "quantity": 5}
        ]
    }
    
    response1 = requests.post(f"{BASE_URL}/products", json=product1)
    print(f"Product 1 - Status: {response1.status_code}")
    product1_data = response1.json()
    print(f"Product 1 - Response: {product1_data}")
    
    # Create second product
    product2 = {
        "name": "Blue Jeans",
        "price": 79.99,
        "sizes": [
            {"size": "28", "quantity": 12},
            {"size": "30", "quantity": 18},
            {"size": "32", "quantity": 14},
            {"size": "34", "quantity": 9}
        ]
    }
    
    response2 = requests.post(f"{BASE_URL}/products", json=product2)
    print(f"Product 2 - Status: {response2.status_code}")
    product2_data = response2.json()
    print(f"Product 2 - Response: {product2_data}")
    print()
    
    return product1_data.get("id"), product2_data.get("id")

def test_list_products():
    """Test listing products with different filters"""
    print("📋 Testing Product Listing...")
    
    # List all products
    response = requests.get(f"{BASE_URL}/products")
    print(f"All Products - Status: {response.status_code}")
    data = response.json()
    print(f"Total products: {len(data['data'])}")
    print(f"Page info: {data['page']}")
    
    # Filter by name
    response = requests.get(f"{BASE_URL}/products?name=shirt")
    print(f"Filter by 'shirt' - Status: {response.status_code}")
    data = response.json()
    print(f"Filtered products: {len(data['data'])}")
    
    # Filter by size
    response = requests.get(f"{BASE_URL}/products?size=L")
    print(f"Filter by size 'L' - Status: {response.status_code}")
    data = response.json()
    print(f"Products with size L: {len(data['data'])}")
    
    # Test pagination
    response = requests.get(f"{BASE_URL}/products?limit=1&offset=0")
    print(f"Pagination (limit=1) - Status: {response.status_code}")
    data = response.json()
    print(f"Paginated products: {len(data['data'])}")
    print()

def test_create_orders(product_id1, product_id2):
    """Test creating orders"""
    print("🛒 Testing Order Creation...")
    
    if not product_id1 or not product_id2:
        print("Cannot create orders without product IDs")
        return []
    
    # Create first order
    order1 = {
        "userId": "user_123",
        "items": [
            {"productId": product_id1, "qty": 2},
            {"productId": product_id2, "qty": 1}
        ]
    }
    
    response1 = requests.post(f"{BASE_URL}/orders", json=order1)
    print(f"Order 1 - Status: {response1.status_code}")
    order1_data = response1.json()
    print(f"Order 1 - Response: {order1_data}")
    
    # Create second order
    order2 = {
        "userId": "user_456",
        "items": [
            {"productId": product_id1, "qty": 3}
        ]
    }
    
    response2 = requests.post(f"{BASE_URL}/orders", json=order2)
    print(f"Order 2 - Status: {response2.status_code}")
    order2_data = response2.json()
    print(f"Order 2 - Response: {order2_data}")
    
    # Create another order for user_123
    order3 = {
        "userId": "user_123",
        "items": [
            {"productId": product_id2, "qty": 2}
        ]
    }
    
    response3 = requests.post(f"{BASE_URL}/orders", json=order3)
    print(f"Order 3 - Status: {response3.status_code}")
    order3_data = response3.json()
    print(f"Order 3 - Response: {order3_data}")
    print()
    
    return [order1_data.get("id"), order2_data.get("id"), order3_data.get("id")]

def test_get_orders():
    """Test getting user orders"""
    print("📊 Testing Order Retrieval...")
    
    # Get orders for user_123
    response = requests.get(f"{BASE_URL}/orders/user_123")
    print(f"User 123 Orders - Status: {response.status_code}")
    data = response.json()
    print(f"User 123 has {len(data['data'])} orders")
    print(f"Page info: {data['page']}")
    
    # Get orders for user_456
    response = requests.get(f"{BASE_URL}/orders/user_456")
    print(f"User 456 Orders - Status: {response.status_code}")
    data = response.json()
    print(f"User 456 has {len(data['data'])} orders")
    
    # Test pagination
    response = requests.get(f"{BASE_URL}/orders/user_123?limit=1&offset=0")
    print(f"User 123 Orders (paginated) - Status: {response.status_code}")
    data = response.json()
    print(f"Paginated orders: {len(data['data'])}")
    print()

def test_error_cases():
    """Test error handling"""
    print("❌ Testing Error Cases...")
    
    # Try to create order with invalid product ID
    invalid_order = {
        "userId": "user_test",
        "items": [
            {"productId": "invalid_product_id", "qty": 1}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/orders", json=invalid_order)
    print(f"Invalid Product Order - Status: {response.status_code}")
    print(f"Error Response: {response.json()}")
    
    # Try to create product with invalid data
    invalid_product = {
        "name": "",
        "price": -10,
        "sizes": []
    }
    
    response = requests.post(f"{BASE_URL}/products", json=invalid_product)
    print(f"Invalid Product - Status: {response.status_code}")
    print(f"Error Response: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("🚀 Starting FastAPI Ecommerce Backend Tests")
    print("=" * 50)
    
    try:
        # Test health check
        test_health_check()
        
        # Test product creation
        product_id1, product_id2 = test_create_products()
        
        # Test product listing
        test_list_products()
        
        # Test order creation
        order_ids = test_create_orders(product_id1, product_id2)
        
        # Test order retrieval
        test_get_orders()
        
        # Test error cases
        test_error_cases()
        
        print("✅ All tests completed successfully!")
        print("\n🎉 Your FastAPI Ecommerce Backend is working perfectly!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main()