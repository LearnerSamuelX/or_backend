from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.responses import JSONResponse

from uuid import uuid4
import schemas  # from the ./models.py
from database import engine, SessionLocal  # from the ./database.py
from datetime import datetime
from sqlalchemy.orm import Session
from validation_models import App, AppInfo, ValidatedAppInfo, AppDelete

app = FastAPI()

schemas.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/res_addresses/{app_id}")
async def get_addresses(app_id: str, db: Session = Depends(get_db)):
    address = db.query(schemas.ResidentialAddress).filter(schemas.ResidentialAddress.app_id == app_id).first()
    return address


@app.get("/get_personal_info/{app_id}")
async def get_personal_info(app_id: str, db: Session = Depends(get_db)):
    address = db.query(schemas.PersonalInfo).filter(schemas.PersonalInfo.app_id == app_id).first()
    return address


@app.get("/applications")
async def get_applications(db: Session = Depends(get_db)):
    """
    Get ALL applications
    """
    results = db.query(schemas.Application).all()
    results.sort(key=lambda x: x.change_date, reverse=True)
    return results


@app.get("/application/{app_id}")
async def get_application(app_id: str, db: Session = Depends(get_db)):
    """
    Get one specific application
    """
    personal_info = db.query(schemas.PersonalInfo).filter(schemas.PersonalInfo.app_id == app_id).first()
    res_address = db.query(schemas.ResidentialAddress).filter(schemas.ResidentialAddress.app_id == app_id).first()

    if not personal_info:
        raise HTTPException(status_code=404, detail=f"Personal information for user  with ID {app_id}  not found")

    if not res_address:
        raise HTTPException(status_code=404, detail="Address not found")

    # combined_data = AppInfo(
    #     first_name=personal_info.first_name,
    #     last_name=personal_info.last_name,
    #     middle_name=personal_info.middle_name,
    #     dl_num=personal_info.dl_num,
    #     dob=personal_info.dob,
    #     gender=personal_info.gender,
    #     height=personal_info.height,
    #     province=res_address.province,
    #     postalcode=res_address.postalcode,
    #     city=res_address.city,
    #     street=res_address.street,
    #     street_num=res_address.street_num,
    # )

    return (personal_info, res_address)


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
async def save_application(app_info: AppInfo, db: Session = Depends(get_db)):
    # Get the res_address from the res_address table first
    app_id = app_info.app_id
    target_app = db.query(schemas.Application).filter(schemas.Application.app_id == app_id).first()
    target_pi = db.query(schemas.PersonalInfo).filter(schemas.PersonalInfo.app_id == app_id).first()
    target_address = db.query(schemas.ResidentialAddress).filter(schemas.ResidentialAddress.app_id == app_id).first()
    if not target_pi:
        raise HTTPException(
            status_code=404, detail=f"Personal information for user  with ID {app_info.app_id}  not found"
        )

    if not target_address:
        raise HTTPException(status_code=404, detail="Address not found")

    # validate personal information
    if app_info.first_name is not None:
        target_pi.first_name = app_info.first_name
    if app_info.last_name is not None:
        target_pi.last_name = app_info.last_name
    if app_info.middle_name is not None:
        target_pi.middle_name = app_info.middle_name
    if app_info.dl_num is not None:
        target_pi.dl_num = app_info.dl_num
    if app_info.dob is not None:
        target_pi.dob = app_info.dob
    if app_info.gender is not None:
        target_pi.gender = app_info.gender
    if app_info.height is not None:
        target_pi.height = app_info.height

    # validate residential information
    if app_info.province is not None:
        target_address.province = app_info.province
    if app_info.postalcode is not None:
        target_address.postalcode = app_info.postalcode
    if app_info.city is not None:
        target_address.city = app_info.city
    if app_info.street is not None:
        target_address.street = app_info.street
    if app_info.street_num is not None:
        target_address.street_num = app_info.street_num

    timestamp_in_seconds = int(datetime.now().timestamp())
    target_app.change_date = timestamp_in_seconds

    db.add(target_app)
    db.add(target_pi)
    db.add(target_address)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={"msg": "SUCCESS, application saved"},
    )


@app.post("/submit")
async def submit_application(app_info: ValidatedAppInfo, db: Session = Depends(get_db)):
    app_id = app_info.app_id

    # change the status of application
    target_app = db.query(schemas.Application).filter(schemas.Application.app_id == app_id).first()
    target_app.app_status = 2
    timestamp_in_seconds = int(datetime.now().timestamp())
    target_app.change_date = timestamp_in_seconds
    db.add(target_app)
    db.commit()
    return JSONResponse(
        status_code=200,
        content={"msg": "SUCCESS, application submitted"},
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
