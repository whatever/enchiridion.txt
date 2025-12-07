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
    chapters = sorted(
        (c.name for c in pathlib.Path(__file__).parent.glob("chapters/*.txt")),
        key=lambda c: convert_to_int(pathlib.Path(c).with_suffix("").name),
    )
    return Response(
        content="\n".join(f"- {c}" for c in chapters), media_type="text/plain"
    )


def convert_to_int(s: str) -> int:
    """Return the integer value of a Roman numeral."""

    s = s.upper()

    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}

    total = 0
    i = 0

    while i < len(s):
        # Look ahead for subtractive pair
        if i + 1 < len(s) and values[s[i]] < values[s[i + 1]]:
            total += values[s[i + 1]] - values[s[i]]
            i += 2
        else:
            total += values[s[i]]
            i += 1

    return total


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
