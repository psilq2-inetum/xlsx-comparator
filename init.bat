python -m venv .venv

@echo off

set "venv_command=.\.venv\Scripts\activate"
set "venv_command=%venv_command% & pip install -r requirements.txt"
set "venv_command=%venv_command% & exit"

cmd /k "%venv_command%"