from fastapi import FastAPI
from sqlalchemy import text 

from app.db.database import engine
from app.api.auth import router as auth_router

app = FastAPI(
    title="BillSplice API",
    version="1.0.0"
)
app.include_router(auth_router)
@app.get("/")
def root():
    return {"message": "Welcome to BillSplice API"}

@app.get("/db-test")
def test_database():
    try: 
        with engine.connect() as connection: 
            connection.execute(text("SELECT 1"))
            return {
                "status": "success", 
                "message": "Database connected successfully"
            }
    except Exception as e: 
        return {
            "status": "error", 
            "message": str(e)
        }