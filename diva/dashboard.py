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
        col_width = int(lcm / num_cols)
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

def get_grid_size(layout):
    max_x = max([x + w for x, y, w, h in layout])
    max_y = max([y + h for x, y, w, h in layout])
    return (max_x, max_y)

def get_grid(dash):
    grid_size = get_grid_size(dash.layout)

    # create a list of panes
    panes = []
    for item, coord in zip(dash.items, dash.layout):
        pane = {}
        # add 1 to point b/c CSS grids start at (1, 1) not (0, 0)
        css_coord = coord[0] + 1, coord[1] + 1, coord[2], coord[3]
        pane['x'], pane['y'], pane['w'], pane['h'] = css_coord
        pane['html'] = convert_to_html(item)
        panes.append(pane)
    return {'size': grid_size, 'panes': panes}
 
@convert_to_html.register(Dashboard)
def dashboard_to_html(dash):
    grid = get_grid(dash)
    return render_template('dashboard.html', grid=grid)
    
