from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="Enterprise AI Chatbot API",
    version="0.1.0"
)

# ⭐ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # برای dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"status": "running"}