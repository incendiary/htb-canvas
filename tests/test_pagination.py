from models.pagination import paginated_fetch


def test_single_page_returns_data():
    def fetch(page):
        return {"data": [{"id": 1}], "links": {}}

    assert paginated_fetch(fetch) == [{"id": 1}]


def test_multi_page_aggregates_all():
    pages = {
        1: {"data": [{"id": 1}], "links": {"next": "page2"}},
        2: {"data": [{"id": 2}], "links": {}},
    }

    assert paginated_fetch(lambda p: pages[p]) == [{"id": 1}, {"id": 2}]


def test_empty_first_page_returns_empty():
    def fetch(page):
        return {"data": [], "links": {}}

    assert paginated_fetch(fetch) == []


def test_stops_after_page_with_no_next_link():
    call_count = {"n": 0}

    def fetch(page):
        call_count["n"] += 1
        return {"data": [{"id": page}], "links": {}}

    result = paginated_fetch(fetch)
    assert result == [{"id": 1}]
    assert call_count["n"] == 1
