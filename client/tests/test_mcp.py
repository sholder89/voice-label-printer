"""MCP endpoint tests.

    python -m unittest discover -s client/tests

Runs the real Flask app against a throwaway data directory, with the MCP server
on an ephemeral port pointed at it. Nothing is sent to a printer: label_print is
only checked for its schema, never called.
"""
import json
import os
import socket
import sys
import tempfile
import threading
import time
import unittest

_TMP = tempfile.TemporaryDirectory()
os.environ["LABEL_DATA_DIR"] = _TMP.name      # never touch %APPDATA%\LabelPrinter
os.environ["MCP_ENABLED"] = "true"
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import httpx                                   # noqa: E402
from mcp import ClientSession                  # noqa: E402
from mcp.client.streamable_http import streamablehttp_client  # noqa: E402
from werkzeug.serving import make_server       # noqa: E402

import app as label_app                        # noqa: E402
import mcp_server                              # noqa: E402

EXPECTED_TOOLS = {
    "label_status", "label_list_printers", "label_list_sizes",
    "label_list_style_presets", "label_preview", "label_history",
    "label_list_addresses", "label_print", "label_save_address",
}
WRITE_TOOLS = {"label_print", "label_save_address"}


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _start_mcp(flask_port, **kw):
    port = _free_port()
    thread = mcp_server.start(flask_port, port=port, allowed_origins=[], **kw)
    assert thread is not None, "MCP server did not start"
    deadline = time.time() + 15
    while not thread.server.started:
        if time.time() > deadline:
            raise RuntimeError("MCP server did not come up")
        time.sleep(0.05)
    return thread, f"http://127.0.0.1:{port}/mcp"


def setUpModule():
    global _flask, _mcp, _mcp_url, _mcp_tok, _mcp_tok_url
    label_app.state["printer"] = ""            # belt and braces: no printer to hit
    _flask = make_server("127.0.0.1", 0, label_app.app, threaded=True)
    threading.Thread(target=_flask.serve_forever, daemon=True).start()
    _mcp, _mcp_url = _start_mcp(_flask.server_port, token="")
    _mcp_tok, _mcp_tok_url = _start_mcp(_flask.server_port, token="s3cret")
    # mcp_server.api is shared, so both servers talk to the same Flask instance.


def tearDownModule():
    for t in (_mcp, _mcp_tok):
        t.server.should_exit = True
    _flask.shutdown()


