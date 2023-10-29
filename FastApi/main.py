from fastapi import FastAPI

import uvicorn 

from src.routes import contacts, authificate

app = FastAPI()

app.include_router(contacts.router, prefix="/api")
app.include_router(authificate.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app)