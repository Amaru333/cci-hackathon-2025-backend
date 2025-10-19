"""
Database initialization script.
Creates indexes and performs initial database setup.
"""

import os
import logging
from database import db_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_indexes():
    """Create database indexes for optimal performance."""
    try:
        db = db_manager.db
        
        # Users collection indexes
        users_collection = db["users"]
        users_collection.create_index("user", unique=True)
        users_collection.create_index("created_at")
        logger.info("✅ Created users collection indexes")
        
        # Ingredients collection indexes
        ingredients_collection = db["ingredients"]
        ingredients_collection.create_index("user")
        ingredients_collection.create_index("name")
        ingredients_collection.create_index([("user", 1), ("name", 1)])
        ingredients_collection.create_index("created_at")
        logger.info("✅ Created ingredients collection indexes")
        
        # All ingredients collection indexes
        all_ingredients_collection = db["all_ingredients"]
        all_ingredients_collection.create_index("name", unique=True)
        all_ingredients_collection.create_index("category")
        all_ingredients_collection.create_index("expiry")
        logger.info("✅ Created all_ingredients collection indexes")
        
        # List all indexes
        logger.info("📊 Users collection indexes:")
        for index in users_collection.list_indexes():
            logger.info(f"  - {index['name']}: {index['key']}")
        
        logger.info("📊 Ingredients collection indexes:")
        for index in ingredients_collection.list_indexes():
            logger.info(f"  - {index['name']}: {index['key']}")
        
        logger.info("📊 All ingredients collection indexes:")
        for index in all_ingredients_collection.list_indexes():
            logger.info(f"  - {index['name']}: {index['key']}")
            
    except Exception as e:
        logger.error(f"❌ Error creating indexes: {e}")
        raise

def check_database_health():
    """Check database health and connection."""
    try:
        health = db_manager.health_check()
        logger.info(f"🏥 Database health: {health}")
        return health["status"] == "healthy"
    except Exception as e:
        logger.error(f"❌ Database health check failed: {e}")
        return False

def main():
    """Main initialization function."""
    logger.info("🚀 Starting database initialization...")
    
    try:
        # Connect to database
        db_manager.connect()
        
        # Check health
        if not check_database_health():
            raise RuntimeError("Database health check failed")
        
        # Create indexes
        create_indexes()
        
        logger.info("✅ Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    finally:
        # Disconnect
        db_manager.disconnect()

if __name__ == "__main__":
    main()
