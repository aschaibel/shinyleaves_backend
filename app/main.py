from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401
from app.models.database import Base, engine
from app.routers import product, weed, orders, customer


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(weed.router, prefix="/api", tags=["weed"])
app.include_router(orders.router, prefix="/api", tags=["orders"])
app.include_router(customer.router, prefix="/api", tags=["customer"])
app.include_router(product.router, prefix="/api", tags=["product"])
