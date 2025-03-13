from sqlalchemy import Column, Integer, String
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, nullable=False)
