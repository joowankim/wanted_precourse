from fastapi import FastAPI

import post
import user

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
