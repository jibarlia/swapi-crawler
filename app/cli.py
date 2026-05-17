import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    print(f"{name} Welcome to the Public API Crawler Template")

if __name__ == "__main__":
    app()