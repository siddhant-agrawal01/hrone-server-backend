import os
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import asyncio

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def get_database():
    if db.database is None:
        logger.warning("Database not connected. Attempting to connect...")
        try:
            await connect_to_mongo()
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise RuntimeError("Database connection not established")
    return db.database

async def connect_to_mongo():
    """Create database connection using Motor only with extended timeouts"""
    if db.database is not None:
        logger.info("Database already connected")
        return
        
    try:
        MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        DATABASE_NAME = os.getenv("DATABASE_NAME", "ecommerce_db")
        
        logger.info(f"Connecting to MongoDB at {MONGODB_URL}...")
        
        # Extended connection settings for Vercel deployment
        db.client = AsyncIOMotorClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=30000,  # 30 seconds
            connectTimeoutMS=30000,          # 30 seconds
            socketTimeoutMS=30000,           # 30 seconds
            maxPoolSize=10,                  # Maximum connection pool size
            maxIdleTimeMS=45000,            # 45 seconds
            heartbeatFrequencyMS=10000,     # 10 seconds heartbeat
        )
        
        # Test the connection with extended timeout
        await asyncio.wait_for(db.client.admin.command('ping'), timeout=30.0)
        
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