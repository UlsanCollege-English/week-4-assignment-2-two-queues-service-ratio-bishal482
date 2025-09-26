import pytest
from src.gate import Gate

def test_ratio_and_skips():
    g = Gate()
    g.arrive("regular","r1"); g.arrive("regular","r2"); g.arrive("regular","r3")
    g.arrive("fastpass","f1")
    # pattern F,R,R,R
    assert g.serve() == "f1"
    assert g.serve() == "r1"
    assert g.serve() == "r2"
    assert g.serve() == "r3"
    with pytest.raises(IndexError):
        g.serve()

def test_peek_next_line():
    g = Gate()
    assert g.peek_next_line() is None
    g.arrive("regular","r1")
    assert g.peek_next_line() == "regular"
    g.arrive("fastpass","f1")
    assert g.peek_next_line() == "fastpass"


# --- Edge Cases ---
def test_edge_serve_when_both_empty():
    g = Gate()
    with pytest.raises(IndexError):
        g.serve()
    assert g.peek_next_line() is None

def test_edge_pattern_wrap_with_sparse_lines():
    g = Gate()
    # Only fastpass riders arrive; ensure cycle still advances correctly
    g.arrive("fastpass", "f1"); g.arrive("fastpass", "f2")
    assert g.peek_next_line() == "fastpass"
    assert g.serve() == "f1"   # consume F slot
    # pattern would point to R, but it's empty; serving should skip to F
    assert g.serve() == "f2"
    with pytest.raises(IndexError):
        g.serve()

# --- Longer Scenario ---
def test_long_mixed_arrivals_and_service():
    g = Gate()
    # Seed queues
    for i in range(1, 7):
        g.arrive("regular", f"r{i}")
    g.arrive("fastpass", "f1"); g.arrive("fastpass", "f2")
    served = []
    for _ in range(8):
        served.append(g.serve())
    # Pattern: F,R,R,R cycling with skips handled; check relative counts
    # Expect 2 fastpass served and 6 regulars in first 8 serves (since both lines have stock)
    assert served.count("f1") + served.count("f2") == 2
    assert sum(1 for s in served if s.startswith("r")) == 6
