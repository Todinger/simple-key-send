# key-client.py

import socket
import click


DEFAULT_HOST = "localhost"  # Use localhost by default
DEFAULT_PORT = 20459  # Default port used by the server
BUFFER_LIMIT = 1024  # Maximum message size


@click.command()
@click.option("-h", "--host", metavar="ADDRESS", default=DEFAULT_HOST, help="Listening address.", show_default=True)
@click.option("-p", "--port", metavar="PORTNUM", default=DEFAULT_PORT, help="Listening port.", show_default=True)
@click.option("-s", "--silent", is_flag=True, help="Do not display any output.")
@click.argument("keys", nargs=-1)
def send(host, port, silent, keys):
	"""Simple key client which sends the given KEYS to the simple key server."""
	
	# Running with no parameters shows the help message
	if len(keys) == 0:
		ctx = click.get_current_context()
		click.echo(ctx.get_help())
		return
	
	
	# Send the given keys with spaces between them
	# NOTE: We let the server deal with bad keys, since it needs to do it anyway
	# and it makes the client simpler
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, port))
		s.sendall(' '.join(keys).encode())
		s.settimeout(5.0)
		data = s.recv(BUFFER_LIMIT)
		
		# A successful reply should be "OK", otherwise it's an error message
		# (we can just print it either way)
		if data and not silent:
			print(data.decode())


if __name__ == "__main__":
	try:
		send()
	
	# Pokemon exception handling for regular users, because if you want to read
	# the stack trace and fix something in this program when something bad
	# happens, then you should also know how to disable this =)
	except Exception as ex:
		print(f"Error: {ex}")
