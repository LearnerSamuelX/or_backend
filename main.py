from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse

from uuid import uuid4
import schemas  # from the ./models.py
from database import engine, SessionLocal  # from the ./database.py
from datetime import datetime
from sqlalchemy.orm import Session
from pydantic import BaseModel

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


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


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

    res_address_model = schemas.ResidentialAddress()
    res_address_model.app_id = app_id
    res_address_model.res_id = app_id

    db.add(application_model)
    db.add(res_address_model)
    db.commit()
    db.refresh(application_model)

    return application_model


# @app.post("/save")
# async def save_application(application: App, db: Session = Depends(get_db)):
#     """
#     save an application
#     """
#     res_address_model = schemas.ResidentialAddress()
#     res_address_model.res_id = str(uuid4())
#     return


@app.delete("/delete")
async def delete_application(appDelete: AppDelete, db: Session = Depends(get_db)):
    """
    Delete ONE application
    """
    app_id = appDelete.app_id
    application = db.query(schemas.Application).filter(schemas.Application.app_id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(application)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={"msg": "SUCCESS, application deleted"},
    )
