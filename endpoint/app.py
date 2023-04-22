import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sources.subgraph.enpoint.app import build_app

logging.basicConfig(
    format="[%(asctime)s:%(levelname)s:%(name)s]:%(message)s",
    datefmt="%Y/%m/%d %I:%M:%S",
    level=logging.INFO,
)


app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.mount("/subgraph", build_app())
# app.mount("/api/v2", apiv2)
