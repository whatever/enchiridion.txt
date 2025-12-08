import glob
import hashlib
import pathlib
import random
import textwrap
from datetime import datetime, timezone

from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

from .utils import convert_to_int, read_chapter

app = FastAPI()


@app.get("/")
def index() -> RedirectResponse:
    return RedirectResponse(url="/enchiridion.txt")


@app.get("/chapters")
def list() -> Response:
    chapters = sorted(
        (c.name for c in pathlib.Path(__file__).parent.glob("chapters/*.txt")),
        key=lambda c: convert_to_int(pathlib.Path(c).with_suffix("").name),
    )
    return Response(
        content="\n".join(f"- {c}" for c in chapters),
        media_type="text/plain",
    )


@app.get("/chapters/{chapter}")
def chapter(chapter: str) -> Response:
    """Return ..."""
    content = read_chapter(chapter)
    if content is None:
        return Response(
            status_code=404,
            media_type="text/plain",
        )
    return Response(content=content, media_type="text/plain")


@app.get("/enchiridion.txt")
def enchiridion_text() -> Response:

    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    chapters = sorted(
        path.with_suffix("").name
        for path in pathlib.Path(__file__).parent.glob("chapters/*.txt")
    )

    index = int(hashlib.sha256(now.encode()).hexdigest(), 16) % len(chapters)

    content = read_chapter(chapters[index])

    if content is None:
        return Response(
            status_code=404,
            media_type="text/plain",
        )

    return Response(
        content=content,
        media_type="text/plain",
    )


@app.exception_handler(404)
def not_found(_, __):
    return Response(
        status_code=404,
        media_type="text/plain",
        content="lost",
    )
