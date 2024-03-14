import click
import time

class View:
    def __init__(self):
        pass

    @click.group()
    def main(self):
        click.echo("Test start...")
        self.loop(True, 1000)
        click.echo("Test completed")

    @main.command()
    def balance(self):
        """
        Prints the balance in the form: 'Balance: ${balance}'
        Uses get_balance() function to get balance value.
        """
        click.echo(f"Balance: $UNKNOWN")

    @main.command()
    def inventory(self):
        click.echo("Here's the inventory: ...")

    @main.command()
    @click.option("--run", "-r", default=True, show_default=True, type=bool, help="Execute commands.")
    @click.option("--delay", "-d", default=5, show_default=True, type=int, help="The number of minutes to wait before executing loop again")
    def loop(self, run: bool, delay: int):
        while run:
            click.echo(f"Currently running: {run}")
            time.sleep(delay) # Multiply by 60 for minutes after testing

    @main.command()
    def test(self):
        click.echo("Test start...")
        self.loop(True, 1000)
        click.echo("Test completed")

if __name__ == "__main__":
    view = View()
    view.main()
