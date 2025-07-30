import asyncio
from threading import Thread
from typing import Any, Coroutine, cast

import requests

from fpl_client.endpoints import FPLEndpoints


class FPLClientException(Exception):
    """FPL Client Exception."""


class AsyncRunner:
    def __init__(self) -> None:
        self.loop = asyncio.new_event_loop()
        self.thread = Thread(target=self.start_loop, daemon=True)
        self.thread.start()

    def start_loop(self) -> None:
        """Start the event loop."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def run(self, coro: Coroutine[Any, Any, Any]) -> Any:
        """Run an async coroutine in the background event loop and return the result."""
        return asyncio.run_coroutine_threadsafe(coro, self.loop).result()


class FPLClient:

    def __init__(self) -> None:

        self.session = requests.Session()

    def get_data(self, endpoint: FPLEndpoints | str) -> dict[Any, Any] | str:
        """Make get request."""
        try:
            response = self.session.get(endpoint)
        except Exception as e:
            raise FPLClientException(e)

        if response.status_code == 200:
            try:
                return cast(dict[Any, Any], response.json())
            except Exception:
                return response.text
        else:
            raise FPLClientException(response.text)

    def post_data(
        self, endpoint: FPLEndpoints, payload: dict[Any, Any] | None = None
    ) -> dict[Any, Any]:
        """Make post request."""
        try:
            if payload:
                response = self.session.post(endpoint, json=payload)
            else:
                response = self.session.post(endpoint)
        except Exception as e:
            raise FPLClientException(e)

        if response.status_code == 200:
            return cast(dict[Any, Any], response.json())
        else:
            raise FPLClientException(response.text)
