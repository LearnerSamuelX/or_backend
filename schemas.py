from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Application(Base):
    """
    appID VARCHAR
    appStatus INT -- 1, 2, 3, 4, 5-finished
    changeDate DATE
    """

    __tablename__ = "application_table"
    app_id = Column(String, primary_key=True, index=True)
    app_status = Column(Integer)
    change_date = Column(Integer)

    to_res = relationship("ResidentialAddress", back_populates="r_address", cascade="all, delete-orphan")
    to_pi = relationship("PersonalInfo", back_populates="personal_info", cascade="all, delete-orphan")


class PersonalInfo(Base):
    __tablename__ = "personal_info_table"
    app_id = Column(String, ForeignKey("application_table.app_id"), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    dl_num = Column(String)
    dob = Column(Integer)
    gender = Column(String)
    height = Column(Integer)

    personal_info = relationship("Application", back_populates="to_pi")


class ResidentialAddress(Base):
    __tablename__ = "address_table"
    app_id = Column(String, ForeignKey("application_table.app_id"), primary_key=True)
    province = Column(String)  # drop down
    postalcode = Column(String)
    city = Column(String)
    province = Column(String)
    street = Column(String)
    street_num = Column(Integer)

    r_address = relationship("Application", back_populates="to_res")
