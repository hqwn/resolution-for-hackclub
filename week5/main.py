#imports
from logging import info
import secrets
import sqlite3
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Header
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# initaliziation
BASE_DIR = os.path.dirname(__file__)
app = FastAPI()
conn = sqlite3.connect("quotes.db")
cursor = conn.cursor()
app.mount("/static", StaticFiles(directory="static"), name="static")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL UNIQUE,
        owner TEXT NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote TEXT NOT NULL,
        owner TEXT NOT NULL
    )
""")

conn.commit()


#Api key/Limiter

def get_api_key(request: Request) -> str:
    return request.headers.get("x-api-key", "unknown")

class RegisterBody(BaseModel):
    name: str

class AddQuote(BaseModel):
    new_quote: str


def create_api_key(owner: str) -> str:
    key = secrets.token_hex(16)
    cursor.execute(
        "INSERT INTO api_keys (key, owner) VALUES (?, ?)",
        (key, owner)
    )
    conn.commit()
    return key

async def verify_api_key(x_api_key: str = Header()):
    cursor.execute("SELECT * FROM api_keys WHERE key = ?", (x_api_key,))
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return result

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later!"}
    )


def delete(name: str):
    with sqlite3.connect("quotes.db") as background_conn:
            background_cursor = background_conn.cursor()
            background_cursor.execute(
                "DELETE FROM quotes WHERE owner = ?", 
                (name,)
            )
            
            background_conn.commit()
limiter = Limiter(key_func=get_api_key)
app.state.limiter = limiter




# Routes

@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.post("/register")
async def register(body: RegisterBody):
    key = create_api_key(body.name)
    return {"api_key": key, "message": "Save this key! You won't be able to see it again."}


@app.post("/quote", dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
async def add_quote(request: Request, quote: AddQuote, info = Depends(verify_api_key)):
    cursor.execute("INSERT INTO quotes (quote, owner) VALUES (?, ?)", (quote.new_quote, info[2]))
    conn.commit()
    return {"message": "Quote added!"}


@app.get("/quote", dependencies=[Depends(verify_api_key)])
@limiter.limit("60/minute")
async def get_quote(request: Request):
    cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1;")
    quote = cursor.fetchone()
    if quote is None:
        raise HTTPException(status_code=404, detail="No quotes found")
    return {"quote": quote[1], "owner": quote[2]}

@app.get("/quotes/{amount}", dependencies=[Depends(verify_api_key)])
@limiter.limit("60/minute")
async def get_multiple_quotes(request: Request,amount: int):
    cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT ?;", (amount,))
    quotes = cursor.fetchall()
    result = []

    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes found")
    else:
        for i in quotes:
            result.append({"quote": i[1], "owner": i[2]})

    return result


@app.get("/my-info")
async def my_info(key_info = Depends(verify_api_key)):
    return {"owner": key_info[2]}


@app.delete("/quotes/delete", dependencies=[Depends(verify_api_key)])
async def delete_all_your_quotes(background_tasks: BackgroundTasks, key_info = Depends(verify_api_key)):
    background_tasks.add_task(delete, key_info[2])
    return {"message": "Your quotes are now deleted!"}

