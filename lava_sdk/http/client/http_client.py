import json
from typing import Any, Dict

import requests

from lava_sdk.constants.client_constants import ClientConstants
from lava_sdk.exceptions.base_exception import LavaBaseException


class HttpClient:
    """Low-level HTTP client using the requests library."""

    def post_request(self, method: str, data: Dict[str, Any], timeout: int = 5) -> Dict[str, Any]:
        """Send a POST request to the Lava API."""
        url = ClientConstants.URL + method
        try:
            response = requests.post(
                url,
                json=data,
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=timeout,
            )
            return response.json()
        except requests.RequestException as e:
            raise LavaBaseException(f"Error request: {e}") from e
        except (ValueError, json.JSONDecodeError) as e:
            raise LavaBaseException(f"Error decoding response: {e}") from e

    def get_request(self, method: str, data: Dict[str, Any], timeout: int = 5) -> Dict[str, Any]:
        """Send a GET request to the Lava API with query params."""
        url = ClientConstants.URL + method
        try:
            response = requests.get(
                url,
                params=data,
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=timeout,
            )
            return response.json()
        except requests.RequestException as e:
            raise LavaBaseException(f"Error request: {e}") from e
        except (ValueError, json.JSONDecodeError) as e:
            raise LavaBaseException(f"Error decoding response: {e}") from e
