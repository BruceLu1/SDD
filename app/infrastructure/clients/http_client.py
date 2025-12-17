import http.client
from typing import Any


class SimpleHttpClient:
    def get(self, host: str, path: str) -> tuple[int, Any]:
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", path)
        res = conn.getresponse()
        data = res.read()
        return res.status, data
