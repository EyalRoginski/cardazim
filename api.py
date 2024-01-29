from flask import Flask, send_file
import click
from saver import Saver
from card_id import CardID

app = Flask(__name__)
saver: Saver = None


@app.route("/creators/")
def get_creators():
    """
    Get a list of all creators in a JSON format.
    """
    print("getting creators")
    return saver.get_creators()


@app.route("/creators/<creator>/cards/")
def get_cards(creator: str):
    """
    Get a list of the names of all the cards a creator has submitted in a JSON format.
    """
    return saver.get_cards(creator)


@app.route("/creators/<creator>/cards/<card_name>/")
def get_card_metadata(creator: str, card_name: str):
    """
    Get a card's metadata via its creator and name, in a JSON format with the fields:

    `creator`, `name`, `riddle`, `solution`, `image_path`
    """
    metadata = saver.get_card_metadata(CardID(card_name, creator))
    # Image path in HTML and not in file system to keep it RESTful.
    metadata[
        "image_path"
    ] = f"/creators/{metadata['creator']}/cards/{metadata['name']}/image.jpg"
    return metadata


@app.route("/creators/<creator>/cards/<card_name>/image.jpg")
def get_card_image(creator: str, card_name: str):
    """
    Get the image of a card via its creator and name.
    """
    metadata = saver.get_card_metadata(CardID(card_name, creator))
    image_path = metadata["image_path"]
    return send_file(image_path)


@app.route("/")
def homepage():
    """
    Homepage for Cardazim.
    """
    return "<h1>Cardazim!</h1>"


@click.command()
@click.option(
    "--host",
    "-h",
    default="127.0.0.1",
    help="The host to run the API on. Defaults to 127.0.0.1",
)
@click.option(
    "--port",
    "-p",
    default=5000,
    help="The port to run the API on. Defaults to 5000",
)
@click.option(
    "--database-url",
    "-d",
    default="mongodb://127.0.0.1:27017",
    help="A URL for the database to use. Defaults to mongodb://127.0.0.1:27017",
)
def run_api_server(host: str, port: int | str, database_url: str):
    """
    Run the REST API on `host:port`, using a database as defined by `database_url`.
    """
    click.echo(f"Hosting on {host}:{port} with database {database_url}")
    # pylint: disable-next=global-statement
    global saver
    saver = Saver(database_url)
    app.run(host, port)


if __name__ == "__main__":
    # pylint: disable-next=E1120
    run_api_server()
