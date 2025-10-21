import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from redis_om import get_redis_connection, HashModel
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Connect to Redis
redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASS"),
    decode_responses=True
)

class ProductCreate(BaseModel):
    name: str
    price: float
    descr: str
    quantity: int


#create a product class for the db, should extend from HashModel
class Product(HashModel):
    name: str
    price: float
    descr: str
    quantity: int

    #write another class to connect db to redis
    class Meta:
        database = redis


@app.get("/")
def root():
    return {"message": "Your API is running!"}


def format_product(pk: str):
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "descr": product.descr,
        "quantity": product.quantity
    }

@app.get("/products")
def get_all():
    #return Product.all_pks() #returns only the primary keys to the products not values
    #correct way after creating the below function
    return [format_product(pk) for pk in Product.all_pks()]


@app.post("/products")
async def create_product(product: ProductCreate):
    new_product = Product(**product.model_dump())
    new_product.save()
    return new_product



@app.get(
    "/products/{pk}",
    summary="Get Product by ID"
)
async def get_pk(pk: str):
    return Product.get(pk)

@app.delete("/products/{pk}")
async def delete_product(pk: str):
    return Product.delete(pk)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
