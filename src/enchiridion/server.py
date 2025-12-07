import glob
import hashlib
import pathlib
import random
import textwrap
from datetime import datetime, timezone

from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def index() -> RedirectResponse:
    return RedirectResponse(url="/enchiridion.txt")


@app.get("/chapters")
def list() -> Response:
    chapters = [c.name for c in pathlib.Path(__file__).parent.glob("chapters/*.txt")]
    return Response(
        content="\n".join(f"- {c}" for c in chapters), media_type="text/plain"
    )


def read_chapter(chapter: str) -> str:
    """Return the  text of a chapter, wrapped to 32 characters."""

    fpath = pathlib.Path(__file__).parent / "chapters" / f"{chapter}.txt"

    if not fpath.exists():
        return Response(
            status_code=404, content="Chapter not found", media_type="text/plain"
        )

    with open(fpath, "r") as f:
        return textwrap.fill(f.read().replace("\n", " ").replace("  ", "\n"), width=39)


@app.get("/chapters/{chapter}")
def chapter(chapter: str) -> Response:
    """Return ..."""
    return Response(
        content=read_chapter(chapter),
        media_type="text/plain",
    )


@app.get("/enchiridion.txt")
def enchiridion_text() -> Response:

    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    chapters = sorted(
        path.with_suffix("").name
        for path in pathlib.Path(__file__).parent.glob("chapters/*.txt")
    )

    index = int(hashlib.sha256(now.encode()).hexdigest(), 16) % len(chapters)

    chapter = chapters[index]

    return Response(
        content=read_chapter(chapter),
        media_type="text/plain",
    )
