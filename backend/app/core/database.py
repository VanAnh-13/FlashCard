"""
Database Connection Management
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Global database client
db_client: AsyncIOMotorClient = None


async def connect_to_mongo():
    """Connect to MongoDB"""
    global db_client
    db_client = AsyncIOMotorClient(settings.MONGODB_URL)
    print(f"✅ Connected to MongoDB at {settings.MONGODB_URL}")


async def close_mongo_connection():
    """Close MongoDB connection"""
    global db_client
    if db_client:
        db_client.close()
        print("❌ Closed MongoDB connection")


def get_database():
    """Get database instance"""
    return db_client[settings.DATABASE_NAME]
