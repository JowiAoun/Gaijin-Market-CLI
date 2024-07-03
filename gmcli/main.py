from gmcli.models.GaijinMarketSettings import SettingsKey
from gmcli.models.User import User
import click

user = User(id=1)

@click.group()
def main():
  pass

@main.command()
@click.option("--embed", "-e", is_flag=True, default=False, show_default=True, type=bool, help="Embed balance in the form: 'Balance: $1.23'")
def balance(embed: bool):
  """
  Prints the balance in the form: '1.23'
  """
  bal = user.get_balance()
  if bal == -1:
    click.echo(f"Error: could not get balance.")
    return

  if embed:
    click.echo(f"Balance: ${bal}")
  else:
    click.echo(bal)

@main.command()
@click.option("--embed", "-e", is_flag=True, default=False, show_default=True, type=bool, help="Embed balance in the form: 'Balance: $1.23'")
def inventory(embed: bool):
  if embed:
    click.echo(f"Inventory: ${user.get_inventory()}")
  else:
    click.echo(user.get_inventory())

@main.command()
@click.option("--token", "-t", default=None, type=str, help="New token to use for market interactions")
def set_token(token: str):
  """
  Sets the token for the user
  """
  if token is None:
    click.echo("Error: could not set token. Please provide a valid Gaijin Market token.")
    return

  user.set_token(token)
  click.echo("Success: New token has been set")

@main.command()
def dev_test():
  """
  Development testing command
  """
  click.echo(user.dev_test())

if __name__ == "__main__":
  main()
