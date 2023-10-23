from fastapi import FastAPI

from src.routes import contacts

import uvicorn

app = FastAPI()

app.include_router(contacts.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "welcome there"}


if __name__ == "__main__":
    uvicorn.run(app)