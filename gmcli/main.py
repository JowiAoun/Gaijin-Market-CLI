from .models.User import User
import json
import click

settings = json.load(open('./gmcli/settings.json', 'r'))
try:
  user = User(settings)
except ValueError as err:
  click.echo("Error: could not retrieve Gaijin Market token.\nPlease provide a token with the command 'gmcli set-token -t ey...'")
  exit(1)


@click.group()
def main():
    pass

@main.command()
@click.option("--embed", "-e", is_flag=True, default=False, show_default=True, type=bool, help="Embed balance in the form: 'Balance: $1.23'")
def balance(embed: bool):
  """
  Prints the balance in the form: '1.23'
  """
  if embed:
    click.echo(f"Balance: ${user.get_balance()}")
  else:
    click.echo(user.get_balance())

@main.command()
def inventory():
  click.echo("Here's the inventory: ...")

@main.command()
@click.option("--token", "-t", default=None, type=str, help="New token to use for market interactions")
def set_token(new_token: str | None):
  if new_token is None:
    click.echo("Error: could not set token. Please provide a valid Gaijin Market token.")
    return

  settings['token'] = new_token
  with open('./gmcli/settings.json', 'w') as f:
    json.dump(settings, f)
  click.echo("New token has been set")

if __name__ == "__main__":
  main()
