from fastapi import FastAPI, Request
from pydantic import BaseModel
import json

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


@app.post("/items")
async def create_item(item: Item, request: Request):
    # Log the payload
    print("=" * 50)
    print("Incoming Request:")
    print("=" * 50)
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Payload: {item.dict()}")
    print("=" * 50)
    
    return {"message": "Item received", "item": item}


# Log all requests (middleware approach)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Get request body
    body = await request.body()
    
    print("\n" + "=" * 60)
    print(f"📥 REQUEST: {request.method} {request.url.path}")
    print("=" * 60)
    print(f"Headers: {dict(request.headers)}")
    
    if body:
        try:
            body_str = body.decode('utf-8')
            print(f"Body: {body_str}")
            # Parse JSON for pretty print
            try:
                body_json = json.loads(body_str)
                print(f"Parsed JSON:\n{json.dumps(body_json, indent=2)}")
            except:
                pass
        except:
            print(f"Body (raw): {body}")
    
    print("=" * 60 + "\n")
    
    # Important: recreate request with body for route handlers
    async def receive():
        return {"type": "http.request", "body": body}
    
    request._receive = receive
    
    response = await call_next(request)
    return response