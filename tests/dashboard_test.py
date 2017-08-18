import pytest
from diva.dashboard import row_layout

def test_row_layout():
    layout = row_layout(1)
    assert layout == [[0, 0, 1, 1]]
    layout = row_layout(2)
    assert layout == [[0, 0, 1, 1], [1, 0, 1, 1]]
    layout = row_layout(1, 2)
    assert layout == [[0, 0, 2, 1], [0, 1, 1, 1], [1, 1, 1, 1]]
    layout = row_layout(2, 2)
    assert layout == [[0, 0, 2, 1], [2, 0, 2, 1], [0, 1, 2, 1], [2, 1, 2, 1]]
