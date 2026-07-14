from fastapi import FastAPI
from sqlalchemy import text 
from app.api.expense import router as expense_router
from app.db.database import engine
from app.api.auth import router as auth_router
from app.api.group import router as group_router
from app.api.settlement import router as settlement_router

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="BillSplice API",
    version="1.0.0", 
)

app.add_middleware(CORSMiddleware,
    allow_origins=[
        "https://bill-splice.vercel.app"
    ], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],)
app.include_router(group_router)
app.include_router(auth_router)
app.include_router(expense_router)
app.include_router(settlement_router)
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
        
        
