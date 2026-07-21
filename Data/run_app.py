import sys
import os

venv_python = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'venv', 'Scripts', 'python.exe')
if sys.executable != venv_python and os.path.exists(venv_python):
    os.execl(venv_python, venv_python, *sys.argv)

import streamlit.web.cli as stcli

app_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_qa.py")
sys.argv = ["streamlit", "run", app_file_path, "--server.headless=true", "--browser.gatherUsageStats=false"]
stcli.main()
