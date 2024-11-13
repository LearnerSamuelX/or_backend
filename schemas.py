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

    application = relationship("ResidentialAddress", back_populates="r_address")


class ResidentialAddress(Base):
    __tablename__ = "address_table"
    res_id = Column(String, primary_key=True, index=True)
    app_id = Column(String, ForeignKey("application_table.app_id"))
    province = Column(String)  # drop down
    postalcode = Column(String)
    city = Column(String)
    province = Column(String)
    street = Column(String)
    street_num = Column(Integer)

    r_address = relationship("Application", back_populates="application")
