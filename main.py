from fastapi import FastAPI, Depends, Request
from slowapi.errors import RateLimitExceeded

from fastapi.middleware.cors import CORSMiddleware

from src.routes import contacts, auth, users

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

import uvicorn

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

origins = [ 
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix='/api')


@app.get("/")
@limiter.limit("5/minute")  
async def read_root(request: Request):
    return {"message": "Hi There"}


if __name__ == "__main__":
    uvicorn.run(app)