import os
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import asyncio

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database = None
    _lock = None

    def __init__(self):
        self._lock = asyncio.Lock()

db = Database()

async def get_database():
    if db.database is None:
        async with db._lock:
            if db.database is None:  # Double-check locking
                logger.warning("Database not connected. Attempting to connect...")
                try:
                    await connect_to_mongo()
                except Exception as e:
                    logger.error(f"Failed to connect to database: {e}")
                    raise RuntimeError("Database connection not established")
    return db.database

async def connect_to_mongo():
    """Create database connection using Motor only with extended timeouts"""
    try:
        # Reset any existing connection
        if db.client:
            db.client.close()
            db.client = None
            db.database = None
        
        MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        DATABASE_NAME = os.getenv("DATABASE_NAME", "ecommerce_db")
        
        logger.info(f"Connecting to MongoDB at {MONGODB_URL}...")
        
        # Create new client with current event loop
        db.client = AsyncIOMotorClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=10000,  # Reduced timeout for faster feedback
            connectTimeoutMS=10000,          
            socketTimeoutMS=10000,           
            maxPoolSize=5,                   # Reduced pool size
            maxIdleTimeMS=30000,            
            heartbeatFrequencyMS=10000,     
        )
        
        # Test the connection with shorter timeout
        await asyncio.wait_for(db.client.admin.command('ping'), timeout=10.0)
        
        db.database = db.client[DATABASE_NAME]
        logger.info(f"Successfully connected to MongoDB database: {DATABASE_NAME}")
        
    except asyncio.TimeoutError:
        logger.error("MongoDB connection timed out")
        db.client = None
        db.database = None
        raise
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        db.client = None
        db.database = None
        raise

async def close_mongo_connection():
    """Close database connection"""
    try:
        if db.client:
            db.client.close()
            logger.info("Disconnected from MongoDB")
    except Exception as e:
        logger.error(f"Error disconnecting from MongoDB: {e}")

async def get_collection(collection_name: str):
    """Get a collection from the database"""
    database = await get_database()
    if database is None:
        raise RuntimeError("Database connection not available")
    return database[collection_name]