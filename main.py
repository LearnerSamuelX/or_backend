from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse

from uuid import uuid4
import schemas  # from the ./models.py
from database import engine, SessionLocal  # from the ./database.py
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

app = FastAPI()

schemas.Base.metadata.create_all(bind=engine)


class App(BaseModel):
    app_id: str
    app_status: int
    change_date: str

    class Config:
        model_config = {"from_attributes": True}


class Apps(BaseModel):
    apps: List[App]


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


@app.get("/applications", response_model=List[App])
async def get_applications(db: Session = Depends(get_db)):
    results = db.query(schemas.Applications).all()
    return results


@app.post("/create")
async def read_api(application: App, db: Session = Depends(get_db)):
    application_status = application.app_status
    application_date = application.change_date

    application_model = schemas.Applications()
    application_model.app_id = str(uuid4())
    application_model.app_status = application_status
    application_model.change_date = application_date
    db.add(application_model)
    db.commit()
    db.refresh(application_model)

    return JSONResponse(
        status_code=200,
        content={"msg": "SUCCESS, application created"},
    )
