from typing import Callable, List, Dict, Any

def paginated_fetch(fetch_fn: Callable[[int], Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generic pagination helper for HTB API responses.

    Arguments:
        fetch_fn: A function that takes a page number (int) and returns an API response dict.

    Returns:
        A flattened list of results across all pages.
    """
    results = []
    page = 1

    while True:
        response = fetch_fn(page)
        data = response.get("data", [])
        if not data:
            break

        results.extend(data)

        if not response.get("links", {}).get("next"):
            break

        page += 1

    return results
