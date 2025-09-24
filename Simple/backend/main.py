import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient


class Fruit(BaseModel):
    name: str


class Fruits(BaseModel):
    fruits: List[Fruit]


app = FastAPI(debug=True)

# ✅ MongoDB connection
# ✅ MongoDB connection
MONGO_URL = "mongodb+srv://"
client = AsyncIOMotorClient(MONGO_URL)
db = client["pydata"]   # Database name (same as connection string)
collection = db["fruits"]  # Collection name


# ✅ CORS setup
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# @app.get("/")
# def read_root():
#     return PlainTextResponse("HI your server is running successfully")



@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Server Status</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #a1c4fd, #c2e9fb); /* light gradient */
                color: #333;
                text-align: center;
            }
            .container {
                background: rgba(255, 255, 255, 0.8);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                animation: fadeIn 2s ease-in-out;
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 20px;
                color: #1a1a1a;
            }
            p {
                font-size: 1.5rem;
                margin: 0;
                color: #555;
            }
            @keyframes fadeIn {
                0% { opacity: 0; transform: translateY(-50px); }
                100% { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Server is Running!</h1>
            <p>Your FastAPI backend is working perfectly.</p>
        </div>
    </body>
    </html>
    """


# ✅ GET fruits (fetch from MongoDB)
@app.get("/fruits", response_model=Fruits)
async def get_fruits():
    fruits_cursor = collection.find({})
    fruits_list = []
    async for fruit in fruits_cursor:
        fruits_list.append(Fruit(name=fruit["name"]))
    return Fruits(fruits=fruits_list)


# ✅ POST fruit (insert into MongoDB)
@app.post("/fruits")
async def add_fruit(fruit: Fruit):
    await collection.insert_one(fruit.dict())
    return fruit


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
