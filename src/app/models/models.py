from enum import Enum

from pydantic import BaseModel, Field


class Add2(BaseModel):
    x: int
    y: int


class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consummables"


class Item(BaseModel):
    """Representation of an item in the system. Attributes with Field will have Field details show up in /docs."""

    name: str = Field(description="Name of the item.")
    price: float = Field(description="Price of the item in dollars.")
    count: int = Field(description="Amount of instances of this item in stock.")
    id: int = Field(description="Unique integer identifying the item.")
    category: Category = Field(description="Category this item belongs to.")


items: dict[int, Item] = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES),
}
