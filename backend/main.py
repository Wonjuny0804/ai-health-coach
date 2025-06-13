from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.onboarding import router as onboarding_router

app = FastAPI(
    title="AI Health Coach API",
    description="API for the AI Health Coach application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(onboarding_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "result": "AI Health Coach API",
        "status": "active",
        "version": "1.0.0"
    }
