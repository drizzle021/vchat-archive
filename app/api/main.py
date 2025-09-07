from fastapi import FastAPI
from app.api.router import router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
