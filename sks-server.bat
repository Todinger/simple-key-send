@ECHO OFF
CMD /K "%~dp0venv\Scripts\activate & python %~dp0key-server.py %* & deactivate & exit"
