# --- Imports
# External
import click
# Internal
import functions as fns


# --- Main function
#@click.command("Hello")
#@click.option('--count', default=1, help='Number of greetings.')
#@click.option('--name', prompt='Your name', help='The person to greet.')
#def hello(count, name):
#    """Simple program that greets NAME for a total of COUNT times."""
#    for x in range(count):
#        click.secho(f"Hello {name}!", fg='green')

@click.command("Sell")
@click.option('--sell', default=1, help='Number of items to sell.')
def sell(sell):
    click.secho(f"Let's sell {sell}!", fg='green')

# --- Execution
if __name__ == '__main__':
    sell()
