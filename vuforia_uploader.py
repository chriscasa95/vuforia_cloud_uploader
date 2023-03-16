import click
import json

from app.ImageUploader import ImageUploader


@click.group()
def cli():
    """Version: 0.1"""
    pass


@click.group()
def upload():
    pass


@click.command()
def update():
    click.echo("Not implemented!")


@click.command()
def get():
    click.echo("Not implemented!")


@click.command()
def delete():
    click.echo("Not implemented!")


@click.command()
@click.option("-p", "--path", required=True, type=str)
@click.option("-ak", "--server_access_key", required=True, type=str)
@click.option("-sk", "--server_secret_key", required=True, type=str)
@click.option("-n", "--name", required=True, type=str)
@click.option("-w", "--width", required=True, type=float, default=1)
@click.option("-m", "--meta_path", type=str, default="", help="Path to JSON file.")
def image(server_access_key, server_secret_key, path, name, width, meta_path):
    uploader = ImageUploader(server_access_key, server_secret_key)
    metadata = __get_metadata(meta_path)

    uploader.upload_image(path, name, width, metadata)


@click.command()
@click.option("-p", "--path", required=True, type=str)
@click.option("-ak", "--server_access_key", required=True, type=str)
@click.option("-sk", "--server_secret_key", required=True, type=str)
@click.option("-n", "--name", required=True, type=str)
@click.option("-w", "--width", required=True, type=float, default=1)
@click.option("-m", "--meta_path", type=str, default="", help="Path to JSON file.")
def folder(server_access_key, server_secret_key, path, name, width, meta_path):
    uploader = ImageUploader(server_access_key, server_secret_key)
    metadata = __get_metadata(meta_path)

    uploader.upload_images_from_folder(path, name, width, metadata)


@click.command()
@click.option("-p", "--path", required=True, type=str)
@click.option("-ak", "--server_access_key", required=True, type=str)
@click.option("-sk", "--server_secret_key", required=True, type=str)
@click.option("-n", "--name", required=True, type=str)
@click.option("-w", "--width", required=True, type=float, default=1)
@click.option("-#", "--number_of_images", type=int, default=30)
@click.option("-m", "--meta_path", type=str, default="", help="Path to JSON file.")
def video(
    server_access_key, server_secret_key, path, name, width, meta_path, number_of_images
):
    uploader = ImageUploader(server_access_key, server_secret_key)
    metadata = __get_metadata(meta_path)

    uploader.upload_video(path, name, width, number_of_images, metadata)


def __get_metadata(meta_path: str) -> str:
    metadata = ""

    if meta_path:
        with open(meta_path) as fd:
            metadata = json.dumps(json.load(fd))

    return metadata


upload.add_command(image)
upload.add_command(folder)
upload.add_command(video)

cli.add_command(upload)
cli.add_command(update)
cli.add_command(get)
cli.add_command(delete)


if __name__ == "__main__":
    cli()
