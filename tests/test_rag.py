from src import rag


def test_build_and_search():
    n = rag.build_index()
    assert n > 0

    docs = rag.search_manual_raw("spindle bearing over temperature")
    assert docs
    assert any("spindle" in d.lower() for d in docs)
