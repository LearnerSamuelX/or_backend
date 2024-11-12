from database import Base
from sqlalchemy import Column, String, Integer, DATE


class Applications(Base):
    """
    appID VARCHAR
    appStatus INT -- 1, 2, 3, 4, 5-finished
    changeDate DATE
    """

    __tablename__ = "applications"
    app_id = Column(String, primary_key=True, index=True)
    app_status = Column(Integer)
    change_date = Column(String)
