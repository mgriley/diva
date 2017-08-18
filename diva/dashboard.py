from .converters import convert_to_html
from .utils import render_template

# A 'layout' is a list of [x, y, width, height] items, 1 for each panel
# where x, y is the position of the top-left corner of the panel, and
# the parent container has (0, 0) in the top-left with +y downwards
    
# helpers for defining layouts
def row_layout(*row_sizes):
    # calc a common-multiple so that can define all columns
    # (not actually the LCM using this lazy way)
    lcm = 1
    for size in row_sizes:
        lcm *= size
    layout = []
    for row_num, num_cols in enumerate(row_sizes):
        col_width = lcm / num_cols
        for i in range(num_cols):
            layout.append([i * col_width, row_num, col_width, 1])

    return layout
        
class Dashboard():
    # default layout is a vertical list of items
    def __init__(self, items, layout=None):
        self.items = items
        if layout is None:
            self.layout = [[0, i, 1, 1] for i in range(len(items))]
        else:
            self.layout = layout
 
@convert_to_html.register(Dashboard)
def dashboard_to_html(d):
    # convert layout lists to list of [startx, starty, endx, endy] lists
    coords = [[x, y, x + w, y + h] for x, y, w, h in d.layout]
    # get the desired size of the grid (max bot-right coord)
    max_x = max([p[0] for p in coords])
    max_y = max([p[1] for p in coords])
    grid_size = (max_x, max_y) 

    # create a list of panes
    panes = []
    for item, coord in zip(d.items, coords):
        pane = {}
        # add 1 b/c CSS grids start at (1, 1) not (0, 0)
        coord = [p + 1 for p in coord]
        pane['x0'], pane['y0'], pane['x1'], pane['y1'] = coord
        pane['html'] = convert_to_html(item)
        panes.append(pane)
    return render_template('dashboard.html', grid={'size': grid_size, 'panes': panes})
