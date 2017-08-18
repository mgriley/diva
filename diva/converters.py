from functools import singledispatch

@singledispatch
def convert_to_html(val):
    # default is to just display the value as a string
    return '<p>{}</p>'.format(str(val))

# assume a raw string is valid HTML
@convert_to_html.register(str)
def str_to_html(html_string):
    return html_string

