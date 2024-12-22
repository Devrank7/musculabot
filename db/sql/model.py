from sqlalchemy import Integer, Column, DateTime, String, ForeignKey, BigInteger, Enum
from sqlalchemy.orm import relationship

from .connect import Base
from .enums.enums import Lang


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True)
    lang = Column(Enum(Lang), nullable=True, default=None)
    date_week_before_kill = Column(DateTime, nullable=True, default=None)
    date_three_before_kill = Column(DateTime, nullable=True, default=None)
    date_one_before_kill = Column(DateTime, nullable=True, default=None)
    date_of_kill = Column(DateTime, nullable=True, default=None)
    wfp_data = relationship("WFPData", uselist=False, back_populates="user")


class WFPData(Base):
    __tablename__ = 'wtf'
    wfp_id = Column(Integer, primary_key=True)
    order = Column(String(length=255), nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.tg_id'), unique=True)
    user = relationship("User", back_populates="wfp_data")
