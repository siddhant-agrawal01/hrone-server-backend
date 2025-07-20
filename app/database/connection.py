import os
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def get_database():
    return db.database

async def connect_to_mongo():
    """Create database connection using Motor only with extended timeouts"""
    try:
        MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        DATABASE_NAME = os.getenv("DATABASE_NAME", "ecommerce_db")
        
        logger.info("Connecting to MongoDB...")
        
        # Extended connection settings for Vercel deployment
        db.client = AsyncIOMotorClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=30000,  # 30 seconds
            connectTimeoutMS=30000,          # 30 seconds
            socketTimeoutMS=30000,           # 30 seconds
            maxPoolSize=10,                  # Maximum connection pool size
            # minPoolSize=1,                   # Minimum connection pool size
            maxIdleTimeMS=45000,            # 45 seconds
            # waitQueueTimeoutMS=10000,       # 10 seconds
            # retryWrites=True,               # Enable retry writes
            # retryReads=True,                # Enable retry reads
            heartbeatFrequencyMS=10000,     # 10 seconds heartbeat
        )
        
        db.database = db.client[DATABASE_NAME]
        
        # Test the connection with extended timeout
        await db.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB!")
        
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
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
    return database[collection_name]