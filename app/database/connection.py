import os
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import asyncio

logger = logging.getLogger(__name__)

# Remove global database instance for serverless compatibility
_client_cache = {}

async def get_database():
    """Get database connection, creating a new one if needed for serverless compatibility"""
    try:
        # Get current event loop ID to ensure we use the right client
        loop_id = id(asyncio.get_running_loop())
        
        # Check if we have a client for this event loop
        if loop_id not in _client_cache or _client_cache[loop_id] is None:
            await _create_connection_for_loop(loop_id)
        
        return _client_cache[loop_id]['database']
    except Exception as e:
        logger.error(f"Failed to get database: {e}")
        raise RuntimeError("Database connection not established")

async def _create_connection_for_loop(loop_id):
    """Create a new connection for the current event loop"""
    try:
        MONGODB_URL = os.getenv("MONGODB_URL")
        DATABASE_NAME = os.getenv("DATABASE_NAME", "ecommerce_db")
        
        logger.info(f"Creating new MongoDB connection for loop {loop_id}")
        
        # Create new client with serverless-optimized configuration
        client = AsyncIOMotorClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,          
            socketTimeoutMS=5000,           
            maxPoolSize=1,  # Single connection for serverless
            minPoolSize=0,
            maxIdleTimeMS=10000,
        )
        
        # Test the connection
        await client.admin.command('ping')
        
        database = client[DATABASE_NAME]
        
        # Store in cache for this event loop
        _client_cache[loop_id] = {
            'client': client,
            'database': database
        }
        
        logger.info(f"Successfully connected to MongoDB database: {DATABASE_NAME}")
        
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        _client_cache[loop_id] = None
        raise

async def connect_to_mongo():
    """Create database connection - simplified for serverless"""
    loop_id = id(asyncio.get_running_loop())
    await _create_connection_for_loop(loop_id)

async def close_mongo_connection():
    """Close database connections for all event loops"""
    try:
        for loop_id, connection_info in _client_cache.items():
            if connection_info and connection_info['client']:
                connection_info['client'].close()
        _client_cache.clear()
        logger.info("Disconnected from MongoDB")
    except Exception as e:
        logger.error(f"Error disconnecting from MongoDB: {e}")

async def get_collection(collection_name: str):
    """Get a collection from the database"""
    database = await get_database()
    if database is None:
        raise RuntimeError("Database connection not available")
    return database[collection_name]