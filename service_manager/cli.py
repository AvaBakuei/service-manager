import typer

app = typer.Typer()


@app.command()
def hello():
    """ Say Hello. """
    print("Hello from Service Manager!")


if __name__ == "__main__":
    app()
