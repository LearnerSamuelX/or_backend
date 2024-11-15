from typing import Optional
from pydantic import BaseModel


class App(BaseModel):
    app_status: int

    class Config:
        model_config = {"from_attributes": True}


class AppDelete(BaseModel):
    app_id: str


class AppInfo(BaseModel):

    app_id: str

    # for personal information
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    dl_num: Optional[str] = None
    dob: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[int] = None

    # for residential address
    province: Optional[str] = None
    postalcode: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    street: Optional[str] = None
    street_num: Optional[int] = None

    class Config:
        model_config = {"from_attributes": True}


class ValidatedAppInfo(BaseModel):

    app_id: str

    # for personal information
    first_name: str
    last_name: str
    middle_name: str
    dl_num: str
    dob: int
    gender: str
    height: int

    # for residential address
    province: str
    postalcode: str
    city: str
    province: str
    street: str
    street_num: str


class PersonalInfo(BaseModel):

    app_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    dl_num: Optional[str] = None
    dob: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[int] = None

    class Config:
        model_config = {"from_attributes": True}


class ResAddress(BaseModel):

    app_id: str
    province: Optional[str] = None
    postalcode: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    street_num: Optional[int] = None

    class Config:
        model_config = {"from_attributes": True}
