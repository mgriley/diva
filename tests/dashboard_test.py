import pytest
from diva.dashboard import row_layout, get_grid_size

def test_grid_size():
    size = get_grid_size([[0, 0, 1, 1]])
    assert size == (1, 1)
    size = get_grid_size([[0, 0, 1, 1], [1, 0, 1, 1]])
    assert size == (2, 1)
    size = get_grid_size(row_layout(1, 2))
    assert size == (2, 2)

def test_row_layout():
    layout = row_layout(1)
    assert layout == [[0, 0, 1, 1]]
    layout = row_layout(2)
    assert layout == [[0, 0, 1, 1], [1, 0, 1, 1]]
    layout = row_layout(1, 2)
    assert layout == [[0, 0, 2, 1], [0, 1, 1, 1], [1, 1, 1, 1]]
    layout = row_layout(2, 2)
    assert layout == [[0, 0, 2, 1], [2, 0, 2, 1], [0, 1, 2, 1], [2, 1, 2, 1]]
