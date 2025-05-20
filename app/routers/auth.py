from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import validate_email
from sqlalchemy.orm import Session

from app import models
from app.routers import oauth2
from app.schemas import customer as schemas
from app.utils.database import get_db
from app.utils.password import verify_password, password_hash

router = APIRouter()


@router.post("/register", response_model=schemas.Customer)
def customer_register(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    # Check for existing email
    existing = (
        db.query(models.Customer)
        .filter(models.Customer.email == customer.email)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = password_hash(customer.password)
    customer.password = hashed_password
    new_customer = models.Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@router.post("/login")
def customer_login(
    user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    try:
        validate_email(user_cred.username)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid email format")

    customer = (
        db.query(models.Customer)
        .filter(models.Customer.email == user_cred.username)
        .first()
    )
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    if not verify_password(user_cred.password, customer.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"customer_id": customer.c_id})
    return {"access_token": access_token, "token_type": "bearer"}
