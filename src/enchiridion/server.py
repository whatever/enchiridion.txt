import glob
import pathlib
import random
from datetime import datetime, timezone

from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def index() -> RedirectResponse:
    return RedirectResponse(url="/enchiridion.txt")


@app.get("/enchiridion.txt")
def enchiridion_text() -> Response:

    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    chapters = sorted(
        glob.glob(str(pathlib.Path(__file__).parent / "chapters" / "*.txt"))
    )

    print(now, hash(now) % len(chapters))

    chapter = chapters[hash(now) % len(chapters)]

    with open(chapter, "r") as f:
        return Response(
            content=f.read(),
            media_type="text/plain",
        )
