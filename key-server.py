# key-server.py

import sys
import threading
import socket
import pyautogui
import click


DEFAULT_HOST = "all"  # Listen to all incoming connections by default
DEFAULT_PORT = 20459  # Default port to listen on
EXIT_COMMANDS = ["exit", "quit", "q"]  # Entering one of these exits the server
BUFFER_LIMIT = 1024  # Maximum message size


def print_keys():
	"""Prints the list of keys that the server can accept."""
	
	print("List of supported keys:")
	print('\n'.join([key for key in pyautogui.KEYBOARD_KEYS if key.strip() != ""]))



def serve(host, port, silent):
	"""Handles all key requests."""
	
	# Listening for all addresses is done by passing an emptyu string to the
	# socket
	if host.strip().lower() == DEFAULT_HOST:
		host = ""
	
	# Listen on the socket for key clients
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((host, port))
		s.listen()
		
		# Accept connections forever (note: we only support one connection at a
		# time, but the client is only meant to send a single message and exit so it
		# should be fine)
		while True:
			conn, addr = s.accept()
			with conn:
				# Also listen for messages forever, in case someone does decide to make
				# a client that sends multiple messages (this would block other
				# connections though)
				while True:
					# This program isn't meant to get large messages, but the
					# buffer limit can be changed via this constant if necessary
					data = conn.recv(BUFFER_LIMIT)
					if not data:
						continue
					
					# This should hols the keys, delimited by spaces
					keys_string = data.decode()
					if not silent:
						print(f"From {addr[0]}: {keys_string}")
					
					# This splits on whitespace, so having multiple spaces is
					# fine (our client doesn't do that, but still)
					keys = keys_string.split()
					
					# If somehow we got no data we fail (our client doesn't do
					# that, but still)
					if len(keys) == 0:
						conn.sendall("No data received (empty message).".encode())
						continue
					
					# Validate the received keys before pressing anything
					for key in keys:
						if key not in pyautogui.KEYBOARD_KEYS:
							# We only send the first invalid key we find
							conn.sendall(f"Unknown key: {key}".encode())
							break
					else:
						# If we've reached here then all the keys are valid
						try:
							# Press all the keys in sequence and release them in
							# reverse order (this makes key combinations like
							# "alt tab" work)
							pyautogui.hotkey(*keys)
							
							# Reply successfully
							conn.sendall("OK".encode())
						
						# Send any exceptions as-is to the client
						except Exception as ex:
							conn.sendall(str(ex).encode())


def read_input():
	"""Reads lines from stdin until an exit command is read."""
	line = ""
	while line not in EXIT_COMMANDS:
		line = input().strip().lower()


@click.command()
@click.option("-h", "--host", metavar="ADDRESS", default=DEFAULT_HOST, help="Listening address.", show_default=True)
@click.option("-p", "--port", metavar="PORTNUM", default=DEFAULT_PORT, help="Listening port.", show_default=True)
@click.option("-s", "--silent", is_flag=True, help="Do not display any output.")
@click.option("--show-keys", is_flag=True, help="List the supported keys that can be sent.")
def start(host, port, silent, show_keys):
	"""Simple key server which accepts requests for pressing key commbinations."""
	
	# If asked to display the keys, ignore everything else
	if show_keys:
		print_keys()
		return
	
	# We do the listening on a separate thread so that we can let the user enter
	# an exit command
	server_thread = threading.Thread(target=serve, daemon=True, args=[host, port, silent])
	server_thread.start()
	if not silent:
		print('Listening for key messages. Type "exit" / "quit" / "q" to exit.')
	
	# The command-reading loop
	read_input()


if __name__ == "__main__":
	try:
		start()
	
	# Pokemon exception handling for regular users, because if you want to read
	# the stack trace and fix something in this program when something bad
	# happens, then you should also know how to disable this =)
	except Exception as ex:
		print(f"Error: {ex}")
