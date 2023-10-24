# --- Imports
import click
from functions import get_balance


# --- Commands
@click.group()
def main():
    pass

@main.command()
def balance():
    click.echo(f"Balance: ${get_balance()}")

@main.command()
def inventory():
    click.echo("Here's the inventory: ...")

@main.command()
def test():
    click.echo("Nothing set to test...")