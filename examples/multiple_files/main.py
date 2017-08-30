from diva import Diva
from foo import app as foo_app
from bar import app as bar_app

app = Diva()

# adds all of the views from foo_app and bar_app
# to this app
app.extend(foo_app)
app.extend(bar_app)

app.run(debug=True)

