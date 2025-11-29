import click
import uvicorn

from enchiridion.server import app


@click.group()
def entrypoint():
    pass


@entrypoint.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8000)
def serve(host, port):
    uvicorn.run(app, host=host, port=port)
