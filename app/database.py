# Import necessary SQLAlchemy components
import time
import psycopg2
from sqlalchemy import create_engine  # Core SQLAlchemy engine factory
from sqlalchemy.ext.declarative import declarative_base  # Base class for declarative models
from sqlalchemy.orm import sessionmaker  # Factory for creating database sessions
from psycopg2.extras import RealDictCursor  
from .config import settings


# Database URL format: postgresql://username:password@host/database_name
# Note: %40 is the URL-encoded form of @ in the password
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Create the SQLAlchemy engine
# The engine is the starting point for any SQLAlchemy application
# It maintains the pool of database connections and handles the dialect (PostgreSQL in this case)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class
# This is a factory that will create new database sessions
# Parameters:
#   - autocommit=False: Changes won't be automatically committed to database
#   - autoflush=False: Changes won't be automatically flushed to database
#   - bind=engine: Associates this session factory with our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
# This is the base class from which all your model classes will inherit
# It keeps track of all your models and their metadata
Base = declarative_base()

# Database dependency function for FastAPI
def get_db():
    """
    Creates a database session and handles cleanup.
    This is a dependency that will be used in FastAPI route functions.
    
    Yields:
        Session: A SQLAlchemy database session
    
    Usage:
        @app.get("/")
        def read_items(db: Session = Depends(get_db)):
            ...
    
    The function:
    1. Creates a new database session
    2. Yields it to be used in your route
    3. Ensures the session is closed after the route is done
    Even if an error occurs, the finally block ensures cleanup
    """
    # Create new database session
    db = SessionLocal()
    try:
        # Yield the session to be used in the route
        yield db
    finally:
        # Ensure the session is closed after the route is done
        # This is crucial for proper resource cleanup
        db.close()


#while True:
#    try:
#        # Attempt to establish database connection with retry logic
#        conn = psycopg2.connect(
#            host='localhost',          # Database server location
#            database='FASTAPI',        # Name of the database
#            user='postgres',           # Database user
#            password='Rein@214051',    # Database password (should be in environment variables in production)
#            cursor_factory=RealDictCursor  # Makes query results return as dictionaries
#        )
#        cursor = conn.cursor()
#        print('Database successfully connected')
#        break  # Exit loop if connection successful
#    except Exception as error:
#        print('Failed to connect to database')
#        print("Error ", error)
#        time.sleep(2)  # Wait 2 seconds before retrying connection