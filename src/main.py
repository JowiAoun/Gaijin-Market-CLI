# --- Imports
import click
import time
from functions import get_balance, db_populate_items_static, db_populate_items_inventory, db_populate_items_variable, get_item_variable_data


# --- Commands
@click.group()
def main():
    pass

@main.command()
def balance():
    """
    Prints the balance in the form: 'Balance: ${balance}'
    Uses get_balance() function to get balance value.
    """

    click.echo(f"Balance: ${get_balance()}")

@main.command()
def inventory():
    click.echo("Here's the inventory: ...")

@main.command()
@click.option("--run", "-r", default=True, show_default=True, type=bool, help="Execute commands.")
@click.option("--delay", "-d", default=5, show_default=True, type=int, help="The number of minutes to wait before executing loop again")
def loop(run, delay):
    while(run):
        click.echo(f"Currently running: {run}")
        time.sleep(delay) #? Multiply by 60 for minutes after testing

@main.command()
def test():
    print(get_item_variable_data("id10030_sons_of_attila_key"))
    click.echo("Test completed")
