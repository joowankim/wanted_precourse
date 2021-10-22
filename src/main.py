from fastapi import FastAPI

import post
import member

app = FastAPI()
app.include_router(post.router)
app.include_router(member.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
