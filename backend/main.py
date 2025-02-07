from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from models.model import Transaction
from bson import ObjectId  # Import ObjectId
from fastapi import HTTPException

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # React app's URL: Use this if normally running on vs code
    # allow_origins=["http://localhost"], # React app's URL: if run using docker
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017") # Use this if normally running on vs code
# client = AsyncIOMotorClient("mongodb://mongo:27017")  # Change localhost -> mongo(if run using docker)
db = client.transactionDB
collection = db.transactions


@app.get("/")
async def home():
    return {"message" : "Hello"}

@app.post("/transactions")
async def add_transaction(transaction: Transaction):
    print(transaction)
    transaction_dict = transaction.model_dump() # To convert into dictionary
    result = await collection.insert_one(transaction_dict)
    transaction_dict["_id"] = str(result.inserted_id) # Convert ObjectId to string
    return transaction_dict

@app.get("/transactions")
async def get_transactions():
    transactions = await collection.find().to_list(100)

    # Convert ObjectId to string for each transaction
    for transaction in transactions:
        transaction["_id"] = str(transaction["_id"])

    return transactions

@app.put("/transactions/{transaction_id}")
async def update_transaction(transaction_id: str, transaction: Transaction):
    if not ObjectId.is_valid(transaction_id):  # Validate before using ObjectId
        raise HTTPException(status_code=400, detail="Invalid transaction ID format")
    
    transaction_dict = transaction.model_dump()
    result = await collection.update_one({"_id": ObjectId(transaction_id)}, {"$set": transaction_dict})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return {"message": "Transaction updated successfully"}

@app.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: str):
    if not ObjectId.is_valid(transaction_id):  # Validate before using ObjectId
        raise HTTPException(status_code=400, detail="Invalid transaction ID format")
    
    result = await collection.delete_one({"_id": ObjectId(transaction_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return {"message": "Transaction deleted successfully"}