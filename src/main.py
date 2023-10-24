# --- Imports
import click
from functions import get_balance, get_item


# --- Commands
@click.group()
def main():
    pass

@main.command()
def balance():
    click.echo(f"Balance: ${get_balance()}")

@main.command()
def item():
    click.echo(get_item(100130))

@main.command()
def inventory():
    click.echo("Here's the inventory: ...")
