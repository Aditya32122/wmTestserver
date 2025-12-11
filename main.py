from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    item_id: str
    description: str = None

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items")
async def read_items():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]

