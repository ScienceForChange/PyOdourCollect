from pyodourcollect import (command_line, occore, ochelpers, ocmodels)
import subprocess
import os

CMDLINETOOL = '..\.venv\Scripts\python.exe ..\src\pyodourcollect\__init__.py'


def test_args_output():
    filename = 'test_output.csv'
    if os.path.exists(filename):
        os.remove(filename)
    test = subprocess.run(CMDLINETOOL + ' --output ' + filename, shell=True)
    assert test.returncode == 0


def test_format_detection():
    filename = 'formatdetection.xlsx'
    if os.path.exists(filename):
        os.remove(filename)
    test = subprocess.run(CMDLINETOOL + ' --output' + filename, shell=True)
    assert test.returncode == 0


