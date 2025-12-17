import pathlib
import textwrap


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


def read_chapter(chapter: str) -> str | None:
    """Return the  text of a chapter, wrapped to 32 characters."""

    fpath = pathlib.Path(__file__).parent / "chapters" / f"{chapter}.txt"

    if not fpath.exists():
        return None

    with open(fpath, "r") as f:
        return (
            chapter
            + "\n\n"
            + textwrap.fill(
                text=f.read().replace("\n", " ").replace("  ", "\n"),
                width=39,
            )
        )
