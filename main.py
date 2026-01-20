"""Main API"""

from fastapi import FastAPI
from app.routes.auth import auth_router
from app.routes.user import user_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Resto API", version="1.0.0")
app.include_router(auth_router.router)
app.include_router(user_router.router)

"""Allow CORS for all origins"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Resto API!"}