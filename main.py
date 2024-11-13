from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse

from uuid import uuid4
import schemas  # from the ./models.py
from database import engine, SessionLocal  # from the ./database.py
from datetime import datetime
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

schemas.Base.metadata.create_all(bind=engine)


class App(BaseModel):
    app_status: int

    class Config:
        model_config = {"from_attributes": True}


# class Apps(BaseModel):
#     apps: List[App]


class AppDelete(BaseModel):
    app_id: str


class ResAddress(BaseModel):

    app_id: str
    res_id: str
    province: Optional[str] = None
    postalcode: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    street: Optional[str] = None
    street_num: Optional[int] = None


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


@app.get("/res_addresses/{res_id}")
async def get_addresses(res_id: str, db: Session = Depends(get_db)):
    address = db.query(schemas.ResidentialAddress).filter(schemas.ResidentialAddress.app_id == res_id).first()
    return address


@app.get("/get_personal_info/{pi_id}")
async def get_personal_info(pi_id: str, db: Session = Depends(get_db)):
    address = db.query(schemas.PersonalInfo).filter(schemas.PersonalInfo.app_id == pi_id).first()
    return address


@app.get("/applications")
async def get_applications(db: Session = Depends(get_db)):
    """
    Get ALL applications
    """
    results = db.query(schemas.Application).all()
    return results


@app.post("/create")
async def create_application(application: App, db: Session = Depends(get_db)):
    """
    Create ONE application, NOT SAVE
    """

    application_status = application.app_status
    timestamp_in_seconds = int(datetime.now().timestamp())
    app_id = str(uuid4())

    application_model = schemas.Application()
    application_model.app_id = app_id
    application_model.app_status = application_status
    application_model.change_date = timestamp_in_seconds

    pi_model = schemas.PersonalInfo()  # pi stands for personal information
    pi_model.app_id = app_id
    pi_model.pi_id = app_id

    res_address_model = schemas.ResidentialAddress()
    res_address_model.app_id = app_id
    res_address_model.res_id = app_id

    db.add(application_model)
    db.add(res_address_model)
    db.add(pi_model)
    db.commit()
    db.refresh(application_model)

    return application_model


@app.post("/save")
async def save_application(res_address: ResAddress, db: Session = Depends(get_db)):
    # Get the res_address from the res_address table first
    res_id = res_address.res_id
    target_address = db.query(schemas.ResidentialAddress).filter(schemas.ResidentialAddress.res_id == res_id).first()
    if not target_address:
        raise HTTPException(status_code=404, detail="Address not found")

    if res_address.province is not None:
        target_address.province = res_address.province
    if res_address.postalcode is not None:
        target_address.postalcode = res_address.postalcode
    if res_address.city is not None:
        target_address.city = res_address.city
    if res_address.province is not None:
        target_address.province = res_address.province
    if res_address.street is not None:
        target_address.street = res_address.street
    if res_address.street_num is not None:
        target_address.street_num = res_address.street_num

    db.add(target_address)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={"msg": "SUCCESS, application saved"},
    )


@app.delete("/delete")
async def delete_application(app_delete: AppDelete, db: Session = Depends(get_db)):
    """
    Delete ONE application
    """
    app_id = app_delete.app_id
    application = db.query(schemas.Application).filter(schemas.Application.app_id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(application)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={"msg": "SUCCESS, application deleted"},
    )