class McpToolsTest(unittest.IsolatedAsyncioTestCase):

    async def _call(self, fn, url=None, headers=None):
        async with streamablehttp_client(url or _mcp_url, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return await fn(session)

    async def test_tool_names(self):
        tools = await self._call(lambda s: s.list_tools())
        self.assertEqual({t.name for t in tools.tools}, EXPECTED_TOOLS)

    async def test_every_tool_has_annotations(self):
        tools = (await self._call(lambda s: s.list_tools())).tools
        for tool in tools:
            with self.subTest(tool=tool.name):
                a = tool.annotations
                self.assertIsNotNone(a)
                self.assertIsNotNone(a.openWorldHint)
                if tool.name in WRITE_TOOLS:
                    self.assertFalse(a.readOnlyHint)
                    self.assertFalse(a.destructiveHint)
                else:
                    self.assertTrue(a.readOnlyHint)
        self.assertTrue(next(t for t in tools if t.name == "label_print").annotations.openWorldHint)

    async def test_print_caps_copies(self):
        tools = (await self._call(lambda s: s.list_tools())).tools
        schema = next(t for t in tools if t.name == "label_print").inputSchema
        self.assertEqual(schema["properties"]["copies"]["maximum"], 5)

    async def test_preview_returns_png(self):
        res = await self._call(lambda s: s.call_tool(
            "label_preview", {"text": "Spices", "size": "2x1", "style_preset": "minimal"}))
        self.assertFalse(res.isError, res.content)
        image = next(c for c in res.content if c.type == "image")
        self.assertEqual(image.mimeType, "image/png")
        import base64
        self.assertTrue(base64.b64decode(image.data).startswith(b"\x89PNG"))
        self.assertEqual(res.structuredContent["size"], "2x1")
        self.assertEqual(res.structuredContent["style_preset"], "minimal")

    async def test_preview_rejects_unknown_size(self):
        res = await self._call(lambda s: s.call_tool(
            "label_preview", {"text": "x", "size": "9x9"}))
        self.assertTrue(res.isError)
        self.assertIn("label_list_sizes", res.content[0].text)

    async def test_reads_return_lists(self):
        for name in ("label_list_sizes", "label_list_style_presets", "label_history"):
            with self.subTest(tool=name):
                res = await self._call(lambda s: s.call_tool(name, {"limit": 3}))
                self.assertFalse(res.isError, res.content)
                data = res.structuredContent
                self.assertIn("total", data)
                self.assertLessEqual(len(data["items"]), 3)
        sizes = (await self._call(lambda s: s.call_tool("label_list_sizes", {}))).structuredContent
        self.assertIn("50mm-round", {i["key"] for i in sizes["items"]})
        self.assertNotIn("53mm-round", {i["key"] for i in sizes["items"]})

    async def test_status_has_no_telegram_flag(self):
        res = await self._call(lambda s: s.call_tool("label_status", {}))
        self.assertFalse(res.isError, res.content)
        self.assertNotIn("telegram", res.structuredContent)
        self.assertIn("default_style", res.structuredContent)

    async def test_save_address_round_trip(self):
        res = await self._call(lambda s: s.call_tool("label_save_address", {
            "label": "Test", "name": "Ada Lovelace", "line1": "1 Engine Way",
            "csz": "London"}))
        self.assertFalse(res.isError, res.content)
        new_id = res.structuredContent["id"]
        listed = await self._call(lambda s: s.call_tool("label_list_addresses", {}))
        match = [a for a in listed.structuredContent["items"] if a["id"] == new_id]
        self.assertEqual(len(match), 1)
        self.assertEqual(match[0]["name"], "Ada Lovelace")


class McpHttpTest(unittest.TestCase):
    INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {},
        "clientInfo": {"name": "test", "version": "0"}}}
    HEADERS = {"accept": "application/json, text/event-stream",
               "content-type": "application/json"}

    def test_foreign_origin_rejected(self):
        r = httpx.post(_mcp_url, json=self.INIT,
                       headers={**self.HEADERS, "origin": "https://evil.example"})
        self.assertEqual(r.status_code, 403)

    def test_no_origin_accepted(self):
        r = httpx.post(_mcp_url, json=self.INIT, headers=self.HEADERS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["result"]["serverInfo"]["name"], "voice-label-printer")

    def test_foreign_host_rejected(self):
        r = httpx.post(_mcp_url, json=self.INIT,
                       headers={**self.HEADERS, "host": "attacker.example:5002"})
        self.assertEqual(r.status_code, 421)

    def test_get_and_delete_are_405(self):
        for method in ("GET", "DELETE"):
            with self.subTest(method=method):
                r = httpx.request(method, _mcp_url)
                self.assertEqual(r.status_code, 405)
                self.assertEqual(r.headers["allow"], "POST")

    def test_oversized_body_rejected(self):
        r = httpx.post(_mcp_url, content=b'{"x":"' + b"a" * (1024 * 1024 + 10) + b'"}',
                       headers=self.HEADERS)
        self.assertEqual(r.status_code, 413)

    def test_token_required_when_set(self):
        r = httpx.post(_mcp_tok_url, json=self.INIT, headers=self.HEADERS)
        self.assertEqual(r.status_code, 401)
        r = httpx.post(_mcp_tok_url, json=self.INIT,
                       headers={**self.HEADERS, "authorization": "Bearer wrong"})
        self.assertEqual(r.status_code, 401)
        r = httpx.post(_mcp_tok_url, json=self.INIT,
                       headers={**self.HEADERS, "authorization": "Bearer s3cret"})
        self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    unittest.main()
