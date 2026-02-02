"""Main API"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.auth import auth_router
from app.routes.menu import menu_routes
from app.routes.user import user_router
from app.routes.meja import meja_routes
from app.routes.kategori_menu import kategori_menu_routes
from app.routes.transaksi import transaksi_routes
from app.routes.updateStokHarian import updateStokHarian_routes
from typing import List
from app.routes.karyawan import karyawan_routes
from app.routes.pesanan import pesanan_routes
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path


app = FastAPI(title="Resto API", version="1.0.0")
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(meja_routes.router)
app.include_router(menu_routes.router)
app.include_router(kategori_menu_routes.router)
app.include_router(transaksi_routes.router)
app.include_router(updateStokHarian_routes.router)
app.include_router(karyawan_routes.router)
app.include_router(pesanan_routes.router)

# Create uploads directory if it doesn't exist
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

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