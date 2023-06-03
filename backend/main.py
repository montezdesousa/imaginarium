from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import validators
from engine.main import get_result_urls


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ERROR = [
    {
        "id": "b29z0iltxk4",
        "urls": {
            "img": "https://i.imgflip.com/7kfw9i.jpg",
            "page": "https://i.imgflip.com/7kfw9i.jpg",
        },
        "title": "Image not Found",
    }
]

INVALID_URL = [
    {
        "id": "b29z0iltxk4",
        "urls": {
            "img": "https://i.imgflip.com/7kfuyn.jpg",
            "page": "https://i.imgflip.com/7kfuyn.jpg",
        },
        "title": "Invalid URL",
    }
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/search")
async def search(
    q: str,
):
    if q == "undefined":
        return {"results": []}
    if validators.url(q):
        try:
            r = get_result_urls(q, "master_db")
            if r:
                results = [
                    {"id": str(i), "urls": {"img": img_url, "page": page_url}, "title": page_title} for i, (img_url, page_url, page_title) in enumerate(r)
                ]
                return {"results": results}
        except Exception as e:
            print(e)
            return {"results": ERROR}
    return {"results": INVALID_URL}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)