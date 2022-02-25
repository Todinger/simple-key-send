# simple-key-send
A simple server and command line client to send keystrokes over LAN.

## Setup
1. Clone this repository.
2. Open a shell (Command Prompt in Windows) on the project folder.
3. Create a Python virtual environment in the project directory, enter it and install the dependencies with these commands in `bash`:
```bash
python -m venv venv
. venv/Scripts/activate
pip install -r requirements.txt
```
And in `cmd`:
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
Start the server by running the virtual environment and then using `python key-server.py`.
Alternatively you can use the shortened scripts (`sks-server` for Linux, `sks-server.bat` on Windows), which activate the environment for you and can be run from any working directory.

After that, run the client with the key sequence you wish to run in order for the server to read and perform it.
Like the server, there are shortcut scripts for entering the virrtual environment and running the client (`sks`, `sks.bat`).
For example, this will perform the Alt+Tab key sequence on the machine that hosts the server:
```bash
$ ./sks alt tab
```
To see a list of supported keys, run the server with the `--show-keys` command.

Generally speaking, you can run both the client and the server with the `--help` flag to see a list of supported options.
There's not much to them - just a configurable host, port, silent mode and the supported key listing.
Running the client without any arguments also results in the help message being shown.

## Goal
The purpose of this project is to enable sending simple keystrokes to other machines over a local network.
I've made it so that I can do things such as bind the 'Shift+Volume Up' sequence on one computer to run `sks -h my-other-pc-hostname volumeup`, thus letting me easily change the volume on another PC.

## Warning
This was not built with any secutiry in mind, so make sure that you **DO NOT** expose it to outside connections from the internet, as it would be a major backdoor since it basically grants remote control over the computer. I might consider adding some security later on, or perhaps a configuration file for the server to only allow specific keys.
