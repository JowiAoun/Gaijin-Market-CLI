# --- Imports
import click
import time
from functions import get_balance, db_populate_items_static, db_populate_items_inventory, cancel_order, db_populate_items_variable, get_item_variable_data, db_get_hash_by_id, get_open_orders


# --- Commands
@click.group()
def main():
    click.echo("Test start...")
    loop(True, 1000)
    click.echo("Test completed")

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
def loop(run: bool, delay: int):
    while run:
        click.echo(f"Currently running: {run}")
        time.sleep(delay) #? Multiply by 60 for minutes after testing

@main.command()
def test():
    click.echo("Test start...")
    loop(True, 1000)
    click.echo("Test completed")

if __name__ == "__main__":
    main()
