from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.weather.router import router as weather_router
from backend.risk.router import router as alert_router
from backend.app.auth.router import router as auth_router


app = FastAPI(
    title="AgriGuard API",
    description="API for the project",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(weather_router)
app.include_router(alert_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"status": "online", "message": "AgriGuard Backend Active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)