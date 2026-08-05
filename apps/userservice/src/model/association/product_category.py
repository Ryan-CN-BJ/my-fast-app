from sqlalchemy import Table, Column, ForeignKey
from model.base import Base

product_category = Table(
    "product_category",
    Base.metadata,
    Column("product_id", ForeignKey("product.id"), primary_key=True),
    Column("category_id", ForeignKey("category.id"), primary_key=True),
)
