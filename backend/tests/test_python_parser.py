import pytest

from app.services.parsers.python_parser import parse_python_file


SAMPLE_PYTHON = '''
import os
from shared.models import User

class UserService:
    pass

def get_user():
    if True:
        return User(1, "a", "b")
    return None

@app.get("/users")
def list_users():
    pass

@app.route("/items", methods=["GET", "POST"])
def items():
    pass
'''.replace("@app.get", "@app.get").replace("@app.route", "@app.route")


def test_python_import_parsing():
    parsed = parse_python_file("services/user.py", SAMPLE_PYTHON, len(SAMPLE_PYTHON))
    modules = {imp.module for imp in parsed.imports}
    assert "os" in modules
    assert "shared.models" in modules
    assert parsed.lines_of_code > 5


def test_python_symbol_parsing():
    parsed = parse_python_file("services/user.py", SAMPLE_PYTHON, len(SAMPLE_PYTHON))
    names = {s.name for s in parsed.symbols}
    assert "UserService" in names
    assert "get_user" in names
    assert "list_users" in names


def test_fastapi_endpoint_detection():
    content = '''
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    pass

@router.post("/orders")
def create_order():
    pass
'''
    parsed = parse_python_file("main.py", content, len(content))
    methods = {(e.method, e.path) for e in parsed.endpoints}
    assert ("GET", "/health") in methods
    assert ("POST", "/orders") in methods


def test_flask_endpoint_detection():
    content = '''
@app.route("/items", methods=["GET", "POST"])
def items():
    pass
'''
    parsed = parse_python_file("app.py", content, len(content))
    methods = {(e.method, e.path) for e in parsed.endpoints}
    assert ("GET", "/items") in methods
    assert ("POST", "/items") in methods
