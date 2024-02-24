from sqlalchemy import Column, String, Integer, Date
from utils.db import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String, nullable=False)
    created = Column(Date, nullable=False)
    status = Column(String, nullable=False)

class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, nullable=False)
    item = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)