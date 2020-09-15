import store
from store.core import S3, jprint
import click


@click.group()
def cli():
    """A CLI for gathering summary statistics about s3 buckets"""


@cli.command()
@click.option(
    "-p", "--profile", default="default", help="AWS Profile (default: 'default')"
)
@click.option(
    "-r", "--region", default="us-east-1", help="AWS Region (default: 'us-east-1')"
)
@click.option(
    "-b",
    "--buckets",
    help="Specify a subset buckets with '-b foo,bar,baz' \n(default: all buckets)",
    default=None,
)
@click.option(
    "-u",
    "--units",
    type=click.Choice(["KB", "MB", "GB", "TB"]),
    help="Specify a bytes unit prefix \n(default: optimal unit)",
    default=None,
)
@click.option(
    "-p",
    "--parallel",
    is_flag=True,
    help="Use rudimentary parallelization (default: False)",
)
def summary(profile, region, buckets, units, parallel):
    """Print Summary statistics for all buckets for a given AWS Profile and Region"""
    if buckets is not None:
        buckets.split(",")
    jprint(
        S3(profile=profile, region=region).summary(
            buckets=buckets, units=units, parallel=parallel
        )
    )


if __name__ == "__main__":
    cli()
