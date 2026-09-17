from sqlmodel import SQLModel, Session, create_engine 
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    FRONTEND_URL: str = "https://bill-splice.vercel.app"
    ENVIRONMENT: str = "production"
    CLOUDINARY_URL: str = ""
    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings() #Pydantic settings 

engine = create_engine(settings.DATABASE_URL, echo=False)

def create_tables(): 
    """Create all tables defined by SQLModel class"""
    SQLModel.metadata.create_all(engine)

def get_db():
    """Dependency that provides a database session per request"""
    with Session(engine) as session: 
        yield session