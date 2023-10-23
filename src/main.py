# --- Imports
import click
from functions import get_balance, get_inventory_ids


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
