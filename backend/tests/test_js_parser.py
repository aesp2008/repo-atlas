from app.services.parsers.js_parser import parse_js_ts_file


def test_js_import_parsing():
    content = '''
import express from "express";
import { foo } from "./utils";
const bar = require("../lib/bar");

export function handler() {}
export class Service {}
const fn = async () => {};
'''
    parsed = parse_js_ts_file("src/server.js", content, len(content), "javascript")
    modules = {imp.module for imp in parsed.imports}
    assert "express" in modules
    assert "./utils" in modules
    assert "../lib/bar" in modules


def test_express_endpoint_detection():
    content = '''
const app = express();
app.get("/health", handler);
router.post("/api/users", createUser);
router.delete("/api/users/:id", deleteUser);
'''
    parsed = parse_js_ts_file("src/server.ts", content, len(content), "typescript")
    routes = {(e.method, e.path) for e in parsed.endpoints}
    assert ("GET", "/health") in routes
    assert ("POST", "/api/users") in routes
    assert ("DELETE", "/api/users/:id") in routes


def test_js_symbol_parsing():
    content = '''
export function getData() {}
export class Repository {}
export const fetchAll = async () => {};
'''
    parsed = parse_js_ts_file("src/api.ts", content, len(content), "typescript")
    names = {s.name for s in parsed.symbols}
    assert "getData" in names
    assert "Repository" in names
    assert "fetchAll" in names
