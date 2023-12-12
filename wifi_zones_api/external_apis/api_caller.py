"""Api calls main functions"""
from typing import Any

# Utils
import requests


def api_post(url: str, data: dict, params=None) -> tuple[Any, int] | tuple[None, None]:
    try:
        response = requests.post(url, json=data, params=params)
        response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if response:
            return response.json(), response.status_code
        return None, None


def api_get(url, params=None) -> tuple[Any, int] | tuple[None, None]:
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if response:
            return response.json(), response.status_code
        return None, None
