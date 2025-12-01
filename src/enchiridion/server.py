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


@app.get("/list")
def list() -> Response:
    chapters = [c.name for c in pathlib.Path(__file__).parent.glob("chapters/*.txt")]
    return Response(
        content="\n".join(f"- {c}" for c in chapters), media_type="text/plain"
    )


@app.get("/chapters/{chapter}")
def chapter(chapter: str) -> Response:

    fpath = pathlib.Path(__file__).parent / "chapters" / f"{chapter}.txt"

    if not fpath.exists():
        return Response(
            status_code=404, content="Chapter not found", media_type="text/plain"
        )

    with open(fpath, "r") as f:
        return Response(content=f.read(), media_type="text/plain")


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
