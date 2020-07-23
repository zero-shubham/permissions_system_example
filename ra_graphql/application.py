from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import databases
import sqlalchemy
import os
from permissions_system.PermissionsSystem import PermissionsS

load_dotenv(verbose=True)
app = FastAPI(title="Cloud9 Backend Staging")

DB_URI = os.environ["DB_URI"]

database = databases.Database(DB_URI, min_size=1, max_size=6)
metadata = sqlalchemy.MetaData()
ps = PermissionsS(
    metadata,
    DB_URI
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Encoding",
        "Authorization",
        "Content-Type",
        "Origin",
        "User-Agent"
    ]
)
