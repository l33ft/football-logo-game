"""
Football Club Logo Guessing Game - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from core.database import engine, Base
from api import game_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Football Club Logo Game",
    description="A football club logo guessing game with blur mechanics",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(game_router.router, prefix="/api", tags=["game"])

# Root endpoint
@app.get("/")
async def root():
    from fastapi.responses import HTMLResponse
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)