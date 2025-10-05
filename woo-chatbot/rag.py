"""This is where I'll write the RAG logic for my app.
I'll attempt it with langchain and co.
make sure to pip install httpx
"""
import pprint
import httpx
import asyncio

async def fetch_products():
    url = "https://dummyjson.com/products"
    async with httpx.AsyncClient() as client:
        feedback = await client.get(url)
        feedback = feedback.json()

        product_list = []  #the list of products in json dict
        for item in feedback.get("products", []):
            product_list.append({
                "name": item.get("title"),
                "description": item.get("description"),
                "tags": ", ".join(item.get("tags", [])),  # convert list → string
                "price": item.get("price"),
                "availability": item.get("availabilityStatus"),
                "thumbnail": item.get("thumbnail"),
            })
        return product_list

if __name__ == "__main__":
    async def main():
        cart = await fetch_products()
        #pprint.pprint(cart[:5])
        for c in cart[:5]:
            print(f"{c['name']} - {c['tags']} - {c['description'][:50]}... - ${c['price']}")

    asyncio.run(main())

