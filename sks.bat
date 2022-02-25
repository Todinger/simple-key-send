@ECHO OFF
CMD /K "%~dp0venv\Scripts\activate & python %~dp0key-client.py %* & deactivate & exit"
