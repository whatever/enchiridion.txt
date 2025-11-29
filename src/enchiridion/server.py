import glob
import pathlib
import random

from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def index() -> RedirectResponse:
    return RedirectResponse(url="/enchiridion.txt")


@app.get("/enchiridion.txt")
def enchiridion_text() -> Response:

    chapters = glob.glob(str(pathlib.Path(__file__).parent / "chapters" / "*.txt"))

    chapter = random.choice(chapters)

    with open(chapter, "r") as f:
        return Response(
            content=f.read(),
            media_type="text/plain",
        )
