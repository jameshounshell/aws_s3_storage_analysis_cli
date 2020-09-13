import click


@click.group()
def cli():
    """A CLI for gathering summary statistics about s3 buckets"""


@cli.command()
def hello():
    """Say Hello"""
    click.echo("Hello")


if __name__ == "__main__":
    cli()
