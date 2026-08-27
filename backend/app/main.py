from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text 
from app.routes.expense import router as expense_router
from app.db.database import engine, create_tables
from app.routes.auth import router as auth_router
from app.routes.group import router as group_router
from app.routes.settlement import router as settlement_router
from fastapi.middleware.cors import CORSMiddleware
import os


@asynccontextmanager
async def lifespan(app: FastAPI): 
    create_tables()    
    print("Database tables created")
    yield
    # shutdown: cleanup 
    print("Shutting down the app")
    
app = FastAPI(
    title="BillSplice API",
    version="1.0.0", 
    lifespan=lifespan
)

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(CORSMiddleware,
    allow_origins=[
        frontend_url
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


#Supabase DB Test
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
        
        
