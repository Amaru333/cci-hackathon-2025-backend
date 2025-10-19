"""
Database connection and configuration module.
Provides centralized MongoDB connection management for the application.
"""

import os
import logging
from typing import Optional
from contextlib import asynccontextmanager
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Centralized database connection manager."""
    
    def __init__(self):
        self._client: Optional[MongoClient] = None
        self._db: Optional[Database] = None
        self._mongodb_uri: Optional[str] = None
        
    def get_mongodb_uri(self) -> str:
        """Get MongoDB URI from environment variables."""
        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise RuntimeError("MONGODB_URI environment variable is required")
        return uri
    
    def create_client(self) -> MongoClient:
        """Create MongoDB client with proper configuration."""
        uri = self.get_mongodb_uri()
        
        # Connection options for production
        client_options = {
            "maxPoolSize": int(os.getenv("MONGODB_MAX_POOL_SIZE", "50")),
            "minPoolSize": int(os.getenv("MONGODB_MIN_POOL_SIZE", "10")),
            "maxIdleTimeMS": int(os.getenv("MONGODB_MAX_IDLE_TIME_MS", "30000")),
            "serverSelectionTimeoutMS": int(os.getenv("MONGODB_SERVER_SELECTION_TIMEOUT_MS", "5000")),
            "socketTimeoutMS": int(os.getenv("MONGODB_SOCKET_TIMEOUT_MS", "20000")),
            "connectTimeoutMS": int(os.getenv("MONGODB_CONNECT_TIMEOUT_MS", "10000")),
            "retryWrites": True,
            "retryReads": True,
        }
        
        # TLS configuration
        if os.getenv("MONGODB_TLS", "true").lower() == "true":
            client_options["tls"] = True
            # Only allow invalid certificates in development
            if os.getenv("ENVIRONMENT", "development") == "development":
                client_options["tlsAllowInvalidCertificates"] = True
                logger.warning("⚠️  TLS certificate validation disabled for development")
        
        try:
            client = MongoClient(uri, **client_options)
            logger.info("✅ MongoDB client created successfully")
            return client
        except Exception as e:
            logger.error(f"❌ Failed to create MongoDB client: {e}")
            raise
    
    def connect(self) -> None:
        """Establish database connection."""
        try:
            self._mongodb_uri = self.get_mongodb_uri()
            self._client = self.create_client()
            
            # Test connection
            self._client.admin.command('ping')
            logger.info("✅ MongoDB connection established successfully")
            
            # Get database
            db_name = os.getenv("MONGODB_DATABASE_NAME", "cci_hackathon")
            self._db = self._client[db_name]
            logger.info(f"✅ Connected to database: {db_name}")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected database error: {e}")
            raise
    
    def disconnect(self) -> None:
        """Close database connection."""
        if self._client:
            try:
                self._client.close()
                logger.info("✅ MongoDB connection closed")
            except Exception as e:
                logger.error(f"❌ Error closing MongoDB connection: {e}")
            finally:
                self._client = None
                self._db = None
    
    @property
    def client(self) -> MongoClient:
        """Get MongoDB client."""
        if self._client is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._client
    
    @property
    def db(self) -> Database:
        """Get database instance."""
        if self._db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._db
    
    def get_collection(self, collection_name: str) -> Collection:
        """Get a collection from the database."""
        return self.db[collection_name]
    
    def health_check(self) -> dict:
        """Check database health."""
        try:
            if self._client is None:
                return {"status": "disconnected", "error": "No client connection"}
            
            # Ping the database
            start_time = time.time()
            self._client.admin.command('ping')
            response_time = (time.time() - start_time) * 1000
            
            # Get server info
            server_info = self._client.server_info()
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "server_version": server_info.get("version", "unknown"),
                "database_name": self.db.name
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }

# Global database manager instance
db_manager = DatabaseManager()

# Convenience functions for backward compatibility
def get_database() -> Database:
    """Get database instance."""
    return db_manager.db

def get_collection(collection_name: str) -> Collection:
    """Get a collection from the database."""
    return db_manager.get_collection(collection_name)

def get_client() -> MongoClient:
    """Get MongoDB client."""
    return db_manager.client

# FastAPI lifespan context manager
@asynccontextmanager
async def database_lifespan(app):
    """Database connection lifespan manager for FastAPI."""
    # Startup
    logger.info("🚀 Starting database connection...")
    db_manager.connect()
    
    yield
    
    # Shutdown
    logger.info("🛑 Closing database connection...")
    db_manager.disconnect()

# Import time for health check
import time
