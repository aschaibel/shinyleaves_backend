from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401
from app.routers import product, order, customer, auth
from app.utils.database import Base, engine


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


app.include_router(order.router, prefix="/api", tags=["order"])
app.include_router(customer.router, prefix="/api", tags=["customer"])
app.include_router(product.router, prefix="/api", tags=["product"])
app.include_router(auth.router, prefix="/api", tags=["authentication"])
