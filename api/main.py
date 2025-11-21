from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import words 
from app.routers import validation 

app = FastAPI(
    title="Vocabulary Practice API",
    version="1.0.0",
    description="API for vocabulary practice and learning"
)

# เปิด CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(words.router, prefix="/api", tags=["words"])
app.include_router(validation.router, prefix="/api", tags=["validation"])

@app.get("/")
def read_root():
    return {"message": "Vocabulary Practice API Ready!"}