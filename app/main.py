import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from starlette.responses import JSONResponse

from app.models.database import Base, engine
from app.routers import product, weed, orders, customer

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred", "error": str(exc)},
    )

@app.exception_handler(OperationalError)
async def operational_error_handler(request: Request, exc: OperationalError):
    return JSONResponse(
        status_code=500,
        content={"detail": "A database operational error occurred", "error": str(exc)},
    )

app.include_router(product.router, prefix="/api", tags=["product"])
app.include_router(weed.router, prefix="/api", tags=["weed"])
app.include_router(orders.router, prefix="/api", tags=["orders"])
app.include_router(customer.router, prefix="/api", tags=["customer"])
